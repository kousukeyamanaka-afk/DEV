#!/usr/bin/env python3
"""Confere cada capítulo escrito contra as metas do guia de estilo (docs/ESTILO.md).

Uso: python3 tools/metricas.py [--parte I]
Metas: 1.000–1.500 palavras por capítulo nas Partes I–V (1.000–1.400 na VI; prólogo ~900; epílogo ~500);
parágrafos narrativos de até 6 palavras <= 25%; nenhuma lista vertical (3+ linhas curtas seguidas);
reticências <= 2; 'perceb*', 'dar conta', 'mais uma vez', 'hoje eu' <= 1 cada;
'menina elefante' só no cap. 26; última linha: imagem, gesto ou fala — nunca uma lição (conferir a olho).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None

itens = []
if not only:
    itens.append(('pról', est['prologo']['titulo'].split('— ')[-1], est['prologo']['arquivo'], None))
for parte in est['partes']:
    if only and parte['numero'] != only:
        continue
    for c in parte['capitulos']:
        itens.append((str(c['n']), c['titulo'], c['arquivo'], c['n']))
if not only:
    itens.append(('epíl', 'EPÍLOGO', est['epilogo']['arquivo'], None))

GASTAS = {'perceb': r'perceb', 'dar conta': r'\bd(ar|ou|ei|ava|ando|ou) conta\b', 'mais uma vez': r'mais uma vez', 'hoje eu': r'\bhoje eu\b'}
total = 0
for rot, titulo, arq, n in itens:
    f = ROOT / arq
    if not f.exists():
        continue
    paras = [p.strip() for p in re.split(r'\n\s*\n', f.read_text(encoding='utf-8')) if p.strip()]
    narr = [p for p in paras if p != '*' and not p.startswith('—') and not p.startswith('**')]
    short = sum(1 for p in narr if len(p.split()) <= 6)
    runs = cur = 0
    for p in paras:
        if p != '*' and not p.startswith(('—', '**')) and len(p.split()) <= 3:
            cur += 1
        else:
            runs += cur >= 3; cur = 0
    runs += cur >= 3
    words = sum(len(p.split()) for p in paras if p != '*')
    total += words
    low = '\n'.join(paras).lower()
    retic = sum(p.count('…') + p.count('...') for p in narr)
    pct = short / len(narr) * 100 if narr else 0
    flags = []
    if pct > 25: flags.append('muitos parágrafos curtos')
    if runs: flags.append('lista vertical')
    if retic > 2: flags.append('reticências')
    for nome, rx in GASTAS.items():
        if len(re.findall(rx, low)) > 1: flags.append(nome)
    if 'menina elefante' in low and n != 26: flags.append('"menina elefante" fora do cap. 26')
    print(f"{rot:>4} {titulo[:30]:30} {words:5d} palavras | curtos {pct:3.0f}% | listas {runs} | retic {retic}"
          + (f"  <- {', '.join(flags)}" if flags else ''))
    print(f"        última linha: {paras[-1][:110]}")
print(f'total: {total} palavras')
