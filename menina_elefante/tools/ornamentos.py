#!/usr/bin/env python3
"""Gera as folhas de fundo das páginas de destaque (frases grandes) em PNG: fundo cinza-escuro
e um ornamento claro num canto (volutas, folhas, arco pontilhado), no estilo das páginas de
citação de livros de negócios. Só usa a biblioteca padrão do Python.

Uso: python3 tools/ornamentos.py   -> ilustracoes/destaque_*.png (1100 x 1700 px, 200 dpi, 5,5 x 8,5 pol.)
"""
import math, random, struct, zlib
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'ilustracoes'
W, H = 1100, 1700            # pixels da página
S = W / 1000                 # espaço de desenho: 1000 de largura
FUNDO = (58, 58, 58)
TINTA = (176, 176, 170)
K = 1.0        # ampliação do ornamento a partir do canto (0, 1545); ajustada por desenho em gerar()
GROSSO = 1.15  # engrossa os traços


def _esc(x, y):
    return (x * K * S, (1545 - (1545 - y) * K) * S)


class Tela:
    def __init__(self, espelho=False):
        self.a = array('f', bytes(4 * W * H))
        self.espelho = espelho

    def _esc(self, x, y):
        X, Y = _esc(x, y)
        return (W - X if self.espelho else X), Y

    def _put(self, x, y, c):
        i = y * W + x
        if c > self.a[i]:
            self.a[i] = c if c < 1 else 1.0

    def capsula(self, x0, y0, x1, y1, r0, r1):
        """Segmento com raio que varia de r0 a r1 (pixels), pontas redondas, antisserrilhado."""
        rm = max(r0, r1) + 1
        xa, xb = int(max(0, min(x0, x1) - rm)), int(min(W - 1, max(x0, x1) + rm))
        ya, yb = int(max(0, min(y0, y1) - rm)), int(min(H - 1, max(y0, y1) + rm))
        dx, dy = x1 - x0, y1 - y0
        L2 = dx * dx + dy * dy or 1e-9
        for y in range(ya, yb + 1):
            py = y + 0.5 - y0
            for x in range(xa, xb + 1):
                px = x + 0.5 - x0
                t = (px * dx + py * dy) / L2
                t = 0.0 if t < 0 else 1.0 if t > 1 else t
                ex, ey = px - t * dx, py - t * dy
                c = r0 + (r1 - r0) * t + 0.5 - math.sqrt(ex * ex + ey * ey)
                if c > 0:
                    self._put(x, y, c)

    def traco(self, pts, r0, r1=None):
        """Polilinha (coordenadas de desenho) com espessura afinando de r0 a r1."""
        r1 = r0 if r1 is None else r1
        P = [self._esc(x, y) for x, y in pts]
        seg = [math.dist(P[i], P[i + 1]) for i in range(len(P) - 1)]
        tot = sum(seg) or 1
        acc = 0
        for i in range(len(P) - 1):
            ra = (r0 + (r1 - r0) * acc / tot) * S * K * GROSSO
            acc += seg[i]
            rb = (r0 + (r1 - r0) * acc / tot) * S * K * GROSSO
            self.capsula(*P[i], *P[i + 1], ra, rb)

    def ponto(self, x, y, r):
        X, Y = self._esc(x, y)
        self.capsula(X, Y, X, Y, r * S * K * GROSSO, r * S * K * GROSSO)

    def poligono(self, pts):
        """Preenche um polígono com 4 sub-linhas por pixel."""
        P = [self._esc(x, y) for x, y in pts]
        ys = [p[1] for p in P]
        ya, yb = max(0, int(min(ys))), min(H - 1, int(max(ys)) + 1)
        n = len(P)
        for y in range(ya, yb + 1):
            row = {}
            for s in range(4):
                sy = y + (s + 0.5) / 4
                xs = []
                for i in range(n):
                    (xa, y0), (xb, y1) = P[i], P[(i + 1) % n]
                    if (y0 <= sy < y1) or (y1 <= sy < y0):
                        xs.append(xa + (sy - y0) * (xb - xa) / (y1 - y0))
                xs.sort()
                for j in range(0, len(xs) - 1, 2):
                    a, b = max(0.0, xs[j]), min(W - 0.001, xs[j + 1])
                    if b <= a:
                        continue
                    ia, ib = int(a), int(b)
                    if ia == ib:
                        row[ia] = row.get(ia, 0) + (b - a) / 4
                        continue
                    row[ia] = row.get(ia, 0) + (ia + 1 - a) / 4
                    for x in range(ia + 1, ib):
                        row[x] = row.get(x, 0) + 0.25
                    row[ib] = row.get(ib, 0) + (b - ib) / 4
            for x, c in row.items():
                if 0 <= x < W:
                    self._put(x, y, c)

    def png(self, path):
        raw = bytearray()
        fr, fg, fb = FUNDO
        tr, tg, tb = TINTA
        for y in range(H):
            raw.append(0)
            base = y * W
            for x in range(W):
                c = self.a[base + x]
                if c:
                    raw += bytes((int(fr + (tr - fr) * c), int(fg + (tg - fg) * c), int(fb + (tb - fb) * c)))
                else:
                    raw += bytes(FUNDO)
        def chunk(t, d):
            return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
        ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
        phys = struct.pack('>IIB', 7874, 7874, 1)   # 200 dpi
        path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'pHYs', phys)
                         + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


