#!/usr/bin/env python3
"""Confere cada capítulo escrito contra as metas do guia de estilo.

Uso: python3 tools/metricas.py [--parte IV]
Metas: 1.300–1.800 palavras nas Partes IV e V; parágrafos narrativos de até 6 palavras <= 25%;
nenhuma lista vertical (3+ linhas curtas seguidas); 'perceb*' no máximo 1 por capítulo;
última linha: imagem, ação ou fala — nunca uma moral (conferir a olho).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
est = json.loads((ROOT / 'manuscrito' / 'estrutura.json').read_text(encoding='utf-8'))
only = sys.argv[sys.argv.index('--parte') + 1].upper() if '--parte' in sys.argv else None
total = 0
for parte in est['partes']:
    if only and parte['numero'] != only:
        continue
    for c in parte['capitulos']:
        f = ROOT / c['arquivo']
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
        perc = sum(len(re.findall(r'perceb', p.lower())) for p in paras)
        pct = short / len(narr) * 100 if narr else 0
        flags = []
        if pct > 25: flags.append('muitos parágrafos curtos')
        if runs: flags.append('lista vertical')
        if perc > 1: flags.append('perceber demais')
        print(f"cap {c['n']:>2} {c['titulo'][:32]:32} {words:5d} palavras | curtos {pct:3.0f}% | listas {runs} | perceb {perc}"
              + (f"  <- {', '.join(flags)}" if flags else ''))
        print(f"        última linha: {paras[-1][:110]}")
print(f'total: {total} palavras')
