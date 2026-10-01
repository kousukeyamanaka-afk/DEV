#!/usr/bin/env python3
"""PDF de leitura do livro, com a mesma diagramação do .docx (5,5 × 8,5 pol., EB Garamond, vinhetas nas
aberturas de capítulo, "Para você", páginas de destaque), montado em HTML e impresso pelo Chromium.

  python3 tools/pdf.py   -> saidas/A_Menina_Elefante_V4.pdf

Diferenças em relação ao .docx: o número da página fica no pé, centralizado, e não há cabeçalho corrido
(o Chromium não sabe repetir o título do capítulo no alto da página). A hifenização é feita aqui mesmo,
por sílabas, com regras conservadoras do português (só separa em encontros de consoantes e nunca
entre vogais), porque o Chromium não hifeniza português.
Só usa a biblioteca padrão do Python.
"""
import base64, html, json, math, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import DIAG, VERSAO  # noqa: E402

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
FONTES = ROOT / 'referencia' / 'fontes'
ILU = ROOT / 'ilustracoes'

# ---------- hifenização ----------
VOGAIS = set('aeiouáéíóúâêôãõàüyAEIOUÁÉÍÓÚÂÊÔÃÕÀÜY')
INSEPARAVEIS = {'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'tr', 'vr', 'ch', 'lh', 'nh', 'qu', 'gu'}
SHY = '­'


def silabas_pontos(p):
    """Posições (índices) onde a palavra pode ser partida."""
    low = p.lower()
    n = len(low)
    vog = [c in VOGAIS for c in low]
    # 'u' depois de q (e de g, antes de e/i) funciona como consoante
    for i in range(1, n):
        if low[i] == 'u' and (low[i - 1] == 'q' or (low[i - 1] == 'g' and i + 1 < n and low[i + 1] in 'eiéíê')):
            vog[i] = False
    pontos = []
    i = 0
    while i < n and not vog[i]:
        i += 1
    while i < n:
        while i < n and vog[i]:
            i += 1
        j = i
        while j < n and not vog[j]:
            j += 1
        if j >= n:
            break
        grupo = low[i:j]
        k = len(grupo)
        if k == 1:
            corte = i
        elif k == 2:
            corte = i if grupo in INSEPARAVEIS else i + 1
        else:
            corte = j - 2 if grupo[-2:] in INSEPARAVEIS else j - 1
        pontos.append(corte)
        i = j
    return [c for c in pontos if c >= 2 and n - c >= 3]


def hifenizar(texto):
    def palavra(m):
        p = m.group(0)
        if len(p) < 6 or p.isupper():
            return p
        pts = silabas_pontos(p)
        for c in reversed(pts):
            p = p[:c] + SHY + p[c:]
        return p
    return re.sub(r"[A-Za-zÀ-ÿ]+", palavra, texto)


def t(x):
    return html.escape(hifenizar(x), quote=False)


def img64(png):
    return 'data:image/png;base64,' + base64.b64encode(png.read_bytes()).decode()


def fonte64(arq):
    return 'data:font/ttf;base64,' + base64.b64encode((FONTES / arq).read_bytes()).decode()


# ---------- corpo ----------
def pagina_destaque(d):
    png = ILU / f"destaque_{d['ornamento']}_{d['lado']}{'_azeitonas' if d.get('azeitonas') else ''}.png"
    limpo = d['frase'].replace('[[', '').replace(']]', '')
    larg_pt = (DIAG['pag_w'] - DIAG['margem_int'] - DIAG['margem_ext']) / 20
    pt = min(58, 0.93 * math.sqrt(larg_pt * 205 / (0.40 * len(limpo))))
    partes = [s for s in re.split(r'(\[\[|\]\])', d['frase'])]
    branco, frase = False, ''
    for s in partes:
        if s == '[[':
            branco = True; continue
        if s == ']]':
            branco = False; continue
        if s:
            frase += f'<span class="{"b" if branco else "c"}">{html.escape(s.upper())}</span>'
    alinh = 'right' if d['lado'] == 'esq' else 'left'
    autor = f'<p class="dautor" style="text-align:{alinh}">— {html.escape(d["autor"].upper())}</p>' if d.get('autor') else ''
    return (f'<section class="destaque" style="background-image:url({img64(png)})"><div class="dcaixa">'
            f'<p class="dfrase" style="font-size:{pt:.1f}pt;line-height:{pt * 1.02:.1f}pt;text-align:{alinh}">{frase}</p>'
            f'{autor}</div></section>')


def corpo_capitulo(path, destaques):
    paras = [p.strip() for p in re.split(r'\n\s*\n', path.read_text(encoding='utf-8').strip()) if p.strip()]
    out, pend, usados = [], [], set()
    primeiro, depois_quebra, reflexao, carta = True, False, False, False
    for p in paras:
        if p == '*':
            out += [pagina_destaque(d) for d in pend]; pend = []
            out.append('<p class="quebra">*&#8195;*&#8195;*</p>'); depois_quebra = True
            continue
        if p == '§':
            out.append(f'<div class="pv"><img class="ramo" src="{img64(ILU / "ramo_reflexao.png")}"><p class="rot">PARA VOCÊ</p></div>')
            reflexao = depois_quebra = True
            continue
        if p in ('[carta]', '[/carta]'):
            carta = p == '[carta]'
            continue
        if p.startswith('|'):
            linhas = ''.join(f'<tr><td class="esq">{t((l.strip().strip("|").split("|") + [""])[0].strip())}</td>'
                             f'<td>{t((l.strip().strip("|").split("|") + ["", ""])[1].strip())}</td></tr>' for l in p.splitlines())
            out.append(f'<table class="colunas">{linhas}</table>')
        elif carta:
            if p.startswith('~'):
                out.append(f'<p class="carta dir">{t(p[1:])}</p>')
            else:
                out.append(f'<p class="carta">{t(p)}</p>')
        elif reflexao:
            if p.startswith('? '):
                out.append(f'<p class="refl perg">{t(p[2:])}</p>')
            else:
                out.append(f'<p class="refl{" sem" if depois_quebra else ""}">{t(p)}</p>')
        elif p.startswith('^'):
            out.append(f'<p class="maior">{t(p[1:])}</p>')
        elif p.startswith('~'):
            out.append(f'<p class="dir"><i>{t(p[1:])}</i></p>')
        elif primeiro:
            m = re.match(r'^((?:\S+\s+){0,3}\S+)(.*)$', p, re.S)
            out.append(f'<p class="sem"><span class="vers">{html.escape(m.group(1))}</span>{t(m.group(2))}</p>')
        else:
            classe = ' class="sem"' if depois_quebra else ''
            out.append(f'<p{classe}>{t(p)}</p>')
        primeiro = depois_quebra = False
        novos = [d for d in destaques if d['ancora'] in p and id(d) not in usados]
        usados.update(id(d) for d in novos); pend += novos
    out += [pagina_destaque(d) for d in pend]
    return ''.join(out)


def abertura(rotulo, titulo, chave):
    v = ILU / f'vinheta_{chave}.png'
    vin = f'<img class="vinheta" src="{img64(v)}">' if v.exists() else '<div class="semvinheta"></div>'
    rot = f'<p class="rotulo">{html.escape(rotulo)}</p>' if rotulo else ''
    return f'<div class="abre">{vin}{rot}<h2>{html.escape(titulo)}</h2></div>'


def montar():
    est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
    dest = json.loads((ROOT / 'manuscrito' / 'destaques.json').read_text(encoding='utf-8'))['destaques']
    b = []
    b.append(f'<section class="limpa rosto"><h1>{html.escape(est["titulo_livro"])}</h1>'
             f'<p class="sub">{html.escape(est.get("subtitulo", ""))}</p>'
             f'<img class="vinheta-rosto" src="{img64(ILU / "vinheta_27.png")}">'
             f'<p class="autora">{html.escape(est["autora"])}</p></section>')
    nota = ''.join(f'<p>{t(x)}</p>' for x in re.split(r'\n\s*\n', (ROOT / est['nota']).read_text(encoding='utf-8').strip()) if x.strip())
    b.append(f'<section class="limpa nota"><p class="rotulo">NOTA AO LEITOR</p>{nota}</section>')
    # sumário
    linhas = [f'<li class="sp"><span>{html.escape(est["abertura"]["titulo"].capitalize())}</span></li>']
    for parte in est['partes']:
        linhas.append(f'<li class="sparte">{html.escape(parte["titulo"])}</li>')
        for c in parte['capitulos']:
            linhas.append(f'<li><span class="n">{c["n"]}</span><span>{html.escape(c["titulo"].capitalize())}</span></li>')
    linhas.append(f'<li class="sp"><span>{html.escape(est["epilogo"]["titulo"].split(" — ")[-1].capitalize())}</span></li>')
    b.append(f'<section class="limpa sumario"><p class="rotulo">SUMÁRIO</p><ul>{"".join(linhas)}</ul></section>')

    def cap(rotulo, titulo, arquivo, chave):
        b.append(f'<section class="cap">{abertura(rotulo, titulo, chave)}'
                 f'{corpo_capitulo(ROOT / arquivo, [d for d in dest if d["capitulo"] == chave])}</section>')

    cap('', est['abertura']['titulo'], est['abertura']['arquivo'], 'abertura')
    for parte in est['partes']:
        rot, tit = parte['titulo'].split(' — ', 1)
        b.append(f'<section class="limpa parte"><p class="prot">{html.escape(rot)}</p><h1>{html.escape(tit)}</h1>'
                 f'<p class="anos">{html.escape(parte.get("anos", ""))}</p></section>')
        for c in parte['capitulos']:
            cap(f"CAPÍTULO {c['n']} · {c['ano']}", c['titulo'], c['arquivo'], c['n'])
    ep = est['epilogo']
    rot, tit = ep['titulo'].split(' — ', 1)
    cap(f"{rot} · {ep['ano']}" if ep.get('ano') else rot, tit, ep['arquivo'], 'epilogo')
    apoio = ''.join(f'<p>{t(x)}</p>' for x in re.split(r'\n\s*\n', (ROOT / est['apoio']).read_text(encoding='utf-8').strip()) if x.strip())
    b.append(f'<section class="limpa apoio"><p class="rotulo">SE VOCÊ PRECISA DE AJUDA</p>{apoio}</section>')

    tw = 1 / 1440
    css = f'''
@font-face {{ font-family: 'EBG'; src: url({fonte64('EBGaramond-Regular.ttf')}); }}
@font-face {{ font-family: 'EBG'; font-style: italic; src: url({fonte64('EBGaramond-Italic.ttf')}); }}
@font-face {{ font-family: 'Bebas'; src: url({fonte64('BebasNeue-Regular.ttf')}); }}
@page {{ size: 5.5in 8.5in; margin: {DIAG['margem_sup'] * tw}in {DIAG['margem_ext'] * tw}in {DIAG['margem_inf'] * tw}in {DIAG['margem_int'] * tw}in;
        @bottom-center {{ content: counter(page); font-family: 'EBG'; font-size: 9pt; color: #555; }} }}
@page :left {{ margin-left: {DIAG['margem_ext'] * tw}in; margin-right: {DIAG['margem_int'] * tw}in; }}
@page :right {{ margin-left: {DIAG['margem_int'] * tw}in; margin-right: {DIAG['margem_ext'] * tw}in; }}
@page limpa {{ @bottom-center {{ content: none; }} }}
@page cheia {{ margin: 0; @bottom-center {{ content: none; }} }}
html {{ font-family: 'EBG', serif; font-size: {DIAG['corpo'] / 2}pt; line-height: {DIAG['entrelinha'] / 20}pt; color: #1d1d1b;
        font-kerning: normal; font-variant-ligatures: common-ligatures; }}
body {{ margin: 0; }}
p {{ margin: 0; text-indent: {DIAG['recuo'] * tw}in; text-align: justify; hyphens: manual; widows: 2; orphans: 2; }}
p.sem {{ text-indent: 0; }}
.vers {{ font-variant: small-caps; letter-spacing: .03em; }}
section {{ break-before: page; }}
section.limpa {{ page: limpa; }}
.rosto {{ text-align: center; padding-top: 1.2in; }}
.rosto h1 {{ font-weight: normal; font-size: 30pt; letter-spacing: .12em; line-height: 1.1; margin: 0; }}
.rosto .sub {{ text-indent: 0; text-align: center; font-style: italic; font-size: 12.5pt; line-height: 1.3; margin-top: .25in; }}
.vinheta-rosto {{ width: 1.9in; margin: .55in auto 0; display: block; }}
.rosto .autora {{ text-indent: 0; text-align: center; letter-spacing: .15em; font-size: 10.5pt; margin-top: .6in; }}
.rotulo {{ text-indent: 0; text-align: center; letter-spacing: .25em; font-size: 9.5pt; color: #555; line-height: 1.3; }}
.nota {{ padding-top: 1in; }} .nota .rotulo {{ margin-bottom: .35in; }}
.nota p:not(.rotulo), .apoio p:not(.rotulo) {{ text-indent: 0; text-align: center; font-style: italic; margin-bottom: .6em; }}
.apoio {{ padding-top: 1.4in; }} .apoio .rotulo {{ margin-bottom: .35in; }}
.sumario {{ padding-top: .5in; }} .sumario .rotulo {{ margin-bottom: .25in; }}
.sumario ul {{ list-style: none; padding: 0; margin: 0; font-size: 9.6pt; line-height: 13pt; }}
.sumario li {{ display: flex; gap: .6em; }}
.sumario li .n {{ width: 1.6em; text-align: right; color: #777; }}
.sumario li.sparte {{ margin-top: .7em; font-size: 8pt; letter-spacing: .14em; color: #555; }}
.sumario li.sp {{ margin-top: .5em; font-style: italic; }}
.parte {{ text-align: center; padding-top: 2.2in; }}
.parte .prot {{ text-indent: 0; text-align: center; letter-spacing: .3em; font-size: 11pt; color: #555; }}
.parte h1 {{ font-weight: normal; font-size: 20pt; letter-spacing: .08em; margin: .2in 0 0; line-height: 1.2; }}
.parte .anos {{ text-indent: 0; text-align: center; font-style: italic; color: #555; margin-top: .25in; }}
.abre {{ text-align: center; break-inside: avoid; }}
.vinheta {{ width: 2.1in; display: block; margin: .3in auto 0; }}
.semvinheta {{ height: 1.04in; }}
.abre .rotulo {{ margin-top: .11in; }}
.abre h2 {{ font-weight: normal; font-size: 17pt; letter-spacing: .05em; line-height: 1.2; margin: .11in 0 .53in; }}
.quebra {{ text-indent: 0; text-align: center; margin: .14in 0; break-after: avoid; }}
.pv {{ text-align: center; margin-top: .33in; break-after: avoid; break-inside: avoid; }}
.ramo {{ width: 1.35in; display: block; margin: 0 auto .04in; }}
.pv .rot {{ text-indent: 0; text-align: center; letter-spacing: .3em; font-size: 9pt; color: #555; margin-bottom: .17in; }}
p.refl {{ margin: 0 {340 * tw}in; text-indent: {300 * tw}in; font-size: {(DIAG['corpo'] - 1) / 2}pt; }}
p.refl.sem {{ text-indent: 0; }}
p.refl.perg {{ text-indent: 0; font-style: italic; margin-top: .14in; }}
p.carta {{ margin: 0 {500 * tw}in; text-indent: {300 * tw}in; font-style: italic; }}
p.carta.dir, p.dir {{ text-align: right; text-indent: 0; }}
p.maior {{ text-indent: 0; text-align: center; font-size: {(DIAG['corpo'] + 6) / 2}pt; margin: .11in 0 .14in; line-height: 1.4; }}
table.colunas {{ margin: .1in auto .12in; border-collapse: collapse; font-size: {(DIAG['corpo'] - 2) / 2}pt; line-height: 1.3; }}
table.colunas td {{ padding: 2pt 8pt; width: 50%; vertical-align: top; }}
table.colunas td.esq {{ text-align: right; text-decoration: line-through; color: #777; border-right: .5pt solid #777; }}
section.destaque {{ page: cheia; width: 5.5in; height: 8.5in; background-size: 100% 100%; position: relative; overflow: hidden; }}
.dcaixa {{ position: absolute; top: 1.32in; left: {DIAG['margem_int'] * tw}in; right: {DIAG['margem_ext'] * tw}in; }}
.dfrase {{ font-family: 'Bebas'; text-indent: 0; margin: 0; letter-spacing: .01em; }}
.dfrase .c {{ color: #A9A9A4; }} .dfrase .b {{ color: #FFFFFF; }}
.dautor {{ font-family: 'Bebas'; color: #A9A9A4; font-size: 13pt; letter-spacing: .15em; text-indent: 0; margin-top: .17in; }}
'''
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(est["titulo_livro"])}</title>'
            f'<style>{css}</style></head><body>{"".join(b)}</body></html>')


def main():
    out = ROOT / 'saidas' / f'A_Menina_Elefante_{VERSAO}.pdf'
    with tempfile.TemporaryDirectory() as tmp:
        h = Path(tmp) / 'livro.html'
        h.write_text(montar(), encoding='utf-8')
        subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={out}', f'file://{h}'], capture_output=True, timeout=600)
    pdf = out.read_bytes()
    print(out.relative_to(ROOT), '-', len(re.findall(rb'/Type\s*/Page[^s]', pdf)), 'páginas')


if __name__ == '__main__':
    main()
