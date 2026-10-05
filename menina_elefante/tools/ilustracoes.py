#!/usr/bin/env python3
"""Vinhetas em traço, uma por capítulo (mais abertura e epílogo), para as aberturas de capítulo.

Cada desenho é um SVG simples (traço contínuo verde-oliva escuro, com uma aguada clara em
alguns pontos), renderizado em PNG transparente pelo Chromium instalado no ambiente.
Uso: python3 tools/ilustracoes.py   → gera ilustracoes/vinheta_<chave>.png
"""
import subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'ilustracoes'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
TINTA = '#34402a'
AGUADA = '#d9dcc0'
FOLHA = '#7c8a4c'

def folhinha(x, y, ang, esc=1.0):
    """Uma folha de oliveira pequena, para assinar cada vinheta."""
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({esc})">'
            f'<path d="M0 0 C 10 -8, 30 -8, 42 0 C 30 8, 10 8, 0 0 Z" fill="{FOLHA}" stroke="none" opacity=".85"/>'
            f'<path d="M2 0 L 38 0" stroke="#5d6b38" stroke-width="1.5"/></g>')

def raminho(x, y, ang=0):
    return (f'<g transform="translate({x} {y}) rotate({ang})">'
            f'<path d="M0 0 C 20 -4, 45 -4, 70 -14" stroke="{TINTA}" stroke-width="2.5"/>'
            + folhinha(18, -3, -35, .55) + folhinha(30, -5, 30, .55) + folhinha(46, -8, -40, .55) + folhinha(58, -10, 25, .5)
            + '</g>')

def chao(x1=90, x2=310, y=262):
    return f'<path d="M{x1} {y} Q 200 {y-6} {x2} {y}" stroke-width="2.5"/>'

D = {}

D['abertura'] = f'''
<path d="M200 95 C 160 80, 110 80, 80 92 L 80 232 C 110 220, 160 220, 200 236 C 240 220, 290 220, 320 232 L 320 92 C 290 80, 240 80, 200 95 Z" fill="{AGUADA}"/>
<path d="M200 95 L 200 236"/>
<path d="M100 115 C 130 108, 160 108, 185 116 M100 140 C 130 133, 160 133, 185 141 M100 165 C 130 158, 160 158, 185 166 M100 190 C 130 183, 160 183, 185 191" stroke-width="2.5"/>
<path d="M215 116 C 240 108, 270 108, 300 115 M215 141 C 240 133, 270 133, 300 140 M215 166 C 240 158, 270 158, 300 165" stroke-width="2.5"/>
{raminho(212, 205, -8)}
'''

D['1'] = f'''
<path d="M110 200 C 110 120, 290 120, 290 200 Z" fill="{AGUADA}"/>
<path d="M98 200 L 302 200"/>
<path d="M150 150 C 175 140, 225 140, 250 150" stroke-width="2.5"/>
<circle cx="168" cy="240" r="13"/><circle cx="208" cy="246" r="13"/>
<path d="M178 230 L 262 186 M198 236 L 262 196"/>
<path d="M240 200 L 250 212 M255 196 L 262 207" stroke-width="2"/>
{chao(80, 320, 266)}
'''

D['2'] = f'''
<path d="M95 190 L 305 190 L 280 225 L 120 225 Z" fill="{AGUADA}"/>
<path d="M140 190 L 140 160 L 260 160 L 260 190"/>
<path d="M165 160 L 165 128 L 190 128 L 190 160 M215 160 L 215 118 L 240 118 L 240 160"/>
<path d="M160 175 h0 M185 175 h0 M210 175 h0 M235 175 h0" stroke-width="9"/>
<path d="M200 112 C 210 100, 225 98, 236 104 C 246 92, 262 94, 268 104" stroke-width="2.5"/>
<path d="M60 245 C 80 235, 100 255, 120 245 C 140 235, 160 255, 180 245 C 200 235, 220 255, 240 245 C 260 235, 280 255, 300 245 C 320 235, 340 255, 345 248"/>
'''

