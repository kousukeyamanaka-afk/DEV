#!/usr/bin/env python3
"""Gera as folhas de fundo das páginas de destaque (frases grandes) em PNG: fundo cinza-escuro
e um ramo de oliveira claro num canto (folhas lanceoladas com nervura, azeitonas), no estilo das
páginas de citação de livros de negócios. Só usa a biblioteca padrão do Python.

Uso: python3 tools/ornamentos.py   -> ilustracoes/destaque_<desenho>_<lado>[_azeitonas].png
(1100 x 1700 px, 200 dpi, 5,5 x 8,5 pol.). Cada desenho sai com e sem azeitonas; manuscrito/destaques.json
escolhe qual versão cada página usa.
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
K = 1.0        # ampliação do ornamento a partir da âncora; ajustada por desenho em gerar()
ANCORA = (0, 1545)   # ponto fixo da ampliação (o canto, ou o centro de baixo na coroa)
GROSSO = 1.15  # engrossa os traços


def _esc(x, y):
    ax, ay = ANCORA
    return ((ax + (x - ax) * K) * S, (ay + (y - ay) * K) * S)


class Tela:
    def __init__(self, espelho=False):
        self.a = array('f', bytes(4 * W * H))
        self.espelho = espelho
        self.apagar = False     # True: desenha com a cor do fundo (nervuras, brilho das azeitonas)

    def _esc(self, x, y):
        X, Y = _esc(x, y)
        return (W - X if self.espelho else X), Y

    def _put(self, x, y, c):
        i = y * W + x
        if self.apagar:
            v = 1.0 - (c if c < 1 else 1.0)
            if v < self.a[i]:
                self.a[i] = v
        elif c > self.a[i]:
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


def arco_pontilhado(t, cx, cy, R, a0, a1, passo, r):
    a = a0
    while a <= a1:
        t.ponto(cx + R * math.cos(a), cy + R * math.sin(a), r)
        a += passo / R


def ao_longo(pts):
    """Comprimento acumulado de uma polilinha: devolve (total, função s -> (ponto, ângulo))."""
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    def em(s):
        s = max(0.0, min(acc[-1], s))
        for k in range(1, len(acc)):
            if acc[k] >= s:
                f = (s - acc[k - 1]) / ((acc[k] - acc[k - 1]) or 1)
                (x0, y0), (x1, y1) = pts[k - 1], pts[k]
                return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f), math.atan2(y1 - y0, x1 - x0)
        return pts[-1], math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    return acc[-1], em


def folha_oliveira(t, base, ang, L, larg, curva=0.0):
    """Folha de oliveira: comprida, estreita, pontuda nas duas pontas, com a nervura central vazada."""
    ca, sa = math.cos(ang), math.sin(ang)
    esq, dir_, nerv = [], [], []
    n = 36
    for i in range(n + 1):
        s = i / n
        dev = curva * L * math.sin(math.pi * s) * 0.12
        x = base[0] + ca * s * L - sa * dev
        y = base[1] + sa * s * L + ca * dev
        h = larg * (math.sin(math.pi * s) ** 0.8) * (1 - 0.25 * s)
        esq.append((x - sa * h, y + ca * h))
        dir_.append((x + sa * h, y - ca * h))
        if 0.06 < s < 0.86:
            nerv.append((x, y))
    t.poligono(esq + dir_[::-1])
    t.apagar = True
    t.traco(nerv, 1.3, 0.5)
    t.apagar = False


def azeitona(t, x, y, ang, r=11):
    """Azeitona oval presa por um cabinho, recortada das folhas por um contorno da cor do fundo."""
    ca, sa = math.cos(ang), math.sin(ang)
    cx, cy = x + ca * (r * 2.1), y + sa * (r * 2.1)

    def oval(rr):
        pts = []
        for k in range(40):
            a = 2 * math.pi * k / 40
            u, v = math.cos(a) * rr * 1.3, math.sin(a) * rr
            pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
        return pts
    t.apagar = True
    t.poligono(oval(r + 3.5))
    t.apagar = False
    t.traco([(x, y), (cx - ca * r * 1.1, cy - sa * r * 1.1)], 1.8, 1.3)
    t.poligono(oval(r))


def galho(t, pts, r0, r1, passo, L0, L1, larg0, larg1, azeitonas=(), seed=1, abertura=0.62):
    """Galho com folhas alternadas (menores para a ponta), folha terminal e azeitonas em alguns nós."""
    rnd = random.Random(seed)
    t.traco(pts, r0, r1)
    total, em = ao_longo(pts)
    s, k, frutos = passo * 0.8, 0, []
    while s < total - passo * 0.4:
        (x, y), a = em(s)
        f = s / total
        lado = 1 if k % 2 == 0 else -1
        L = L0 + (L1 - L0) * f
        folha_oliveira(t, (x, y), a + lado * (abertura + rnd.uniform(-0.12, 0.12)), L * rnd.uniform(0.9, 1.08),
                       larg0 + (larg1 - larg0) * f, curva=lado * rnd.uniform(0.3, 0.8))
        if k in azeitonas:
            r = 16 - 4 * f
            frutos += [(x, y, a - lado * 1.2, r), (x, y, a - lado * 1.85, r * 0.85)]
        s += passo * (1 - 0.25 * f)
        k += 1
    (x, y), a = em(total)
    folha_oliveira(t, (x, y), a, L1 * 1.05, larg1, curva=0.5)
    for fx, fy, fa, fr in frutos:
        azeitona(t, fx, fy, fa, r=fr)


# ---------- composições (canto inferior esquerdo; a versão "dir" é espelhada) ----------
# f = True desenha as azeitonas; False, só folhas.
def oliveira_longa(t, seed, f):
    """Um ramo que sobe do canto em curva aberta, com um raminho lateral."""
    principal = bezier((-10, 1560), (120, 1420), (230, 1250), (420, 1090), 120)
    galho(t, principal, 7, 2.4, 58, 130, 85, 17, 12, azeitonas=(2, 5, 8) if f else (), seed=seed)
    total, em = ao_longo(principal)
    (x, y), a = em(total * 0.38)
    lateral = bezier((x, y), (x + 70, y + 20), (x + 170, y + 5), (x + 250, y - 40), 60)
    galho(t, lateral, 3.5, 1.8, 50, 95, 70, 13, 10, azeitonas=(1,) if f else (), seed=seed + 1)


def oliveira_cruzada(t, seed, f):
    """Dois ramos que saem juntos do canto e se abrem em V."""
    a = bezier((10, 1580), (70, 1440), (130, 1300), (200, 1130), 110)
    b = bezier((10, 1580), (190, 1480), (340, 1420), (520, 1400), 110)
    galho(t, a, 6.5, 2.2, 56, 125, 80, 16, 11, azeitonas=(3, 7) if f else (), seed=seed)
    galho(t, b, 6.5, 2.2, 56, 125, 80, 16, 11, azeitonas=(2, 6) if f else (), seed=seed + 5)


def oliveira_arco(t, seed, f):
    """Ramo em arco, como um pedaço de coroa, contornando o canto."""
    cx, cy, R = -30, 1600, 470
    arco = [(cx + R * math.cos(math.radians(g)), cy + R * math.sin(math.radians(g))) for g in range(-96, -2, 2)]
    galho(t, arco, 6, 2.2, 54, 120, 85, 16, 12, azeitonas=(3, 6, 10) if f else (), seed=seed, abertura=0.55)
    arco_pontilhado(t, cx, cy, R * 0.8, math.radians(-88), math.radians(-6), 24, 3.6)


def oliveira_coroa(t, seed, f):
    """Meia coroa: dois ramos que nascem juntos no centro, embaixo, e sobem abertos para os lados."""
    cx, cy, R = 500, 1150, 390
    esq = [(cx + R * math.cos(math.radians(g)), cy + R * math.sin(math.radians(g))) for g in range(94, 196, 2)]
    dir_ = [(cx + R * math.cos(math.radians(g)), cy + R * math.sin(math.radians(g))) for g in range(86, -16, -2)]
    galho(t, esq, 6, 2.2, 50, 115, 80, 15, 11, azeitonas=(2, 6) if f else (), seed=seed, abertura=0.55)
    galho(t, dir_, 6, 2.2, 50, 115, 80, 15, 11, azeitonas=(4, 8) if f else (), seed=seed + 3, abertura=0.55)
    t.ponto(cx, cy + R + 4, 9)   # o laço onde os dois ramos se encontram


DESENHOS = {'oliveira_longa': oliveira_longa, 'oliveira_cruzada': oliveira_cruzada,
            'oliveira_arco': oliveira_arco, 'oliveira_coroa': oliveira_coroa}
# escala e âncora de cada desenho: o topo do ornamento fica abaixo de ~50% da altura da página
ESCALA = {'oliveira_longa': 1.3, 'oliveira_cruzada': 1.5, 'oliveira_arco': 1.45, 'oliveira_coroa': 1.02}
ANCORAS = {'oliveira_coroa': (500, 1545)}


def gerar(nome, lado, frutos, seed=7):
    global K, ANCORA
    K, ANCORA = ESCALA[nome], ANCORAS.get(nome, (0, 1545))
    t = Tela(espelho=(lado == 'dir'))
    DESENHOS[nome](t, seed, frutos)
    OUT.mkdir(exist_ok=True)
    p = OUT / f"destaque_{nome}_{lado}{'_azeitonas' if frutos else ''}.png"
    t.png(p)
    return p


def main():
    for nome in DESENHOS:
        for lado in ('esq', 'dir'):
            for frutos in (False, True):
                print(gerar(nome, lado, frutos).relative_to(ROOT))


if __name__ == '__main__':
    main()
