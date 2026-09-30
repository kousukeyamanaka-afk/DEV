#!/usr/bin/env python3
"""Monta a V2 de A Menina Elefante em .docx usando os estilos do modelo (referencia/modelo_estilos.docx,
cópia do .docx de O Jardim).

Uso:
  python3 tools/build.py              -> saidas/A_Menina_Elefante_V2.docx (tudo o que já foi escrito, com folha de rosto)
  python3 tools/build.py --parte IV   -> saidas/A_Menina_Elefante_V2_Parte_IV.docx (só aquela parte, sem folha de rosto)

Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com "—";
"*" sozinho numa linha = quebra de cena; **TEXTO** = parágrafo em negrito (não usado neste livro).
Páginas de destaque: manuscrito/destaques.json lista as frases que ganham uma página inteira (fundo escuro,
ornamento de ilustracoes/, letra grande em Bebas Neue, embutida no .docx a partir de referencia/fontes/).
Gere os fundos antes com tools/ornamentos.py.
Capítulos cujo arquivo ainda não existe são pulados (com aviso). Só usa a biblioteca padrão do Python.
"""
import datetime, json, math, re, sys, uuid, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'referencia' / 'modelo_estilos.docx'
HEADER_MODELO = 'O JARDIM ENTRE O AGORA E O DEPOIS'
PB = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
FONTE = ROOT / 'referencia' / 'fontes' / 'BebasNeue-Regular.ttf'
FONTE_NOME = 'Bebas Neue'
EMU = 914400
NS_PIC = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"',
          'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


class Midia:
    """Imagens usadas no documento (uma relação por arquivo)."""
    def __init__(self):
        self.arquivos, self.n_desenho = {}, 0

    def rid(self, path):
        if path not in self.arquivos:
            self.arquivos[path] = f'rIdImg{len(self.arquivos) + 1}'
        return self.arquivos[path]

    def novo_id(self):
        self.n_desenho += 1
        return 1000 + self.n_desenho


def fundo_pagina(midia, png, pg_w, pg_h):
    """Imagem ancorada na página inteira, atrás do texto."""
    cx, cy = pg_w * EMU // 1440, pg_h * EMU // 1440
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


def pagina_destaque(d, midia, pg_w, pg_h, larg_texto):
    """Página inteira: fundo escuro com ornamento, frase grande em caixa-alta, [[...]] em branco."""
    png = ROOT / 'ilustracoes' / f"destaque_{d['ornamento']}_{d['lado']}.png"
    if not png.exists():
        sys.exit(f'falta {png.relative_to(ROOT)}: rode python3 tools/ornamentos.py')
    jc = 'right' if d['lado'] == 'esq' else 'left'
    limpo = d['frase'].replace('[[', '').replace(']]', '')
    # tamanho: o bloco de texto deve caber na metade de cima da página
    larg_pt = larg_texto / 20
    pt = min(58, 0.93 * math.sqrt(larg_pt * 230 / (0.40 * len(limpo))))
    sz = int(pt) * 2
    def r(txt, cor):
        return (f'<w:r><w:rPr><w:rFonts w:ascii="{FONTE_NOME}" w:hAnsi="{FONTE_NOME}" w:cs="{FONTE_NOME}"/><w:caps/>'
                f'<w:color w:val="{cor}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape(txt.upper())}</w:t></w:r>')
    runs = ''.join(r(s, 'FFFFFF' if k % 2 else 'A9A9A4') for k, s in enumerate(re.split(r'\[\[|\]\]', d['frase'])) if s)
    out = [f'<w:p><w:pPr><w:pageBreakBefore/><w:spacing w:before="0" w:after="0"/><w:ind w:firstLine="0"/></w:pPr>'
           f'{fundo_pagina(midia, png, pg_w, pg_h)}</w:p>',
           f'<w:p><w:pPr><w:spacing w:before="900" w:after="0" w:line="{int(pt * 20 * 1.02)}" w:lineRule="exact"/>'
           f'<w:ind w:firstLine="0"/><w:jc w:val="{jc}"/></w:pPr>{runs}</w:p>']
    if d.get('autor'):
        out.append(f'<w:p><w:pPr><w:spacing w:before="240" w:after="0"/><w:ind w:firstLine="0"/><w:jc w:val="{jc}"/></w:pPr>'
                   f'<w:r><w:rPr><w:rFonts w:ascii="{FONTE_NOME}" w:hAnsi="{FONTE_NOME}"/><w:caps/><w:color w:val="A9A9A4"/>'
                   f'<w:spacing w:val="30"/><w:sz w:val="26"/></w:rPr><w:t xml:space="preserve">— {escape(d["autor"].upper())}</w:t></w:r></w:p>')
    out.append(PB)
    return out

def run(t, bold=False):
    rpr = '<w:rPr><w:b/></w:rPr>' if bold else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'