D['3'] = f'''
<path d="M60 222 C 150 212, 250 220, 340 204" stroke-width="5"/>
<path d="M305 208 C 316 194, 324 186, 338 184 M250 216 C 258 230, 270 236, 282 234" stroke-width="3"/>
<path d="M140 212 C 136 172, 170 140, 215 140 C 245 140, 262 152, 272 166 L 300 176 C 306 186, 300 198, 286 202 C 276 206, 262 210, 250 212 Z" fill="{AGUADA}"/>
<path d="M150 170 L 158 158 L 166 165 L 175 150 L 184 158 L 194 144 L 204 152 L 214 140 L 224 150 L 236 142 L 244 152" stroke-width="2.5"/>
<circle cx="268" cy="182" r="11" fill="#fff"/><circle cx="270" cy="182" r="4" fill="{TINTA}"/>
<path d="M286 196 C 292 196, 296 194, 300 190" stroke-width="2"/>
<path d="M140 212 C 112 214, 92 202, 94 182 C 96 164, 118 158, 128 170 C 136 180, 128 192, 118 188 C 111 185, 114 176, 119 176"/>
<path d="M165 210 L 160 224 L 152 228 M168 224 L 160 224 M232 212 L 236 224 L 228 228 M244 226 L 236 224" stroke-width="3"/>
<path d="M180 180 C 195 188, 220 188, 240 180 M175 196 C 195 204, 225 204, 245 196" stroke-width="2"/>
'''

D['4'] = f'''
<path d="M95 210 C 95 180, 115 160, 140 158 L 175 156 C 190 175, 220 185, 250 186 C 285 188, 305 198, 305 212 L 305 222 L 95 222 Z" fill="{AGUADA}"/>
<path d="M90 222 L 310 222 L 310 236 L 90 236 Z"/>
<path d="M175 156 C 175 140, 185 132, 198 132"/>
<path d="M185 175 L 210 168 M195 185 L 222 176 M207 192 L 235 182" stroke-width="2.5"/>
<path d="M125 186 C 135 194, 150 196, 160 190" stroke-width="2.5"/>
{chao(70, 330, 262)}
'''

D['5'] = f'''
<path d="M95 175 L 305 175 L 305 235 L 95 235 Z" fill="{AGUADA}"/>
<path d="M95 175 L 305 175 L 305 235 L 95 235 Z M95 195 L 305 195 M95 215 L 305 215"/>
<path d="M120 120 C 120 110, 128 104, 140 104 L 260 104 C 272 104, 280 110, 280 120 L 280 150 C 280 160, 272 166, 260 166 L 140 166 C 128 166, 120 160, 120 150 Z"/>
''' + ''.join(f'<g transform="translate({x} {y})"><circle r="3.2" fill="{TINTA}"/><circle cx="6" r="3" /><circle cx="-6" r="3"/><circle cy="6" r="3"/><circle cy="-6" r="3"/></g>'
              for x, y in [(130, 185), (190, 205), (250, 185), (160, 225), (280, 225), (225, 225)]) + chao(70, 330, 262)

D['6'] = f'''
<path d="M60 230 L 340 230 L 325 250 L 75 250 Z" fill="{AGUADA}"/>
<path d="M95 175 L 95 215 C 95 230, 108 232, 125 232 L 165 232 C 182 232, 195 230, 195 215 L 195 175 Z"/>
<path d="M195 185 C 218 185, 218 215, 195 213"/>
<path d="M230 190 L 238 230 L 292 230 L 300 190 Z" fill="#fff"/>
<path d="M300 198 C 316 196, 316 220, 296 220"/>
<path d="M300 205 L 312 205" stroke-width="2"/>
<path d="M130 160 C 120 145, 140 135, 130 118 M160 160 C 150 145, 170 135, 160 118" stroke-width="2.5"/>
<path d="M258 175 C 250 162, 268 155, 260 140" stroke-width="2.5"/>
'''

