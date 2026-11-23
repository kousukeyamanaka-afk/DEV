#!/usr/bin/env python3
"""Gera um 工事・サービス契約書 (EASY HOUSE) a partir do modelo e de um arquivo JSON.

Uso:
    python3 gerar_contrato.py dados.json [saida.docx]

Só usa a biblioteca padrão do Python. Veja README.md para os campos do JSON.
"""
import json, re, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).resolve().parent
MODELO = AQUI / "modelo" / "工事・サービス契約書_簡易版_ひな形.docx"
FIM_PAGINA1 = '<w:br w:type="page"/>'


# ---------- utilidades de XML ----------
def run(texto, sz=16, negrito=False, cor="111111"):
    sz = max(sz, 16)  # mínimo de 8 pontos
    b = "<w:b/>" if negrito else ""
    return (f'<w:r><w:rPr>{b}<w:color w:val="{cor}"/><w:sz w:val="{sz}"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(texto)}</w:t></w:r>')


def para(texto, sz=16, negrito=False, alinh=None, cor="111111"):
    linha = max(sz, 16) * 12
    jc = f'<w:jc w:val="{alinh}"/>' if alinh else ""
    return (f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="{linha}" w:lineRule="exact"/>{jc}</w:pPr>'
            f'{run(texto, sz, negrito, cor)}</w:p>')


def texto_celula(xml):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))


def yen(v):
    return f"￥{v:,}" if isinstance(v, int) else str(v)


def data_jp(s):
    if not s:
        return None
    a, m, d = (int(x) for x in s.split("-"))
    return f"{a}年　{m}月　{d}日"


class Doc:
    def __init__(self, xml):
        self.xml = xml

    def celulas(self):
        fim = self.xml.find(FIM_PAGINA1)
        return [(m.start(), m.end()) for m in re.finditer(r"<w:tc>.*?</w:tc>", self.xml[:fim], re.S)]

    def indice(self, rotulo):
        for i, (s, e) in enumerate(self.celulas()):
            if texto_celula(self.xml[s:e]) == rotulo:
                return i
        raise KeyError(rotulo)

    def texto(self, i):
        s, e = self.celulas()[i]
        return texto_celula(self.xml[s:e])

    def preencher(self, i, paragrafos):
        s, e = self.celulas()[i]
        c = self.xml[s:e]
        k = c.find("</w:tcPr>") + len("</w:tcPr>")
        self.xml = self.xml[:s] + c[:k] + "".join(paragrafos) + "</w:tc>" + self.xml[e:]

    def marcar(self, i, opcoes, extra=None):
        """Troca □opção por ■opção dentro da célula i."""
        s, e = self.celulas()[i]
        c = self.xml[s:e]
        for o in opcoes:
            novo = re.sub(r"□(\s?)" + re.escape(o), r"■\g<1>" + o, c, count=1)
            if novo == c:
                raise ValueError(f"opção não encontrada: {o}")
            c = novo
        if extra:
            c = c.replace("期間：", "期間：" + escape(extra), 1)
        self.xml = self.xml[:s] + c + self.xml[e:]

    def valor_de(self, rotulo, paragrafos):
        self.preencher(self.indice(rotulo) + 1, paragrafos)

    def ajustar_linhas_itens(self, n):
        fim = self.xml.find(FIM_PAGINA1)
        h = self.xml.find(">品名・作業項目<")
        trs = [m.start() for m in re.finditer(r"<w:tr[ >]", self.xml[:fim]) if m.start() > h]
        # trs[0] = 1ª linha de item ... trs[3] = linha do 小計
        linha = self.xml[trs[0]:trs[1]]
        linha = re.sub(r' w14:(paraId|textId)="[0-9A-F]+"', "", linha)
        existentes = 3
        if n > existentes:
            self.xml = self.xml[:trs[1]] + linha * (n - existentes) + self.xml[trs[1]:]