def para(t, flush=False, bold=False):
    ppr = '<w:pPr><w:ind w:firstLine="0"/></w:pPr>' if flush else ''
    return f'<w:p>{ppr}{run(t, bold)}</w:p>'

def scene_break():
    return ('<w:p><w:pPr><w:spacing w:before="240" w:after="240"/><w:ind w:firstLine="0"/>'
            '<w:jc w:val="center"/></w:pPr>' + run('*') + '</w:p>')

def title(t, style='MyChapterTitle', before=1440, after=560):
    sp = f'<w:spacing w:before="{before}" w:after="{after}"/>' if after is not None else f'<w:spacing w:before="{before}"/>'
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{sp}</w:pPr>{run(t)}</w:p>'

def body_from_txt(path, destaques=(), pagina=None):
    """destaques: frases deste capítulo; cada página entra na próxima quebra de cena depois da âncora,
    ou no fim do capítulo. pagina: função que monta a página de destaque."""
    txt = path.read_text(encoding='utf-8').strip()
    out, after_break, pendentes = [], False, []
    paras = [p.strip() for p in re.split(r'\n\s*\n', txt) if p.strip()]
    for d in destaques:
        if not any(d['ancora'] in p for p in paras):
            sys.exit(f"âncora não encontrada em {path.name}: {d['ancora']}")
    for p in paras:
        if p == '*':
            for d in pendentes:
                out += pagina(d)
            pendentes = []
            out.append(scene_break()); after_break = True; continue
        if p.startswith('**') and p.endswith('**'):
            out.append(para(p[2:-2], flush=True, bold=True)); after_break = False; continue
        flush = p.startswith('—') or after_break or len(p) <= 55 or p.endswith(':')
        out.append(para(p, flush)); after_break = False
        pendentes += [d for d in destaques if d['ancora'] in p]
    for d in pendentes:
        out += pagina(d)
    while out and out[-1] == PB:
        out.pop()
    return out

def centered(t, size=24, before=0, italic=False, bold=False):
    rpr = '<w:rFonts w:ascii="EB Garamond" w:hAnsi="EB Garamond"/>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + f'<w:sz w:val="{size}"/>'
    sp = f'<w:spacing w:before="{before}"/>' if before else ''
    return f'<w:p><w:pPr>{sp}<w:jc w:val="center"/></w:pPr><w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r></w:p>'

def front_matter(est, nota_text):
    out = [f'<w:p><w:pPr><w:pStyle w:val="MyBookTitle"/><w:spacing w:before="2300"/></w:pPr>{run(est["titulo_livro"])}</w:p>']
    if est.get('subtitulo'):
        out.append(f'<w:p><w:pPr><w:pStyle w:val="MyBookSubtitle"/><w:spacing w:before="280"/></w:pPr>{run(est["subtitulo"])}</w:p>')
    out.append(f'<w:p><w:pPr><w:pStyle w:val="MyBookSubtitle"/><w:spacing w:before="2400"/></w:pPr>{run(est["autora"], bold=True)}</w:p>')
    out.append(PB)
    if est.get('dedicatoria'):
        out += [centered('DEDICATÓRIA', 28, 1700, bold=True), centered(est['dedicatoria'], 26, 600, italic=True), PB]
    out.append(title('NOTA AO LEITOR', before=1100))
    out += [para(p) for p in re.split(r'\n\s*\n', nota_text) if p.strip()]
    out.append(PB)
    return out

def ofuscar(fonte, chave):
    """Ofuscação de fonte embutida (ECMA-376, 17.8.1): XOR dos 32 primeiros bytes com a chave GUID invertida."""
    k = bytes.fromhex(chave.strip('{}').replace('-', ''))[::-1]
    b = bytearray(fonte)
    for i in range(32):
        b[i] ^= k[i % 16]
    return bytes(b)