D['7'] = f'''
<path d="M110 90 L 290 90 L 290 250 L 110 250 Z" fill="{AGUADA}"/>
<path d="M110 120 L 290 120"/>
<path d="M150 80 L 150 100 M250 80 L 250 100"/>
''' + ''.join(f'<path d="M{126+c*27} {140+r*27} l14 14 m0 -14 l-14 14" stroke-width="2.5" stroke="#8a3b2e"/>'
              for r in range(4) for c in range(6) if r * 6 + c < 21) + \
    ''.join(f'<rect x="{126+c*27-2}" y="{140+r*27-2}" width="18" height="18" stroke-width="1.5"/>' for r in range(4) for c in range(6))

D['8'] = f'''
<path d="M70 250 L 160 150 L 205 195 L 245 160 L 330 250 Z" fill="{AGUADA}"/>
<path d="M70 250 L 160 150 L 205 195 L 245 160 L 330 250"/>
<circle cx="155" cy="105" r="32"/><circle cx="245" cy="105" r="32"/>
<path d="M187 100 C 195 92, 205 92, 213 100"/>
<path d="M123 98 L 92 88 M277 98 L 308 88"/>
'''

D['9'] = f'''
<path d="M95 255 L 305 255" stroke-width="3"/>
<path d="M110 255 L 120 240 M290 255 L 280 240" stroke-width="3"/>
<path d="M125 160 L 275 160 L 268 232 C 266 240, 258 242, 250 242 L 150 242 C 142 242, 134 240, 132 232 Z" fill="{AGUADA}"/>
<path d="M118 160 L 282 160"/>
<path d="M160 160 C 160 145, 240 145, 240 160"/>
<path d="M190 145 C 190 136, 210 136, 210 145"/>
<path d="M125 180 L 100 178 M275 180 L 300 178"/>
<path d="M170 125 C 160 110, 180 100, 170 84 M200 125 C 190 110, 210 100, 200 84 M230 125 C 220 110, 240 100, 230 84" stroke-width="2.5"/>
'''

D['10'] = f'''
<path d="M90 150 C 100 90, 300 90, 310 150 C 290 140, 270 140, 250 150 C 230 140, 210 140, 200 150 C 190 140, 170 140, 150 150 C 130 140, 110 140, 90 150 Z" fill="{AGUADA}"/>
<path d="M200 98 L 200 92 M200 150 L 200 245 C 200 258, 182 258, 182 245"/>
<path d="M150 150 C 160 120, 190 102, 200 98 C 210 102, 240 120, 250 150" stroke-width="2.5"/>
<path d="M70 80 l-8 18 M110 60 l-8 18 M300 70 l-8 18 M340 95 l-8 18 M85 190 l-8 18 M320 190 l-8 18 M120 215 l-8 18 M290 225 l-8 18" stroke-width="2.5"/>
'''

D['11'] = f'''
<path d="M110 200 C 110 175, 130 160, 160 158 L 240 158 C 270 160, 290 175, 290 200 L 290 238 L 110 238 Z" fill="{AGUADA}"/>
<path d="M95 128 C 95 108, 120 100, 200 100 C 280 100, 305 108, 305 128 L 305 140 L 265 140 L 262 125 L 138 125 L 135 140 L 95 140 Z"/>
<circle cx="200" cy="198" r="24"/>
<circle cx="200" cy="198" r="7"/>
<path d="M290 220 C 330 220, 340 240, 320 250 C 300 260, 310 270, 330 268" stroke-width="2.5"/>
'''

D['12'] = f'''
<path d="M150 80 L 210 80 C 218 80, 222 84, 222 92 L 222 190 C 222 198, 218 202, 210 202 L 150 202 C 142 202, 138 198, 138 190 L 138 92 C 138 84, 142 80, 150 80 Z" fill="{AGUADA}"/>
<path d="M150 98 L 210 98 L 210 160 L 150 160 Z" stroke-width="2.5"/>
<circle cx="180" cy="182" r="9"/>
<path d="M222 190 C 250 200, 250 225, 230 232 C 210 240, 205 255, 230 258 C 260 262, 270 245, 262 232 C 254 220, 275 210, 290 220" stroke-width="3"/>
<path d="M282 214 L 300 214 L 300 238 L 282 238 Z" fill="#fff"/>
<path d="M287 214 L 287 205 M295 214 L 295 205" stroke-width="2.5"/>
'''

