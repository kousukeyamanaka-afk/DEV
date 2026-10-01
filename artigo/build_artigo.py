#!/usr/bin/env python3
"""Gera .docx do artigo a partir dos .md em artigo/, reaproveitando os estilos
do manuscrito original (artigo/original/*.docx). Só biblioteca padrão.

Marcação aceita (um parágrafo por bloco, separados por linha em branco):
  %title / %subtitle / %author / %meta   folha de rosto
  %resumo TEXTO                            título do resumo
  %abs TEXTO                               parágrafo do resumo
  # TEXTO                                  título de seção (Heading1)
  ## TEXTO                                 subtítulo (Heading2)
  > TEXTO                                  frase em destaque (KeyQuote)
  @ TEXTO                                  referência (recuo francês)
  - TEXTO                                  item de lista
  *itálico*  **negrito**                   dentro de qualquer parágrafo

Uso:
  python3 artigo/build_artigo.py            gera os dois arquivos
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).resolve().parent
MODELO = AQUI / "original" / "Contentamento_Dinamico_Versao_2_Alan_Yamanaka.docx"
SAIDAS = AQUI / "saidas"
TRABALHOS = [
    ("Contentamento_Dinamico_V3.md", "Contentamento_Dinamico_Versao_3_Alan_Yamanaka.docx"),
    ("RELATORIO_EDITORIAL.md", "Relatorio_Editorial_Contentamento_Dinamico_V3.docx"),
]

BORDA = ('<w:pBdr><w:left w:val="single" w:sz="12" w:space="8" '
         'w:color="203A5F"/></w:pBdr>')


def runs(texto, base_rpr=""):
    """Converte *itálico* e **negrito** em runs."""
    partes = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", texto)
    out = []
    for p in partes:
        if not p:
            continue
        rpr = base_rpr
        if p.startswith("**") and p.endswith("**"):
            p, rpr = p[2:-2], rpr + "<w:b/>"
        elif p.startswith("*") and p.endswith("*") and len(p) > 1:
            p, rpr = p[1:-1], rpr + "<w:i/>"
        rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        out.append(f'<w:r>{rpr_xml}<w:t xml:space="preserve">{escape(p)}</w:t></w:r>')
    return "".join(out)


def par(estilo, texto, extra_ppr="", base_rpr=""):
    st = f'<w:pStyle w:val="{estilo}"/>' if estilo else ""
    return f"<w:p><w:pPr>{st}{extra_ppr}</w:pPr>{runs(texto, base_rpr)}</w:p>"


def converter(md):
    blocos = [b.strip() for b in re.split(r"\n\s*\n", md) if b.strip()]
    xml = []
    for b in blocos:
        linha = " ".join(l.strip() for l in b.splitlines())
        cab, _, resto = linha.partition(" ")
        centro = '<w:jc w:val="center"/>'
        if cab == "%title":
            xml.append(par("Title", resto, centro))
        elif cab == "%subtitle":
            xml.append(par("Subtitle", resto, centro))
        elif cab == "%author":
            xml.append(par("AuthorLine", resto, centro))
        elif cab == "%meta":
            xml.append(par("MetaLine", resto, centro))
        elif cab == "%resumo":
            xml.append(par("Abstract", resto, base_rpr='<w:b/><w:color w:val="203A5F"/>'))
        elif cab == "%abs":
            xml.append(par("Abstract", resto))
        elif cab == "#":
            xml.append(par("Heading1", resto))
        elif cab == "##":
            xml.append(par("Heading2", resto))
        elif cab == ">":
            xml.append(par("KeyQuote", resto, BORDA))
        elif cab == "@":
            xml.append(par("Reference", resto))
        elif cab == "-":
            # listas: cada linha "- " vira um item
            for item in b.splitlines():
                xml.append(par("ListBullet", item.strip()[2:].strip()))
        else:
            xml.append(par("", linha, "<w:widowControl/>"))
    return "".join(xml)


def gerar(md_path, docx_path):
    with zipfile.ZipFile(MODELO) as z:
        doc = z.read("word/document.xml").decode("utf8")
        inicio = doc.index("<w:body>") + len("<w:body>")
        sect = doc[doc.rindex("<w:sectPr"):]
        novo = doc[:inicio] + converter(md_path.read_text(encoding="utf8")) + sect
        with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as out:
            for item in z.infolist():
                dados = novo.encode("utf8") if item.filename == "word/document.xml" else z.read(item.filename)
                out.writestr(item, dados)
    print(f"gerado: {docx_path.relative_to(AQUI.parent)}")


def main():
    SAIDAS.mkdir(exist_ok=True)
    for md, docx in TRABALHOS:
        gerar(AQUI / md, SAIDAS / docx)


if __name__ == "__main__":
    sys.exit(main())
