#!/usr/bin/env python3
"""Monta A Menina Elefante em .docx, diagramado como livro (5,5 x 8,5 pol.), a partir dos estilos do modelo
(referencia/modelo_estilos.docx, cópia do .docx de O Jardim).

Uso:
  python3 tools/build.py              -> saidas/A_Menina_Elefante_V2.docx (livro inteiro, com folha de rosto)
  python3 tools/build.py --parte IV   -> saidas/A_Menina_Elefante_V2_Parte_IV.docx (só aquela parte)

Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com "—";
"*" sozinho numa linha = quebra de cena.

Diagramação (constantes DIAG abaixo): EB Garamond 12 pt, entrelinha exata de 17,6 pt, margens espelhadas, hifenização em
português; cabeçalho com o título do livro nas páginas pares e o do capítulo nas ímpares; abertura de capítulo,
páginas de parte, folha de rosto e páginas de destaque sem cabeçalho. As fontes (EB Garamond e Bebas Neue, OFL)
vão embutidas no .docx a partir de referencia/fontes/.

Páginas de destaque: manuscrito/destaques.json lista as frases que ganham uma página inteira (fundo escuro,
ornamento de ilustracoes/, letra grande em Bebas Neue). Gere os fundos antes com tools/ornamentos.py.
Só usa a biblioteca padrão do Python.
"""
import datetime, json, math, re, sys, uuid, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'referencia' / 'modelo_estilos.docx'
FONTES = ROOT / 'referencia' / 'fontes'
HEADER_MODELO = 'O JARDIM ENTRE O AGORA E O DEPOIS'
SERIF, DISPLAY = 'EB Garamond', 'Bebas Neue'
EMBUTIR = [(SERIF, 'Regular', 'EBGaramond-Regular.ttf'), (SERIF, 'Italic', 'EBGaramond-Italic.ttf'),
           (SERIF, 'Bold', 'EBGaramond-Bold.ttf'), (DISPLAY, 'Regular', 'BebasNeue-Regular.ttf')]
EMU = 914400
NS_PIC = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"',
          'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
R_HDR = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/header'
R_FTR = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer'
CT_HDR = 'application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml'
CT_FTR = 'application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml'

# medidas em twips (1/1440 pol.) e meios-pontos
DIAG = dict(
    corpo=24,            # 12 pt
    entrelinha=352,      # exata, 17,6 pt (não depende das métricas da fonte em cada sistema)
    recuo=340,           # recuo da primeira linha (0,6 cm)
    pag_w=7920, pag_h=12240,
    margem_int=1150, margem_ext=870, margem_sup=1000, margem_inf=1000,
    cabecalho=560, rodape=560,
)


# ---------- texto ----------
def run(t, rpr=''):
    return f'<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'


def para(t, primeiro=False, recuo=True):
    """Parágrafo de corpo. primeiro=True: sem recuo e com as primeiras palavras em versalete."""
    ppr = '<w:pPr><w:ind w:firstLine="0"/></w:pPr>' if (primeiro or not recuo) else ''
    if primeiro:
        m = re.match(r'^((?:\S+\s+){0,3}\S+)(.*)$', t, re.S)
        cabeca, resto = (m.group(1), m.group(2)) if m else (t, '')
        return f'<w:p>{ppr}{run(cabeca, "<w:smallCaps/>")}{run(resto) if resto else ""}</w:p>'
    return f'<w:p>{ppr}{run(t)}</w:p>'


def scene_break():
    return ('<w:p><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="200"/><w:ind w:firstLine="0"/>'
            '<w:jc w:val="center"/></w:pPr>' + run('*   *   *') + '</w:p>')