D['13'] = f'''
<ellipse cx="200" cy="195" rx="62" ry="58" fill="{AGUADA}"/>
<ellipse cx="200" cy="195" rx="62" ry="58"/>
<ellipse cx="200" cy="195" rx="46" ry="42" fill="#fff"/>
<path d="M178 132 L 200 105 L 222 132 Z" fill="#fff"/>
<path d="M178 132 L 186 118 L 214 118 L 222 132 M186 118 L 200 105 L 214 118 M200 105 L 200 132" stroke-width="2.5"/>
{raminho(250, 255, -20)}
'''

D['14'] = f'''
<path d="M95 150 L 305 150 L 305 240 L 95 240 Z" fill="{AGUADA}"/>
<path d="M95 150 L 305 150 L 305 240 L 95 240 Z M200 150 L 200 240 M200 195 L 305 195"/>
<circle cx="145" cy="190" r="18" fill="#e8b64a" stroke-width="3"/>
<path d="M120 225 C 135 215, 165 215, 180 225" stroke-width="2.5"/>
<path d="M215 175 C 230 168, 250 180, 290 172 M215 220 h70" stroke-width="2.5"/>
<path d="M110 120 L 300 92 M110 132 L 300 104" stroke-width="4"/>
'''

D['15'] = f'''
<path d="M200 70 L 200 92"/>
<path d="M196 92 L 204 92 L 222 175 L 248 252 L 152 252 L 178 175 Z" fill="{AGUADA}"/>
<path d="M188 135 L 212 135 M174 175 L 226 175"/>
<path d="M170 252 C 175 222, 225 222, 230 252"/>
<path d="M184 175 L 200 135 L 216 175 M180 175 L 196 92 M220 175 L 204 92" stroke-width="2"/>
''' + ''.join(f'<g transform="translate({x} {y})" stroke-width="2"><path d="M-7 0 h14 M0 -7 v14 M-5 -5 l10 10 M5 -5 l-10 10"/></g>'
              for x, y in [(110, 95), (300, 80), (140, 170), (290, 160), (100, 230), (320, 225), (260, 115), (125, 130)])

D['16'] = f'''
<path d="M120 80 L 270 80 L 270 250 L 120 250 Z" fill="{AGUADA}"/>
<path d="M120 80 L 270 80 L 270 250 L 120 250 Z M138 80 L 138 250"/>
<path d="M270 95 L 292 95 L 292 115 L 270 115 M270 125 L 292 125 L 292 145 L 270 145 M270 155 L 292 155 L 292 175 L 270 175 M270 185 L 292 185 L 292 205 L 270 205" fill="#fff"/>
<path d="M160 120 h85 M160 145 h85 M160 170 h60" stroke-width="2.5"/>
<path d="M160 200 l8 8 l16 -18" stroke="#4f7a3a" stroke-width="3"/>
<path d="M195 205 l14 14 m0 -14 l-14 14" stroke="#8a3b2e" stroke-width="3"/>
'''

D['17'] = f'''
<path d="M170 120 L 230 120 L 236 245 C 236 255, 228 260, 220 260 L 180 260 C 172 260, 164 255, 164 245 Z" fill="{AGUADA}"/>
<path d="M166 120 L 234 120 L 234 104 L 166 104 Z"/>
<path d="M182 104 C 182 80, 190 64, 200 62 C 210 64, 218 80, 218 104"/>
<path d="M170 160 h14 M170 185 h14 M170 210 h14 M170 235 h14" stroke-width="2.5"/>
<path d="M120 150 c-6 -10 4 -16 8 -8 c4 -8 14 -2 8 8 l-8 9 z M280 200 c-6 -10 4 -16 8 -8 c4 -8 14 -2 8 8 l-8 9 z" fill="#c98e86" stroke-width="2"/>
'''

