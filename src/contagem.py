"""Parte 2: contagem própria de objetos por rotulagem de componentes conexos,
medidas por objeto e rótulos coloridos.

Sem contadores prontos (nada de scipy.ndimage.label, cv2.connectedComponents ou
skimage.measure.label). Máscaras booleanas (True = objeto); rótulos inteiros,
0 = fundo e 1..n = objetos, numerados na ordem de leitura da imagem.
"""
from collections import deque

import numpy as np

VIZINHOS_4 = [(-1, 0), (0, -1), (0, 1), (1, 0)]
VIZINHOS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def rotular(mascara, conectividade=8):
    """Rotula os componentes conexos de uma máscara. Devolve (rótulos, quantidade).

    Algoritmo (busca em largura / flood fill):
    1. percorre a imagem em ordem de leitura;
    2. ao achar um pixel de objeto ainda sem rótulo, abre um novo rótulo e o coloca
       numa fila;
    3. tira um pixel da fila e dá o mesmo rótulo aos vizinhos de objeto ainda sem
       rótulo, que também entram na fila;
    4. fila vazia = objeto inteiro rotulado; volta ao passo 1.
    Cada pixel entra na fila uma única vez: custo linear no número de pixels.

    conectividade=8 considera vizinhos diagonais como o mesmo objeto; 4 só os
    laterais (separa objetos que se tocam apenas pela quina).
    Listas do Python no lugar de indexar o array pixel a pixel: mesmo algoritmo,
    bem mais rápido.
    """
    if conectividade not in (4, 8):
        raise ValueError('conectividade deve ser 4 ou 8.')
    vizinhos = VIZINHOS_8 if conectividade == 8 else VIZINHOS_4
    mascara = np.asarray(mascara, dtype=bool)
    h, w = mascara.shape
    m = mascara.tolist()
    rotulos = [[0] * w for _ in range(h)]
    atual = 0
    for i, j in zip(*np.nonzero(mascara)):  # nonzero já vem em ordem de leitura
        i, j = int(i), int(j)
        if rotulos[i][j]:
            continue
        atual += 1
        rotulos[i][j] = atual
        fila = deque([(i, j)])
        while fila:
            y, x = fila.popleft()
            for dy, dx in vizinhos:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and m[ny][nx] and not rotulos[ny][nx]:
                    rotulos[ny][nx] = atual
                    fila.append((ny, nx))
    return np.array(rotulos, dtype=np.int32), atual


def areas(rotulos):
    """Área em pixels de cada objeto: vetor de tamanho n, posição k-1 = rótulo k."""
    return np.bincount(np.asarray(rotulos).ravel())[1:]


def remover_pequenos(rotulos, area_min):
    """Descarta objetos com menos de `area_min` pixels e renumera os restantes em
    1..n, mantendo a ordem. Devolve (rótulos, quantidade)."""
    rotulos = np.asarray(rotulos)
    manter = np.concatenate([[False], areas(rotulos) >= area_min])
    mapa = np.zeros(len(manter), dtype=np.int32)
    mapa[manter] = np.arange(1, manter.sum() + 1)
    return mapa[rotulos], int(manter.sum())


def contar_objetos(mascara, conectividade=8, area_min=1):
    """Contagem automática: número de componentes conexos com pelo menos `area_min`
    pixels. Devolve (quantidade, rótulos)."""
    rotulos, n = rotular(mascara, conectividade)
    if area_min > 1:
        rotulos, n = remover_pequenos(rotulos, area_min)
    return n, rotulos


def medidas(rotulos):
    """Uma linha por objeto: rótulo, área, centroide (linha, coluna) e caixa
    delimitadora (y0, x0, y1, x1, com y1 e x1 inclusivos). Útil para tabelas e para
    escrever o número de cada célula na figura."""
    rotulos = np.asarray(rotulos)
    r = rotulos.ravel()
    n = int(r.max()) if r.size else 0
    if n == 0:
        return []
    yy, xx = np.indices(rotulos.shape)
    area = np.bincount(r, minlength=n + 1)[1:]
    cy = np.bincount(r, yy.ravel(), n + 1)[1:] / np.maximum(area, 1)
    cx = np.bincount(r, xx.ravel(), n + 1)[1:] / np.maximum(area, 1)
    linhas = []
    for k in range(1, n + 1):
        if area[k - 1] == 0:
            continue
        ys, xs = np.nonzero(rotulos == k)
        linhas.append({'rotulo': k, 'area': int(area[k - 1]),
                       'centroide': (float(cy[k - 1]), float(cx[k - 1])),
                       'caixa': (int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max()))})
    return linhas


def colorir_rotulos(rotulos, seed=0, fundo=(0.0, 0.0, 0.0)):
    """Imagem RGB float [0, 1] com uma cor por rótulo (fundo na cor `fundo`).

    As cores vêm de matizes espalhados pelo passo do ângulo áureo: rótulos
    consecutivos (células vizinhas na ordem de leitura) recebem cores bem
    diferentes, e a mesma `seed` reproduz sempre a mesma figura.
    """
    rotulos = np.asarray(rotulos)
    n = int(rotulos.max()) if rotulos.size else 0
    matiz = (np.random.default_rng(seed).random() + np.arange(n) * 0.61803398875) % 1.0
    paleta = np.empty((n + 1, 3))
    paleta[0] = fundo
    paleta[1:] = _hsv_para_rgb(matiz, 0.85, 0.95)
    return paleta[rotulos]


def _hsv_para_rgb(h, s, v):
    """HSV -> RGB vetorizado (h em [0, 1), s e v escalares)."""
    k = (np.array([5.0, 3.0, 1.0])[None, :] + h[:, None] * 6.0) % 6.0
    return v - v * s * np.clip(np.minimum(k, 4.0 - k), 0.0, 1.0)


def comparar_etapas(etapas, conectividade=8, area_min=1):
    """Conta os objetos em cada etapa do pipeline, para a tabela "antes e depois".

    `etapas`: dicionário {nome: máscara booleana}, na ordem do processamento, por
    exemplo {'limiarização': binaria, 'fechamento': fechada, ...}.
    Devolve uma lista de dicionários com nome, contagem, pixels de objeto e a
    variação da contagem em relação à etapa anterior.
    """
    linhas, anterior = [], None
    for nome, mascara in etapas.items():
        n, _ = contar_objetos(mascara, conectividade, area_min)
        linhas.append({'etapa': nome, 'objetos': n, 'pixels_objeto': int(np.sum(mascara)),
                       'variacao': None if anterior is None else n - anterior})
        anterior = n
    return linhas