def centrado(t, sz, antes=0, depois=0, rpr_extra='', estilo=None, espaco=0):
    pst = f'<w:pStyle w:val="{estilo}"/>' if estilo else ''
    rpr = (f'<w:rFonts w:ascii="{SERIF}" w:hAnsi="{SERIF}"/>{rpr_extra}'
           + (f'<w:spacing w:val="{espaco}"/>' if espaco else '') + f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    return (f'<w:p><w:pPr>{pst}<w:keepNext/><w:spacing w:before="{antes}" w:after="{depois}" w:line="240" w:lineRule="auto"/>'
            f'<w:ind w:firstLine="0"/><w:jc w:val="center"/></w:pPr>{run(t, rpr)}</w:p>')


def abertura(rotulo, titulo):
    """Abertura de capítulo: rótulo pequeno espaçado, título grande, respiro."""
    out = []
    if rotulo:
        out.append(centrado(rotulo, 19, antes=1500, depois=160, espaco=40, rpr_extra='<w:color w:val="555555"/>'))
    out.append(centrado(titulo, 34, antes=0 if rotulo else 1500, depois=900, espaco=10))
    return out


def body_from_txt(path, destaques=()):
    """Devolve segmentos: ('texto', [parágrafos]) e ('destaque', d). Cada página de destaque entra na próxima
    quebra de cena depois da âncora, ou no fim do capítulo."""
    txt = path.read_text(encoding='utf-8').strip()
    paras = [p.strip() for p in re.split(r'\n\s*\n', txt) if p.strip()]
    for d in destaques:
        if not any(d['ancora'] in p for p in paras):
            sys.exit(f"âncora não encontrada em {path.name}: {d['ancora']}")
    segs, atual, pendentes, primeiro, depois_quebra = [], [], [], True, False
    for p in paras:
        if p == '*':
            if pendentes:
                segs.append(('texto', atual)); atual = []
                segs += [('destaque', d) for d in pendentes]; pendentes = []
            atual.append(scene_break()); depois_quebra = True
            continue
        atual.append(para(p, primeiro=primeiro, recuo=not depois_quebra))
        primeiro = depois_quebra = False
        pendentes += [d for d in destaques if d['ancora'] in p]
    segs.append(('texto', atual))
    segs += [('destaque', d) for d in pendentes]
    return segs


# ---------- página de destaque ----------
class Midia:
    def __init__(self):
        self.arquivos, self.n = {}, 0

    def rid(self, path):
        if path not in self.arquivos:
            self.arquivos[path] = f'rIdImg{len(self.arquivos) + 1}'
        return self.arquivos[path]

    def novo_id(self):
        self.n += 1
        return 1000 + self.n


def fundo_pagina(midia, png):
    cx, cy = DIAG['pag_w'] * EMU // 1440, DIAG['pag_h'] * EMU // 1440
    rid, i = midia.rid(png), midia.novo_id()
    return ('<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="0" '
            'behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
            '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
            f'<wp:docPr id="{i}" name="Destaque {i}"/><wp:cNvGraphicFramePr/>'
            f'<a:graphic {NS_PIC[0]}><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic {NS_PIC[1]}><pic:nvPicPr><pic:cNvPr id="{i}" name="{png.name}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            '</wp:anchor></w:drawing></w:r>')


def pagina_destaque(d, midia):
    png = ROOT / 'ilustracoes' / f"destaque_{d['ornamento']}_{d['lado']}.png"
    if not png.exists():
        sys.exit(f'falta {png.relative_to(ROOT)}: rode python3 tools/ornamentos.py')
    jc = 'right' if d['lado'] == 'esq' else 'left'
    limpo = d['frase'].replace('[[', '').replace(']]', '')
    larg_pt = (DIAG['pag_w'] - DIAG['margem_int'] - DIAG['margem_ext']) / 20
    pt = min(58, 0.93 * math.sqrt(larg_pt * 230 / (0.40 * len(limpo))))
    sz = int(pt) * 2

    def r(txt, cor):
        return (f'<w:r><w:rPr><w:rFonts w:ascii="{DISPLAY}" w:hAnsi="{DISPLAY}" w:cs="{DISPLAY}"/><w:caps/>'
                f'<w:color w:val="{cor}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape(txt.upper())}</w:t></w:r>')
    runs = ''.join(r(s, 'FFFFFF' if k % 2 else 'A9A9A4') for k, s in enumerate(re.split(r'\[\[|\]\]', d['frase'])) if s)
    out = [f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:ind w:firstLine="0"/></w:pPr>{fundo_pagina(midia, png)}</w:p>',
           f'<w:p><w:pPr><w:spacing w:before="900" w:after="0" w:line="{int(pt * 20 * 1.02)}" w:lineRule="exact"/>'
           f'<w:ind w:firstLine="0"/><w:jc w:val="{jc}"/></w:pPr>{runs}</w:p>']
    if d.get('autor'):
        out.append(f'<w:p><w:pPr><w:spacing w:before="240" w:after="0"/><w:ind w:firstLine="0"/><w:jc w:val="{jc}"/></w:pPr>'
                   f'<w:r><w:rPr><w:rFonts w:ascii="{DISPLAY}" w:hAnsi="{DISPLAY}"/><w:caps/><w:color w:val="A9A9A4"/>'
                   f'<w:spacing w:val="30"/><w:sz w:val="26"/></w:rPr><w:t xml:space="preserve">— {escape(d["autor"].upper())}</w:t></w:r></w:p>')
    return out


# ---------- seções, cabeçalhos e rodapés ----------
class Partes:
    """Cabeçalhos/rodapés extras (vazio e um por capítulo) e suas relações."""
    def __init__(self, cab_modelo):
        self.cab_modelo = cab_modelo
        self.arquivos = {}          # nome do arquivo -> xml
        self.rels = []              # (rid, tipo, alvo, content-type)
        self.add('header_vazio.xml', 'rIdHVazio', R_HDR, CT_HDR, self._hdr(''))
        self.add('footer_vazio.xml', 'rIdFVazio', R_FTR, CT_FTR,
                 self._hdr('').replace('<w:hdr ', '<w:ftr ').replace('</w:hdr>', '</w:ftr>'))
        self.n = 0

    def _hdr(self, texto):
        corpo = re.sub(r'<w:t>[^<]*</w:t>', f'<w:t xml:space="preserve">{escape(texto)}</w:t>', self.cab_modelo)
        return corpo if texto else re.sub(r'<w:r>.*?</w:r>', '', corpo, flags=re.S)

    def add(self, nome, rid, tipo, ct, xml):
        self.arquivos[nome] = xml
        self.rels.append((rid, tipo, nome, ct))

    def cabecalho(self, texto):
        self.n += 1
        rid = f'rIdHCap{self.n}'
        self.add(f'header_cap{self.n}.xml', rid, R_HDR, CT_HDR, self._hdr(texto))
        return rid


def sect_pr(tipo, cab=None, centro=False):
    """tipo: 'vazio' (sem cabeçalho nem número), 'abre' (abertura de capítulo: sem cabeçalho na 1ª página),
    'segue' (continuação de capítulo)."""
    if tipo == 'vazio':
        refs = ('<w:headerReference w:type="even" r:id="rIdHVazio"/><w:headerReference w:type="default" r:id="rIdHVazio"/>'
                '<w:headerReference w:type="first" r:id="rIdHVazio"/><w:footerReference w:type="even" r:id="rIdFVazio"/>'
                '<w:footerReference w:type="default" r:id="rIdFVazio"/><w:footerReference w:type="first" r:id="rIdFVazio"/>')
    else:
        refs = (f'<w:headerReference w:type="even" r:id="rId9"/><w:headerReference w:type="default" r:id="{cab}"/>'
                '<w:headerReference w:type="first" r:id="rIdHVazio"/><w:footerReference w:type="even" r:id="rId10"/>'
                '<w:footerReference w:type="default" r:id="rId10"/><w:footerReference w:type="first" r:id="rId10"/>')
    D = DIAG
    return (f'<w:sectPr>{refs}<w:type w:val="nextPage"/><w:pgSz w:w="{D["pag_w"]}" w:h="{D["pag_h"]}"/>'
            f'<w:pgMar w:top="{D["margem_sup"]}" w:right="{D["margem_ext"]}" w:bottom="{D["margem_inf"]}" '
            f'w:left="{D["margem_int"]}" w:header="{D["cabecalho"]}" w:footer="{D["rodape"]}" w:gutter="0"/>'
            '<w:cols w:space="720"/>' + ('<w:vAlign w:val="center"/>' if centro else '')
            + ('<w:titlePg/>' if tipo == 'abre' else '') + '<w:docGrid w:linePitch="360"/></w:sectPr>')


def fecha_secao(sp):
    return (f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>'
            f'<w:ind w:firstLine="0"/>{sp}</w:pPr></w:p>')


def ofuscar(fonte, chave):
    """Ofuscação de fonte embutida (ECMA-376, 17.8.1): XOR dos 32 primeiros bytes com a chave GUID invertida."""
    k = bytes.fromhex(chave.strip('{}').replace('-', ''))[::-1]
    b = bytearray(fonte)
    for i in range(32):
        b[i] ^= k[i % 16]
    return bytes(b)


def ajustar_estilos(xml):
    D = DIAG
    xml = xml.replace('<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>',
                      '<w:lang w:val="pt-BR" w:eastAsia="ja-JP" w:bidi="ar-SA"/>')
    normal = re.search(r'<w:style w:type="paragraph" w:default="1" w:styleId="Normal">.*?</w:style>', xml, re.S).group(0)
    novo = (f'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
            f'<w:pPr><w:widowControl/><w:spacing w:after="0" w:line="{D["entrelinha"]}" w:lineRule="exact"/>'
            f'<w:ind w:firstLine="{D["recuo"]}"/><w:jc w:val="both"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{SERIF}" w:hAnsi="{SERIF}" w:eastAsia="{SERIF}" w:cs="{SERIF}"/>'
            f'<w:sz w:val="{D["corpo"]}"/><w:szCs w:val="{D["corpo"]}"/><w:lang w:val="pt-BR"/></w:rPr></w:style>')
    xml = xml.replace(normal, novo)
    for sid in ('Header', 'Footer'):
        xml = re.sub(rf'(<w:style w:type="paragraph" w:styleId="{sid}">.*?<w:pPr>)(.*?)(</w:pPr>)',
                     r'\1\2<w:ind w:firstLine="0"/><w:jc w:val="center"/>\3', xml, count=1, flags=re.S)
    return xml


def ajustar_config(xml):
    xml = re.sub(r'(<w:zoom [^>]*/>)', r'\1<w:embedTrueTypeFonts/><w:mirrorMargins/>', xml, count=1)
    return re.sub(r'(<w:defaultTabStop [^>]*/>)',
                  r'\1<w:autoHyphenation/><w:consecutiveHyphenLimit w:val="2"/><w:hyphenationZone w:val="357"/>'
                  r'<w:doNotHyphenateCaps/><w:evenAndOddHeaders/>', xml, count=1)


def main():
    est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
    only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None
    zin = zipfile.ZipFile(TEMPLATE)
    doc = zin.read('word/document.xml').decode('utf-8')
    head = doc[:doc.index('<w:body>') + len('<w:body>')]
    cab_modelo = zin.read('word/header1.xml').decode('utf-8')
    partes, midia = Partes(cab_modelo), Midia()
    arq_dest = ROOT / 'manuscrito' / 'destaques.json'
    todos = json.loads(arq_dest.read_text(encoding='utf-8'))['destaques'] if arq_dest.exists() else []

    secoes = []   # (lista de parágrafos, tipo, rid do cabeçalho, centralizado)

    def capitulo(rotulo, titulo, cabecalho, arquivo, chave):
        cab = partes.cabecalho(cabecalho)
        tipo = 'abre'
        corpo = abertura(rotulo, titulo)
        for kind, conteudo in body_from_txt(ROOT / arquivo, [d for d in todos if d['capitulo'] == chave]):
            if kind == 'texto':
                if conteudo:
                    corpo += conteudo
                continue
            if corpo:
                secoes.append((corpo, tipo, cab, False)); tipo, corpo = 'segue', []
            secoes.append((pagina_destaque(conteudo, midia), 'vazio', None, False))
        if corpo:
            secoes.append((corpo, tipo, cab, False))

    if not only:
        titulo = run(est['titulo_livro'], '<w:spacing w:val="40"/>')
        fr = [f'<w:p><w:pPr><w:pStyle w:val="MyBookTitle"/><w:spacing w:before="0" w:after="0"/>'
              f'<w:ind w:firstLine="0"/></w:pPr>{titulo}</w:p>']
        if est.get('subtitulo'):
            fr.append(centrado(est['subtitulo'], 27, antes=280))
        fr.append(centrado(est['autora'], 22, antes=2600, espaco=30))
        secoes.append((fr, 'vazio', None, True))
        if est.get('dedicatoria'):
            secoes.append(([centrado(est['dedicatoria'], 24, rpr_extra='<w:i/>')], 'vazio', None, True))
        nota = [centrado('NOTA AO LEITOR', 22, antes=1500, depois=500, espaco=40)]
        nota += [f'<w:p><w:pPr><w:ind w:firstLine="0"/><w:jc w:val="center"/></w:pPr>{run(p, "<w:i/>")}</w:p>'
                 for p in re.split(r'\n\s*\n', (ROOT / est['nota']).read_text(encoding='utf-8').strip()) if p.strip()]
        secoes.append((nota, 'vazio', None, False))
        rot, tit = est['prologo']['titulo'].split(' — ', 1) if ' — ' in est['prologo']['titulo'] else ('', est['prologo']['titulo'])
        capitulo(rot, tit, rot or tit, est['prologo']['arquivo'], 'prologo')

    count, missing = 0, []
    for parte in est['partes']:
        if only and parte['numero'] != only:
            continue
        caps = [c for c in parte['capitulos'] if (ROOT / c['arquivo']).exists()]
        missing += [c['n'] for c in parte['capitulos'] if not (ROOT / c['arquivo']).exists()]
        if not caps:
            continue
        rot, tit = parte['titulo'].split(' — ', 1)
        secoes.append(([centrado(rot, 22, depois=300, espaco=60, rpr_extra='<w:color w:val="555555"/>'),
                        centrado(tit, 40, espaco=20)], 'vazio', None, True))
        for c in caps:
            capitulo(f"CAPÍTULO {c['n']}", c['titulo'], c['titulo'], c['arquivo'], c['n'])
            count += 1
    ep = ROOT / est['epilogo']['arquivo']
    if not only and ep.exists():
        capitulo('', est['epilogo']['titulo'], est['epilogo']['titulo'], est['epilogo']['arquivo'], 'epilogo')

    xml = []
    for corpo, tipo, cab, centro in secoes[:-1]:
        xml += corpo
        xml.append(fecha_secao(sect_pr(tipo, cab, centro)))
    corpo, tipo, cab, centro = secoes[-1]
    xml += corpo
    body_sect = sect_pr(tipo, cab, centro)

    name = f"A_Menina_Elefante_V2_Parte_{only}.docx" if only else 'A_Menina_Elefante_V2.docx'
    out = ROOT / 'saidas' / name
    out.parent.mkdir(exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    doc_title = est['titulo_doc'] + (f', Parte {only}' if only else '')
    fontes = [(nome, estilo, FONTES / arq) for nome, estilo, arq in EMBUTIR if (FONTES / arq).exists()]
    chaves = {arq: '{' + str(uuid.uuid5(uuid.NAMESPACE_URL, f'menina-elefante/{arq.name}')).upper() + '}' for _, _, arq in fontes}
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for png in midia.arquivos:
            zout.writestr(f'word/media/{png.name}', png.read_bytes())
        for nome, x in partes.arquivos.items():
            zout.writestr(f'word/{nome}', x)
        for i, (_, _, arq) in enumerate(fontes, 1):
            zout.writestr(f'word/fonts/font{i}.odttf', ofuscar(arq.read_bytes(), chaves[arq]))
        zout.writestr('word/_rels/fontTable.xml.rels',
                      '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                      + ''.join(f'<Relationship Id="rIdF{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" '
                                f'Target="fonts/font{i}.odttf"/>' for i in range(1, len(fontes) + 1))
                      + '</Relationships>')
        for item in zin.infolist():
            if item.filename == 'docProps/thumbnail.jpeg':
                continue
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                data = (head + ''.join(xml) + body_sect + '</w:body></w:document>').encode('utf-8')
            elif item.filename == 'word/header1.xml':
                data = data.decode('utf-8').replace(HEADER_MODELO, escape(est['titulo_livro'])).encode('utf-8')
            elif item.filename == 'word/styles.xml':
                data = ajustar_estilos(data.decode('utf-8')).encode('utf-8')
            elif item.filename == 'word/settings.xml':
                data = ajustar_config(data.decode('utf-8')).encode('utf-8')
            elif item.filename == 'word/fontTable.xml':
                por_nome = {}
                for i, (nome, estilo, arq) in enumerate(fontes, 1):
                    por_nome.setdefault(nome, []).append(f'<w:embed{estilo} r:id="rIdF{i}" w:fontKey="{chaves[arq]}"/>')
                f = ''.join(f'<w:font w:name="{nome}"><w:charset w:val="00"/><w:family w:val="{"roman" if nome == SERIF else "swiss"}"/>'
                            f'<w:pitch w:val="variable"/>{"".join(emb)}</w:font>' for nome, emb in por_nome.items())
                data = data.decode('utf-8').replace('</w:fonts>', f + '</w:fonts>').encode('utf-8')
            elif item.filename == 'word/_rels/document.xml.rels':
                rels = ''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                               f'Target="media/{png.name}"/>' for png, rid in midia.arquivos.items())
                rels += ''.join(f'<Relationship Id="{rid}" Type="{tipo}" Target="{alvo}"/>' for rid, tipo, alvo, _ in partes.rels)
                data = data.decode('utf-8').replace('</Relationships>', rels + '</Relationships>').encode('utf-8')
            elif item.filename == '[Content_Types].xml':
                c = data.decode('utf-8').replace('<Default Extension="rels"', '<Default Extension="png" ContentType="image/png"/>'
                                                 '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/>'
                                                 '<Default Extension="rels"')
                c = c.replace('</Types>', ''.join(f'<Override PartName="/word/{alvo}" ContentType="{ct}"/>'
                                                  for _, _, alvo, ct in partes.rels) + '</Types>')
                data = c.encode('utf-8')
            elif item.filename == 'docProps/core.xml':
                c = data.decode('utf-8')
                c = c.replace('<dc:title/>', f'<dc:title>{escape(doc_title)}</dc:title>')
                c = c.replace('<dc:creator>python-docx</dc:creator>', '<dc:creator>Luciana Lumi Watanabe Yamanaka</dc:creator>')
                c = c.replace('<dc:description>generated by python-docx</dc:description>', '<dc:description>Versão 2 do manuscrito</dc:description>')
                c = re.sub(r'(<dcterms:created[^>]*>)[^<]*', r'\g<1>' + now, c)
                c = re.sub(r'(<dcterms:modified[^>]*>)[^<]*', r'\g<1>' + now, c)
                data = c.encode('utf-8')
            elif item.filename == '_rels/.rels':
                data = re.sub(r'<Relationship Id="rId2" Type="[^"]*thumbnail"[^>]*/>', '', data.decode('utf-8')).encode('utf-8')
            zout.writestr(item, data)
    print(f'{out.relative_to(ROOT)}: {count} capítulo(s), {midia.n} página(s) de destaque, {len(secoes)} seções')
    if missing:
        print('ainda não escritos:', ', '.join(map(str, missing)))


if __name__ == '__main__':
    main()