D['18'] = f'''
<path d="M110 125 L 290 125 C 300 125, 305 130, 305 140 L 305 240 C 305 250, 300 255, 290 255 L 110 255 C 100 255, 95 250, 95 240 L 95 140 C 95 130, 100 125, 110 125 Z" fill="#c9d3e3"/>
<path d="M170 125 L 170 105 C 170 98, 175 95, 182 95 L 218 95 C 225 95, 230 98, 230 105 L 230 125"/>
<path d="M95 185 L 305 185" stroke="#a33a2c" stroke-width="7"/>
<path d="M200 125 L 200 255" stroke="#a33a2c" stroke-width="7"/>
<path d="M190 185 C 175 165, 160 175, 175 190 C 185 198, 195 192, 200 185 C 205 192, 215 198, 225 190 C 240 175, 225 165, 210 185" stroke="#a33a2c" stroke-width="3"/>
<circle cx="125" cy="262" r="8"/><circle cx="275" cy="262" r="8"/>
'''

D['19'] = f'''
<path d="M200 105 C 170 105, 160 135, 160 160 C 160 205, 175 235, 200 235 C 225 235, 240 205, 240 160 C 240 135, 230 105, 200 105 Z" fill="#efe3a6"/>
<path d="M200 105 C 200 92, 204 84, 212 78" stroke-width="3.5"/>
<path d="M162 150 C 185 160, 215 160, 238 150 M161 175 C 185 185, 215 185, 239 175 M165 200 C 185 210, 215 210, 235 200" stroke-width="2"/>
<path d="M240 205 C 270 200, 300 215, 295 235 C 290 255, 250 250, 240 262 C 230 274, 260 280, 290 272" stroke-width="3"/>
{chao(70, 330, 262)}
'''

D['20'] = f'''
<circle cx="200" cy="175" r="78" fill="{AGUADA}"/>
<circle cx="200" cy="175" r="78"/>
<circle cx="200" cy="175" r="58" fill="#fff"/>
<circle cx="200" cy="175" r="14"/>
<path d="M142 168 L 186 172 M214 172 L 258 168 M200 189 L 200 233"/>
'''

D['21'] = f'''
<circle cx="200" cy="130" r="58" stroke-width="12" stroke="{AGUADA}"/>
<circle cx="200" cy="130" r="64"/><circle cx="200" cy="130" r="52"/>
<path d="M185 110 L 215 110 C 219 110, 221 112, 221 116 L 221 148 C 221 152, 219 154, 215 154 L 185 154 C 181 154, 179 152, 179 148 L 179 116 C 179 112, 181 110, 185 110 Z"/>
<path d="M200 194 L 200 225 M200 225 L 160 262 M200 225 L 240 262 M200 225 L 200 262"/>
'''

D['22'] = f'''
<path d="M80 130 L 280 130 L 280 230 L 80 230 Z" fill="#f2efe0"/>
<path d="M280 160 L 318 160 L 330 195 L 330 230 L 280 230 Z"/>
<path d="M290 168 L 312 168 L 322 195 L 290 195 Z" stroke-width="2.5"/>
<path d="M105 150 L 225 150 L 225 195 L 105 195 Z" fill="#fff"/>
<path d="M95 130 L 240 130 L 230 112 L 105 112 Z" fill="#c5d0a4"/>
<path d="M120 112 L 115 130 M140 112 L 138 130 M160 112 L 160 130 M180 112 L 182 130 M200 112 L 205 130 M220 112 L 227 130" stroke-width="2.5"/>
<circle cx="125" cy="236" r="18" fill="#fff"/><circle cx="295" cy="236" r="18" fill="#fff"/>
<path d="M135 172 C 150 160, 175 160, 190 172 Z" fill="#e8d9a8" stroke-width="2.5"/>
<path d="M60 262 L 340 262" stroke-width="2.5"/>
'''

D['23'] = f'''
<path d="M110 165 L 290 165 C 290 215, 255 245, 200 245 C 145 245, 110 215, 110 165 Z" fill="{AGUADA}"/>
<path d="M100 165 L 300 165"/>
<path d="M250 175 L 320 110" stroke-width="5"/>
<ellipse cx="327" cy="103" rx="12" ry="8" transform="rotate(-42 327 103)"/>
<path d="M160 150 C 150 135, 170 125, 160 108 M200 150 C 190 135, 210 125, 200 108 M240 150 C 230 135, 250 125, 240 108" stroke-width="2.5"/>
<path d="M150 250 L 250 250" stroke-width="2.5"/>
'''