def gerar(dados, saida):
    with zipfile.ZipFile(MODELO) as z:
        arquivos = {n: z.read(n) for n in z.namelist()}
    doc = Doc(arquivos["word/document.xml"].decode("utf8"))

    # ---- cabeçalho
    c = dados.get("contrato", {})
    if c.get("numero"):
        doc.valor_de("契約番号", [para(c["numero"])])
    if c.get("data"):
        doc.valor_de("契約年月日", [para(data_jp(c["data"]), alinh="center")])
    if c.get("responsavel"):
        doc.valor_de("担当者", [para(c["responsavel"])])

    # ---- cliente
    cli = dados["cliente"]
    doc.valor_de("フリガナ", [para(cli.get("furigana", ""))])
    doc.valor_de("氏名", [para(cli["nome"], 18, True)])
    end = ("〒" + cli["cep"] + "　" if cli.get("cep") else "〒　") + cli.get("endereco", "")
    doc.valor_de("住所", [para(end)])
    doc.valor_de("TEL", [para(cli.get("tel", ""))])
    lo = dados.get("local_obra", {})
    if lo.get("mesmo_endereco"):
        txt = "■ ご契約者住所と同じ　□ 別住所："
    else:
        txt = "□ ご契約者住所と同じ　■ 別住所：" + lo.get("endereco", "")
    doc.valor_de("施工場所", [para(txt)])

    # ---- valores
    total = int(dados["valor_total_com_imposto"])
    sem_imposto = (total * 10 + 5) // 11
    imposto = total - sem_imposto
    doc.valor_de("契約金額（税込）", [para(yen(total), 19, True)])
    doc.valor_de("うち消費税", [para(yen(imposto))])
    pg = dados.get("pagamento", {})
    if pg.get("metodo"):
        doc.marcar(doc.indice("支払方法") + 1, pg["metodo"])
    if pg.get("condicao"):
        doc.marcar(doc.indice("支払条件") + 1, pg["condicao"])
    if pg.get("vencimento"):
        doc.valor_de("支払期日", [para(data_jp(pg["vencimento"]), alinh="center")])
    ga = dados.get("garantia", {})
    if ga.get("tipo") or ga.get("periodo"):
        doc.marcar(doc.indice("保証") + 1, ga.get("tipo", []), ga.get("periodo"))

    # ---- obra
    ob = dados["obra"]
    doc.valor_de("工事・サービス名", [para(ob["nome"])])
    doc.valor_de("内容・仕様", [para(t) for t in ob.get("especificacao", [])] or [para("")])
    if ob.get("inicio"):
        doc.valor_de("着工予定日", [para(data_jp(ob["inicio"]), alinh="center")])
    if ob.get("entrega"):
        doc.valor_de("完了・引渡し予定日", [para(data_jp(ob["entrega"]), alinh="center")])

    # ---- itens
    itens = dados.get("itens", [])
    doc.ajustar_linhas_itens(len(itens))
    base = doc.indice("品名・作業項目") + 5
    soma = 0
    for r, it in enumerate(itens):
        valor = it.get("valor", "")
        if isinstance(valor, int):
            soma += valor
        cols = [it.get("nome", ""), it.get("spec", ""), it.get("qtd", "1式"),
                yen(it.get("unitario", valor)), yen(valor)]
        for k, v in enumerate(cols):
            al = None if k < 2 else ("center" if k == 2 else "right")
            doc.preencher(base + 5 * r + k, [para(v, alinh=al)])
    if itens and soma != total:
        print(f"AVISO: soma dos itens ({soma:,}) diferente do total ({total:,})", file=sys.stderr)
    doc.valor_de("小計（税抜）", [para(yen(sem_imposto))])
    doc.valor_de("消費税", [para(yen(imposto))])
    doc.valor_de("合計（税込）", [para(yen(total), 17, True)])

    # ---- observações (备考): substitui as linhas pautadas
    obs = dados.get("observacoes", [])
    pad = re.compile(r'(<w:p(?: [^>]*)?><w:pPr><w:pBdr>.*?</w:pPr><w:r><w:rPr>.*?</w:rPr><w:t xml:space="preserve">)(　+)(</w:t></w:r></w:p>)', re.S)
    linhas = list(pad.finditer(doc.xml))
    if obs and linhas:
        modelo = linhas[0]
        novos = "".join(modelo.group(1) + escape(t) + modelo.group(3) for t in obs)
        doc.xml = doc.xml[:linhas[0].start()] + novos + doc.xml[linhas[-1].end():]

    arquivos["word/document.xml"] = doc.xml.encode("utf8")
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in arquivos.items():
            z.writestr(n, b)
    print(f"Contrato gerado: {saida}")
    print(f"Total ￥{total:,} = sem imposto ￥{sem_imposto:,} + imposto ￥{imposto:,}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    entrada = Path(sys.argv[1])
    dados = json.loads(entrada.read_text(encoding="utf8"))
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else entrada.with_suffix(".docx")
    gerar(dados, saida)