# ---------- geometria ----------
def bezier(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def espiral(cx, cy, R, a0, voltas, sentido, n=90, aperto=0.28):
    """Espiral logarítmica que começa em (cx + R cos a0, cy + R sin a0) e se enrola para dentro."""
    out = []
    for i in range(n + 1):
        th = voltas * 2 * math.pi * i / n
        r = R * math.exp(-aperto * th)
        a = a0 + sentido * th
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def voluta(t, p0, c1, c2, fim, R, sentido, voltas=1.6, r0=9, r1=2.2):
    """Haste em curva que termina numa espiral, afinando, com um ponto no miolo."""
    haste = bezier(p0, c1, c2, fim)
    dx, dy = fim[0] - c2[0], fim[1] - c2[1]
    ang = math.atan2(dy, dx)
    # centro da espiral: à esquerda/direita da direção de chegada
    nx, ny = -math.sin(ang) * sentido, math.cos(ang) * sentido
    cx, cy = fim[0] + nx * R, fim[1] + ny * R
    a0 = math.atan2(fim[1] - cy, fim[0] - cx)
    esp = espiral(cx, cy, R, a0, voltas, sentido)
    pts = haste + esp[1:]
    t.traco(pts, r0, r1)
    t.ponto(*esp[-1], r1 * 1.8)
    return haste


def folha(t, base, ang, L, larg, curva=0.35, ponta=0.25):
    """Folha de acanto: nervura curva, largura em seno, ponta que dobra."""
    ca, sa = math.cos(ang), math.sin(ang)
    esq, dir_ = [], []
    n = 40
    for i in range(n + 1):
        s = i / n
        dev = curva * L * math.sin(math.pi * s) * 0.35 + ponta * L * max(0, s - 0.7) ** 2 * 3
        x = base[0] + ca * s * L - sa * dev
        y = base[1] + sa * s * L + ca * dev
        h = larg * (math.sin(math.pi * min(s, 0.98)) ** 0.75) * (1 - 0.35 * s)
        # recortes do acanto
        h *= 1 - 0.18 * (0.5 + 0.5 * math.cos(s * 5 * 2 * math.pi))
        esq.append((x - sa * h, y + ca * h))
        dir_.append((x + sa * h, y - ca * h))
    t.poligono(esq + dir_[::-1])


def arco_pontilhado(t, cx, cy, R, a0, a1, passo, r):
    a = a0
    while a <= a1:
        t.ponto(cx + R * math.cos(a), cy + R * math.sin(a), r)
        a += passo / R


def aneis(t, cx, cy, R):
    """Anel grosso, anel pontilhado, anel fino e marcas, como o mostrador das páginas de exemplo."""
    def circ(r, w):
        pts = [(cx + r * math.cos(a / 180 * math.pi), cy + r * math.sin(a / 180 * math.pi)) for a in range(0, 361, 2)]
        t.traco(pts, w)
    circ(R, 4.5)
    circ(R * 0.9, 1.6)
    arco_pontilhado(t, cx, cy, R * 1.07, 0, 2 * math.pi, 22, 5.5)
    for k in range(24):
        a = k * math.pi / 12
        L = 0.09 if k % 2 == 0 else 0.05
        t.traco([(cx + R * 0.9 * math.cos(a), cy + R * 0.9 * math.sin(a)),
                 (cx + R * (0.9 - L) * math.cos(a), cy + R * (0.9 - L) * math.sin(a))], 3 if k % 2 == 0 else 1.6)


# ---------- composições (canto inferior esquerdo; a versão "dir" é espelhada) ----------
def relogio(t, seed):
    rnd = random.Random(seed)
    aneis(t, -60, 1600, 330)
    haste = voluta(t, (40, 1545), (20, 1350), (180, 1250), (250, 1080), 70, -1, 1.7, 11, 2.5)
    voluta(t, (150, 1545), (330, 1500), (470, 1400), (430, 1260), 55, 1, 1.5, 8, 2)
    voluta(t, (250, 1080), (330, 990), (300, 900), (220, 860), 42, -1, 1.5, 6, 1.6)
    for k, (s, lado) in enumerate([(12, 1), (22, -1), (32, 1), (44, -1)]):
        x, y = haste[s]
        ang = -math.pi / 2 + lado * (0.75 + rnd.uniform(-0.12, 0.12))
        folha(t, (x, y), ang, 150 - 18 * k, 34 - 3 * k, curva=0.4 * lado, ponta=0.3 * lado)
    folha(t, (40, 1545), -1.35, 260, 55, curva=-0.5, ponta=-0.3)
    folha(t, (150, 1545), -0.55, 230, 48, curva=0.45, ponta=0.35)
    pts = bezier((30, 1200), (-10, 1050), (60, 900), (20, 760), 30)
    for i, (x, y) in enumerate(pts[::2]):
        t.ponto(x, y, 7 - i * 0.35)


def vinha(t, seed):
    rnd = random.Random(seed)
    tronco = bezier((70, 1545), (-10, 1300), (150, 1100), (60, 850), 80)
    t.traco(tronco, 12, 5)
    voluta(t, tronco[-1], (20, 780), (60, 700), (140, 690), 45, 1, 1.6, 5, 1.5)
    y_ramos = [10, 25, 40, 55, 68]
    for k, s in enumerate(y_ramos):
        x, y = tronco[s]
        lado = 1 if k % 2 == 0 else -1
        if lado == 1:
            voluta(t, (x, y), (x + 90, y - 20), (x + 170, y - 90), (x + 150, y - 170), 45 - 4 * k, 1, 1.5, 7 - k * 0.6, 1.6)
            folha(t, (x, y), -0.35 - rnd.uniform(0, 0.2), 170 - 15 * k, 36 - 3 * k, curva=0.4, ponta=0.35)
        else:
            folha(t, (x, y), -2.4 + rnd.uniform(-0.1, 0.1), 110 - 10 * k, 26 - 2 * k, curva=-0.4, ponta=-0.3)
    voluta(t, (200, 1545), (380, 1540), (520, 1450), (480, 1330), 60, -1, 1.6, 9, 2)
    folha(t, (200, 1545), -0.3, 280, 50, curva=0.5, ponta=0.4)
    arco_pontilhado(t, 70, 1545, 430, -math.pi / 2 + 0.05, -0.25, 26, 5)


def ramo(t, seed):
    rnd = random.Random(seed)
    arco_pontilhado(t, -40, 1620, 520, -math.pi / 2, 0, 24, 5.5)
    t.traco([(-40 + 470 * math.cos(a / 100), 1620 + 470 * math.sin(a / 100)) for a in range(-157, 1, 2)], 4)
    haste = voluta(t, (0, 1480), (160, 1440), (230, 1300), (180, 1180), 60, -1, 1.7, 10, 2.4)
    voluta(t, (180, 1180), (140, 1060), (230, 980), (330, 1010), 48, 1, 1.5, 7, 1.8)
    voluta(t, (60, 1545), (300, 1560), (420, 1470), (400, 1380), 50, 1, 1.5, 8, 2)
    for k, s in enumerate([15, 30, 45]):
        x, y = haste[s]
        folha(t, (x, y), -2.2 + 0.25 * k + rnd.uniform(-0.1, 0.1), 140 - 15 * k, 30 - 3 * k, curva=-0.4, ponta=-0.3)
        folha(t, (x, y), -0.5 - 0.1 * k, 120 - 12 * k, 26 - 2 * k, curva=0.4, ponta=0.3)
    folha(t, (0, 1480), -0.9, 200, 44, curva=0.4, ponta=0.35)


DESENHOS = {'relogio': relogio, 'vinha': vinha, 'ramo': ramo}
# escala de cada desenho: o topo do ornamento fica abaixo de ~55% da altura da página
ESCALA = {'relogio': 1.05, 'vinha': 0.85, 'ramo': 1.15}


def gerar(nome, lado, seed=7):
    global K
    K = ESCALA[nome]
    t = Tela(espelho=(lado == 'dir'))
    DESENHOS[nome](t, seed)
    OUT.mkdir(exist_ok=True)
    p = OUT / f'destaque_{nome}_{lado}.png'
    t.png(p)
    return p


def main():
    for nome in DESENHOS:
        for lado in ('esq', 'dir'):
            print(gerar(nome, lado).relative_to(ROOT))


if __name__ == '__main__':
    main()