D['24'] = f'''
<path d="M100 80 L 300 80 L 300 255 L 100 255 Z" fill="{AGUADA}"/>
<path d="M100 80 L 300 80 L 300 255 L 100 255 Z M100 100 L 300 100"/>
<path d="M150 100 L 195 100 L 195 255 L 150 255 Z M205 100 L 250 100 L 250 255 L 205 255 Z" fill="#eef2ee"/>
<path d="M160 150 L 172 140 M162 170 L 182 152 M215 150 L 227 140 M217 170 L 237 152" stroke-width="2"/>
<path d="M190 90 L 210 90" stroke-width="3"/>
<path d="M140 178 L 112 178 M120 170 L 112 178 L 120 186 M260 178 L 288 178 M280 170 L 288 178 L 280 186" stroke-width="3"/>
'''

D['25'] = f'''
<path d="M160 70 L 240 70 C 250 70, 255 75, 255 85 L 255 245 C 255 255, 250 260, 240 260 L 160 260 C 150 260, 145 255, 145 245 L 145 85 C 145 75, 150 70, 160 70 Z" fill="{AGUADA}"/>
<path d="M158 92 L 242 92 L 242 232 L 158 232 Z" fill="#fff" stroke-width="2.5"/>
<path d="M190 81 L 210 81 M195 246 L 205 246" stroke-width="3"/>
<path d="M168 106 L 228 106 C 232 106, 234 108, 234 112 L 234 124 C 234 128, 232 130, 228 130 L 176 130 L 168 136 Z M168 146 L 222 146 C 226 146, 228 148, 228 152 L 228 164 C 228 168, 226 170, 222 170 L 176 170 L 168 176 Z M168 186 L 230 186 C 234 186, 236 188, 236 192 L 236 204 C 236 208, 234 210, 230 210 L 176 210 L 168 216 Z" stroke-width="2"/>
<circle cx="256" cy="74" r="13" fill="#a33a2c" stroke="#a33a2c"/>
<path d="M285 120 C 300 112, 305 100, 300 88 M110 120 C 95 112, 90 100, 95 88" stroke-width="2.5"/>
'''

D['26'] = f'''
<path d="M120 105 L 280 105 C 285 105, 288 108, 288 113 L 288 205 L 112 205 L 112 113 C 112 108, 115 105, 120 105 Z" fill="{AGUADA}"/>
<path d="M126 118 L 274 118 L 274 195 L 126 195 Z" fill="#fff" stroke-width="2.5"/>
<path d="M90 205 L 310 205 L 296 222 L 104 222 Z"/>
<circle cx="200" cy="146" r="14" stroke-width="2.5"/><path d="M174 190 C 178 168, 222 168, 226 190" stroke-width="2.5"/>
<path d="M300 180 L 304 214 C 305 220, 310 222, 318 222 L 330 222 C 338 222, 343 220, 344 214 L 348 180 Z"/>
<path d="M348 188 C 362 188, 362 208, 346 208"/>
<path d="M316 168 C 310 156, 324 150, 318 138 M332 168 C 326 156, 340 150, 334 138" stroke-width="2"/>
'''

D['27'] = f'''
<path d="M120 130 C 120 98, 160 85, 200 88 C 245 90, 275 108, 275 140 L 275 215 L 257 215 L 257 182 L 238 182 L 238 215 L 220 215 L 220 182 L 175 182 L 175 215 L 157 215 L 157 182 L 140 182 L 140 215 L 122 215 L 122 170 C 104 168, 96 150, 104 135 Z" fill="{AGUADA}"/>
<path d="M275 140 C 300 140, 315 155, 312 180 C 310 198, 298 210, 302 225 C 304 232, 312 234, 316 228"/>
<path d="M275 132 C 260 118, 262 100, 280 98 C 296 96, 300 112, 292 124"/>
<circle cx="292" cy="128" r="3.5" fill="{TINTA}"/>
<path d="M122 135 C 112 130, 106 125, 104 135" stroke-width="2.5"/>
<path d="M140 212 C 120 220, 100 222, 82 220" stroke-width="2" stroke-dasharray="6 5"/>
<path d="M78 205 L 78 238" stroke-width="5"/>
{chao(60, 340, 240)}
'''

