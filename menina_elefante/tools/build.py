#!/usr/bin/env python3
"""Monta a V2 de A Menina Elefante em .docx usando os estilos do modelo (referencia/modelo_estilos.docx,
cópia do .docx de O Jardim).

Uso:
  python3 tools/build.py              -> saidas/A_Menina_Elefante_V2.docx (tudo o que já foi escrito, com folha de rosto)
  python3 tools/build.py --parte IV   -> saidas/A_Menina_Elefante_V2_Parte_IV.docx (só aquela parte, sem folha de rosto)

Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com "—";
"*" sozinho numa linha = quebra de cena; **TEXTO** = parágrafo em negrito (não usado neste livro).
Capítulos cujo arquivo ainda não existe são pulados (com aviso). Só usa a biblioteca padrão do Python.
"""
import datetime, json, re, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'referencia' / 'modelo_estilos.docx'
HEADER_MODELO = 'O JARDIM ENTRE O AGORA E O DEPOIS'
PB = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

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

def body_from_txt(path):
    txt = path.read_text(encoding='utf-8').strip()
    out, after_break = [], False
    for p in [p.strip() for p in re.split(r'\n\s*\n', txt) if p.strip()]:
        if p == '*':
            out.append(scene_break()); after_break = True; continue
        if p.startswith('**') and p.endswith('**'):
            out.append(para(p[2:-2], flush=True, bold=True)); after_break = False; continue
        flush = p.startswith('—') or after_break or len(p) <= 55 or p.endswith(':')
        out.append(para(p, flush)); after_break = False
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

def main():
    est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
    only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None
    zin = zipfile.ZipFile(TEMPLATE)
    doc = zin.read('word/document.xml').decode('utf-8')
    head = doc[:doc.index('<w:body>') + len('<w:body>')]
    sect = re.search(r'<w:sectPr\b.*?</w:sectPr>', doc, re.S).group(0)
    xml, count, missing = [], 0, []
    if not only:
        xml += front_matter(est, (ROOT / est['nota']).read_text(encoding='utf-8').strip())
        xml.append(title(est['prologo']['titulo'], before=1100))
        xml += body_from_txt(ROOT / est['prologo']['arquivo']); xml.append(PB)
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
            xml += body_from_txt(ROOT / c['arquivo']); xml.append(PB); count += 1
    ep = ROOT / est['epilogo']['arquivo']
    if not only and ep.exists():
        xml.append(title(est['epilogo']['titulo'], before=1100)); xml += body_from_txt(ep)
    while xml and xml[-1] == PB:
        xml.pop()
    name = f"A_Menina_Elefante_V2_Parte_{only}.docx" if only else 'A_Menina_Elefante_V2.docx'
    out = ROOT / 'saidas' / name
    out.parent.mkdir(exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    doc_title = est['titulo_doc'] + (f', Parte {only}' if only else '')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
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
            elif item.filename == '_rels/.rels':
                data = re.sub(r'<Relationship Id="rId2" Type="[^"]*thumbnail"[^>]*/>', '', data.decode('utf-8')).encode('utf-8')
            zout.writestr(item, data)
    print(f'{out.relative_to(ROOT)}: {count} capítulo(s)')
    if missing:
        print('ainda não escritos:', ', '.join(map(str, missing)))

if __name__ == '__main__':
    main()
