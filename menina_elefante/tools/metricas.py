#!/usr/bin/env python3
"""Confere cada capítulo escrito contra as metas do guia de estilo (docs/ESTILO.md).

Uso: python3 tools/metricas.py [--parte I]
A cena (antes do '§') e o 'Para você' (depois do '§') são medidos separadamente.
Metas da cena: parágrafos narrativos de até 6 palavras <= 25%; nenhuma lista vertical (3+ linhas curtas seguidas);
reticências <= 2; 'perceb*', 'dar conta', 'mais uma vez', 'hoje eu' <= 1 cada; última linha da cena: imagem, gesto
ou fala, nunca uma lição (conferir a olho). 'Para você': 100–220 palavras, terminando numa pergunta ('? ').
'menina elefante' não aparece antes do cap. 27, onde a imagem nasce.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None

itens = []
if not only:
    itens.append(('abre', est['abertura']['titulo'], est['abertura']['arquivo'], 0))
for parte in est['partes']:
    if only and parte['numero'] != only:
        continue
    for c in parte['capitulos']:
        itens.append((str(c['n']), c['titulo'], c['arquivo'], c['n']))
if not only:
    itens.append(('epíl', 'EPÍLOGO', est['epilogo']['arquivo'], 99))

MARCAS = ('*', '§', '[carta]', '[/carta]')
GASTAS = {'perceb': r'perceb', 'dar conta': r'\bd(ar|ou|ei|ava|ando|ou) conta\b', 'mais uma vez': r'mais uma vez', 'hoje eu': r'\bhoje eu\b'}
total = 0
for rot, titulo, arq, n in itens:
    f = ROOT / arq
    if not f.exists():
        continue
    todos = [p.strip() for p in re.split(r'\n\s*\n', f.read_text(encoding='utf-8')) if p.strip()]
    corte = todos.index('§') if '§' in todos else len(todos)
    paras, refl = todos[:corte], todos[corte + 1:]
    narr = [p for p in paras if p not in MARCAS and not p.startswith(('—', '|', '~'))]
    short = sum(1 for p in narr if len(p.split()) <= 6)
    runs = cur = 0
    for p in paras:
        if p not in MARCAS and not p.startswith(('—', '|', '~')) and len(p.split()) <= 3:
            cur += 1
        else:
            runs += cur >= 3; cur = 0
    runs += cur >= 3
    cena = sum(len(p.split()) for p in paras if p not in MARCAS)
    pv = sum(len(p.lstrip('? ').split()) for p in refl)
    total += cena + pv
    low = '\n'.join(p for p in paras if not p.startswith('|')).lower()
    retic = sum(p.count('…') + p.count('...') for p in narr)
    pct = short / len(narr) * 100 if narr else 0
    flags = []
    if pct > 25: flags.append('muitos parágrafos curtos')
    if runs: flags.append('lista vertical')
    if retic > 2: flags.append('reticências')
    for nome, rx in GASTAS.items():
        if len(re.findall(rx, low)) > 1: flags.append(nome)
    if 'menina elefante' in '\n'.join(todos).lower() and 0 < n < 27: flags.append('"menina elefante" antes do cap. 27')
    if n and n != 99 and not refl: flags.append('sem "Para você"')
    if refl and not refl[-1].startswith('? '): flags.append('"Para você" não termina em pergunta')
    if refl and not 100 <= pv <= 260: flags.append(f'"Para você" com {pv} palavras')
    ultima = [p for p in paras if p not in MARCAS][-1]
    print(f"{rot:>4} {titulo[:28]:28} cena {cena:5d} + para você {pv:3d} | curtos {pct:3.0f}% | listas {runs} | retic {retic}"
          + (f"  <- {', '.join(flags)}" if flags else ''))
    print(f"        fim da cena: {ultima[:100]}")
print(f'total: {total} palavras')