D['28'] = f'''
<path d="M110 120 C 110 70, 290 70, 290 120 C 270 110, 250 110, 230 120 C 215 110, 185 110, 170 120 C 150 110, 130 110, 110 120 Z" fill="#e7c9c3"/>
<path d="M200 76 L 200 120 M150 82 C 160 100, 168 112, 170 120 M250 82 C 240 100, 232 112, 230 120" stroke-width="2"/>
<path d="M110 120 L 192 190 M170 120 L 196 190 M230 120 L 204 190 M290 120 L 208 190" stroke-width="1.6"/>
<circle cx="200" cy="196" r="7"/><path d="M200 203 L 200 222 M200 210 L 188 202 M200 210 L 212 202 M200 222 L 192 236 M200 222 L 208 236" stroke-width="2.5"/>
<path d="M60 262 L 140 200 L 165 218 L 185 205 L 260 262" fill="{AGUADA}"/>
<path d="M140 200 L 150 214 L 160 208 L 165 218" stroke-width="2"/>
<path d="M270 262 L 340 262" stroke-width="2.5"/>
'''

D['29'] = f'''
<path d="M135 125 L 245 125 L 238 240 C 237 250, 230 255, 220 255 L 160 255 C 150 255, 143 250, 142 240 Z" fill="#fff"/>
<path d="M135 125 L 245 125 L 238 240 C 237 250, 230 255, 220 255 L 160 255 C 150 255, 143 250, 142 240 Z"/>
<path d="M243 150 C 285 150, 290 215, 238 215"/>
<path d="M255 158 l8 6 M270 180 l9 2 M262 202 l8 -5" stroke="#c8a24a" stroke-width="3"/>
<path d="M170 110 C 160 95, 180 85, 170 68 M200 110 C 190 95, 210 85, 200 68 M230 110 C 220 95, 240 85, 230 68" stroke-width="2.5"/>
{chao(80, 320, 262)}
'''

def cubo():
    a = 70
    cx, cy = 200, 175
    top = f'M{cx} {cy-a} L {cx+a*0.87} {cy-a/2} L {cx} {cy} L {cx-a*0.87} {cy-a/2} Z'
    left = f'M{cx-a*0.87} {cy-a/2} L {cx} {cy} L {cx} {cy+a} L {cx-a*0.87} {cy+a/2} Z'
    right = f'M{cx+a*0.87} {cy-a/2} L {cx} {cy} L {cx} {cy+a} L {cx+a*0.87} {cy+a/2} Z'
    g = f'<path d="{top}" fill="#f1d36b"/><path d="{left}" fill="#c96a55"/><path d="{right}" fill="#7f9bc4"/>'
    T=(cx,cy-a); R=(cx+a*0.87,cy-a/2); C=(cx,cy); L=(cx-a*0.87,cy-a/2); B=(cx,cy+a); BL=(cx-a*0.87,cy+a/2); BR=(cx+a*0.87,cy+a/2)
    def lerp(p,q,t): return (p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t)
    def ln(p,q): return f'<path d="M{p[0]:.1f} {p[1]:.1f} L {q[0]:.1f} {q[1]:.1f}" stroke-width="2.5"/>'
    for k in (1, 2):
        t = k / 3
        g += ln(lerp(L,T,t), lerp(C,R,t)) + ln(lerp(T,R,t), lerp(L,C,t))
        g += ln(lerp(L,C,t), lerp(BL,B,t)) + ln(lerp(L,BL,t), lerp(C,B,t))
        g += ln(lerp(C,R,t), lerp(B,BR,t)) + ln(lerp(C,B,t), lerp(R,BR,t))
    g += f'<path d="{top}"/><path d="{left}"/><path d="{right}"/>'
    return g

D['30'] = cubo() + f'''
<path d="M70 268 C 95 258, 120 278, 145 268 C 170 258, 195 278, 220 268 C 245 258, 270 278, 295 268 C 310 262, 325 266, 335 270" stroke="#5f84a8" stroke-width="3"/>
'''