def main():
    est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
    only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None
    zin = zipfile.ZipFile(TEMPLATE)
    doc = zin.read('word/document.xml').decode('utf-8')
    head = doc[:doc.index('<w:body>') + len('<w:body>')]
    sect = re.search(r'<w:sectPr\b.*?</w:sectPr>', doc, re.S).group(0)
    pg_w, pg_h = (int(v) for v in re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"', sect).groups())
    m_dir, m_esq = (int(v) for v in re.search(r'w:right="(\d+)"[^>]*w:left="(\d+)"', sect).groups())
    midia = Midia()
    arq_dest = ROOT / 'manuscrito' / 'destaques.json'
    todos = json.loads(arq_dest.read_text(encoding='utf-8'))['destaques'] if arq_dest.exists() else []
    def dest(cap):
        return [d for d in todos if d['capitulo'] == cap]
    def pagina(d):
        return pagina_destaque(d, midia, pg_w, pg_h, pg_w - m_dir - m_esq)
    xml, count, missing = [], 0, []
    if not only:
        xml += front_matter(est, (ROOT / est['nota']).read_text(encoding='utf-8').strip())
        xml.append(title(est['prologo']['titulo'], before=1100))
        xml += body_from_txt(ROOT / est['prologo']['arquivo'], dest('prologo'), pagina); xml.append(PB)
    for parte in est['partes']:
        if only and parte['numero'] != only:
            continue
        caps = [c for c in parte['capitulos'] if (ROOT / c['arquivo']).exists()]
        missing += [c['n'] for c in parte['capitulos'] if not (ROOT / c['arquivo']).exists()]
        if not caps:
            continue
        xml.append(title(parte['titulo'], style='MyPartTitle', before=2400, after=None)); xml.append(PB)
        for c in caps:
            xml.append(title(f"CAPÍTULO {c['n']} — {c['titulo']}"))
            xml += body_from_txt(ROOT / c['arquivo'], dest(c['n']), pagina); xml.append(PB); count += 1
    ep = ROOT / est['epilogo']['arquivo']
    if not only and ep.exists():
        xml.append(title(est['epilogo']['titulo'], before=1100)); xml += body_from_txt(ep, dest('epilogo'), pagina)
    while xml and xml[-1] == PB:
        xml.pop()
    name = f"A_Menina_Elefante_V2_Parte_{only}.docx" if only else 'A_Menina_Elefante_V2.docx'
    out = ROOT / 'saidas' / name
    out.parent.mkdir(exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    doc_title = est['titulo_doc'] + (f', Parte {only}' if only else '')
    chave = '{' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'menina-elefante/bebas-neue')).upper() + '}'
    embutir = FONTE.exists() and bool(midia.arquivos)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for png, rid in midia.arquivos.items():
            zout.writestr(f'word/media/{png.name}', png.read_bytes())
        if embutir:
            zout.writestr('word/fonts/font1.odttf', ofuscar(FONTE.read_bytes(), chave))
            zout.writestr('word/_rels/fontTable.xml.rels',
                          '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                          '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                          '<Relationship Id="rIdF1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" '
                          'Target="fonts/font1.odttf"/></Relationships>')
        for item in zin.infolist():
            if item.filename == 'docProps/thumbnail.jpeg':
                continue
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                data = (head + ''.join(xml) + sect + '</w:body></w:document>').encode('utf-8')
            elif item.filename == 'word/header1.xml':
                data = data.decode('utf-8').replace(HEADER_MODELO, escape(est['titulo_livro'])).encode('utf-8')
            elif item.filename == 'docProps/core.xml':
                c = data.decode('utf-8')
                c = c.replace('<dc:title/>', f'<dc:title>{escape(doc_title)}</dc:title>')
                c = c.replace('<dc:creator>python-docx</dc:creator>', '<dc:creator>Luciana Lumi Watanabe Yamanaka</dc:creator>')
                c = c.replace('<dc:description>generated by python-docx</dc:description>', '<dc:description>Versão 2 do manuscrito</dc:description>')
                c = re.sub(r'(<dcterms:created[^>]*>)[^<]*', r'\g<1>' + now, c)
                c = re.sub(r'(<dcterms:modified[^>]*>)[^<]*', r'\g<1>' + now, c)
                data = c.encode('utf-8')
            elif item.filename == 'word/_rels/document.xml.rels':
                rels = ''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                               f'Target="media/{png.name}"/>' for png, rid in midia.arquivos.items())
                data = data.decode('utf-8').replace('</Relationships>', rels + '</Relationships>').encode('utf-8')
            elif item.filename == '[Content_Types].xml':
                c = data.decode('utf-8').replace('<Default Extension="rels"', '<Default Extension="png" ContentType="image/png"/>'
                                                 '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/>'
                                                 '<Default Extension="rels"')
                data = c.encode('utf-8')
            elif item.filename == 'word/fontTable.xml' and embutir:
                f = (f'<w:font w:name="{FONTE_NOME}"><w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
                     f'<w:embedRegular r:id="rIdF1" w:fontKey="{chave}"/></w:font>')
                data = data.decode('utf-8').replace('</w:fonts>', f + '</w:fonts>').encode('utf-8')
            elif item.filename == 'word/settings.xml' and embutir:
                data = re.sub(r'(<w:zoom [^>]*/>)', r'\1<w:embedTrueTypeFonts/>', data.decode('utf-8'), count=1).encode('utf-8')
            elif item.filename == '_rels/.rels':
                data = re.sub(r'<Relationship Id="rId2" Type="[^"]*thumbnail"[^>]*/>', '', data.decode('utf-8')).encode('utf-8')
            zout.writestr(item, data)
    print(f'{out.relative_to(ROOT)}: {count} capítulo(s), {midia.n_desenho} página(s) de destaque')
    if missing:
        print('ainda não escritos:', ', '.join(map(str, missing)))

if __name__ == '__main__':
    main()
