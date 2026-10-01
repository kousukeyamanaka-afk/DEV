#!/usr/bin/env python3
"""Monta o manuscrito V2 em .docx usando os estilos do V1 (referencia/O_Jardim_V1.docx).

Uso:
  python3 tools/build.py              -> saidas/O_Jardim_V2.docx (tudo o que já foi escrito, com folha de rosto)
  python3 tools/build.py --parte IV   -> saidas/O_Jardim_V2_Parte_IV.docx (só aquela parte, sem folha de rosto)

Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com "—";
"*" sozinho numa linha = quebra de cena; **TEXTO** = parágrafo em negrito (só as placas do cap. 10).
Capítulos cujo arquivo ainda não existe são pulados (com aviso). Só usa a biblioteca padrão do Python.
"""
import datetime, json, re, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'referencia' / 'O_Jardim_V1.docx'
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

def front_matter(doc_xml, nota_text):
    body = doc_xml[doc_xml.index('<w:body>') + 8:]
    cut = body.index('PRÓLOGO — A CASA ACESA')
    cut = max(body.rfind('<w:p>', 0, cut), body.rfind('<w:p ', 0, cut))
    out, in_nota = [], False
    for p in re.findall(r'<w:p\b.*?</w:p>', body[:cut], re.S):
        t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
        if t.startswith('Conceito central'):
            continue  # o conceito é nomeado uma única vez, pela Maya, no cap. 23
        if t == 'NOTA AO LEITOR':
            in_nota = True; out.append(p); continue
        if in_nota and t.startswith('Esta é uma obra de ficção'):
            out.append(para(nota_text)); in_nota = False; continue
        out.append(p)
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
        xml += front_matter(doc, (ROOT / est['nota']).read_text(encoding='utf-8').strip())
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
    notas = ROOT / est['notas']['arquivo'] if 'notas' in est else None
    if not only and notas and notas.exists():
        xml.append(PB); xml.append(title(est['notas']['titulo'], before=1100)); xml += body_from_txt(notas)
    while xml and xml[-1] == PB:
        xml.pop()
    name = f"O_Jardim_V2_Parte_{only}.docx" if only else 'O_Jardim_V2.docx'
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
            elif item.filename == 'docProps/core.xml':
                c = data.decode('utf-8')
                c = c.replace('<dc:title/>', f'<dc:title>{escape(doc_title)}</dc:title>')
                c = c.replace('<dc:creator>python-docx</dc:creator>', '<dc:creator>Alan Yamanaka</dc:creator>')
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