D['31'] = f'''
<path d="M200 110 C 170 98, 125 96, 85 104 L 85 240 C 125 232, 170 234, 200 246 C 230 234, 275 232, 315 240 L 315 104 C 275 96, 230 98, 200 110 Z" fill="{AGUADA}"/>
<path d="M200 110 L 200 246"/>
''' + ''.join(f'<path d="M100 {128+i*22} L 185 {128+i*22}" stroke-width="2"/><path d="M100 {128+i*22} L 185 {128+i*22}" stroke="#8a3b2e" stroke-width="2.5" transform="translate(0 -4)"/>' for i in range(5)) + \
    ''.join(f'<path d="M215 {124+i*22} C 240 {120+i*22}, 270 {128+i*22}, 300 {122+i*22}" stroke-width="2.5"/>' for i in range(5)) + \
    '<path d="M150 270 C 180 262, 220 262, 250 270" stroke-width="3"/>'

D['32'] = f'''
<path d="M60 220 C 120 120, 280 120, 340 220" fill="none" stroke-width="6"/>
<path d="M60 220 L 340 220" stroke-width="6"/>
<path d="M100 220 L 100 170 M140 220 L 140 145 M180 220 L 180 134 M220 220 L 220 134 M260 220 L 260 145 M300 220 L 300 170" stroke-width="3"/>
<path d="M60 220 L 60 252 M340 220 L 340 252" stroke-width="6"/>
<path d="M40 252 C 90 244, 120 260, 170 252 C 220 244, 260 260, 300 252 C 330 247, 350 252, 365 254" stroke="#5f84a8" stroke-width="3"/>
<circle cx="182" cy="200" r="7"/><path d="M182 207 L 182 220" stroke-width="3"/>
<circle cx="204" cy="200" r="7"/><path d="M204 207 L 204 220" stroke-width="3"/>
<path d="M189 212 L 197 212" stroke-width="3"/>
'''

D['33'] = f'''
<path d="M170 70 L 192 150 M230 70 L 208 150" stroke="#5f84a8" stroke-width="12"/>
<path d="M164 70 L 236 70" stroke-width="3"/>
<circle cx="200" cy="190" r="46" fill="#ecd27c"/>
<circle cx="200" cy="190" r="46"/><circle cx="200" cy="190" r="34" stroke-width="2.5"/>
<path d="M200 168 L 206 182 L 221 183 L 210 193 L 213 208 L 200 200 L 187 208 L 190 193 L 179 183 L 194 182 Z" stroke-width="2.5"/>
{raminho(110, 262, -5)}{raminho(290, 262, 185)}
'''

D['epilogo'] = f'''
<path d="M110 195 C 110 125, 290 125, 290 195 Z" fill="{AGUADA}"/>
<path d="M98 195 L 302 195"/>
<path d="M150 150 C 175 140, 225 140, 250 150" stroke-width="2.5"/>
<path d="M130 225 C 140 212, 150 232, 160 220 M180 232 C 188 220, 198 238, 206 226 M228 224 C 236 212, 246 230, 254 218" stroke-width="2.5"/>
{raminho(240, 262, -10)}{raminho(160, 262, 190)}
'''

def svg(corpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="1200" height="900">'
            f'<g fill="none" stroke="{TINTA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{corpo}</g></svg>')

def render(chaves=None):
    SAIDA.mkdir(exist_ok=True)
    feitos = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, corpo in D.items():
            if chaves and k not in chaves:
                continue
            html = Path(tmp) / f'{k}.html'
            html.write_text('<html><body style="margin:0;background:transparent">' + svg(corpo) + '</body></html>', encoding='utf-8')
            png = SAIDA / f'vinheta_{k}.png'
            subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                            '--default-background-color=00000000', '--window-size=1200,900',
                            f'--screenshot={png}', f'file://{html}'], capture_output=True, timeout=60)
            feitos.append(png.name)
    return feitos

if __name__ == '__main__':
    print(len(render(sys.argv[1:] or None)), 'vinhetas em', SAIDA)
