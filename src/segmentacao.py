"""Segmentação da Parte 1: Watershed por inundação com marcadores, SLIC e
comparação de contornos.

Base: "Prática - Algoritmos de Segmentação.ipynb" (prof. Felipe Viel) e, para a
convolução, src/filtros.py do trabalho M2 anterior do grupo. Adaptações citadas
em cada função. Entradas em float [0, 1]; rótulos inteiros, 0 = sem rótulo.
"""
from collections import deque
from heapq import heappop, heappush

import numpy as np

VIZINHOS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def para_cinza(rgb):
    """RGB -> cinza com os pesos da ITU-R BT.601 (o olho é mais sensível ao verde)."""
    if rgb.ndim == 2:
        return rgb
    return rgb @ np.array([0.299, 0.587, 0.114])


def convolve2d(image, kernel):
    """Correlação 2D sem laços (trabalho M2 anterior). Adaptação: padding 'edge' em vez
    de zeros, para a moldura da imagem não virar uma borda falsa no gradiente."""
    kh, kw = kernel.shape
    padded = np.pad(image.astype(np.float64), ((kh // 2, kh // 2), (kw // 2, kw // 2)), mode='edge')
    janelas = np.lib.stride_tricks.sliding_window_view(padded, (kh, kw))
    return np.einsum('ijkl,kl->ij', janelas, kernel)


def gradiente_sobel(cinza):
    """Magnitude do gradiente de Sobel: o "relevo" que o Watershed inunda.

    Sem normalizar pelo máximo: assim original, ruidosa e filtrada ficam na mesma
    escala (0 a 4·√2 para entrada em [0, 1]) e o mesmo limiar vale para as três.
    """
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    gx = convolve2d(cinza, kx)
    gy = convolve2d(cinza, kx.T)
    return np.hypot(gx, gy)


def rotular_componentes(mascara):
    """Rotula as regiões conexas (8-vizinhança) de uma máscara booleana por busca em
    largura. Devolve (rótulos, quantidade); fundo = 0.

    Usa listas do Python em vez de indexar o array pixel a pixel: o mesmo algoritmo,
    cerca de 4x mais rápido (acesso a um elemento de lista é mais barato que no NumPy).
    """
    h, w = mascara.shape
    m = mascara.tolist()
    rotulos = [[0] * w for _ in range(h)]
    atual = 0
    for i, j in zip(*np.nonzero(mascara)):
        i, j = int(i), int(j)
        if rotulos[i][j]:
            continue
        atual += 1
        rotulos[i][j] = atual
        fila = deque([(i, j)])
        while fila:
            y, x = fila.popleft()
            for dy, dx in VIZINHOS_8:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and m[ny][nx] and not rotulos[ny][nx]:
                    rotulos[ny][nx] = atual
                    fila.append((ny, nx))
    return np.array(rotulos, dtype=np.int32), atual


def marcadores(gradiente, limiar, area_min):
    """Marcadores = regiões planas (gradiente <= limiar) com pelo menos `area_min` pixels.

    Cada marcador é uma "fonte de água". Sem esse filtro, todo mínimo local, inclusive
    os criados pelo ruído, viraria uma região: a supersegmentação clássica do Watershed.
    `<=` e não `<`: em imagens com fundo liso o percentil pode ser 0, e `< 0` não marca nada.
    """
    rotulos, _ = rotular_componentes(gradiente <= limiar)
    areas = np.bincount(rotulos.ravel())
    pequenos = areas < area_min
    pequenos[0] = False
    rotulos[pequenos[rotulos]] = 0
    # Renumera somente regiões positivas. Quando toda a imagem é um marcador,
    # não existe fundo 0 em unique: return_inverse o transformaria em fundo.
    presentes = np.unique(rotulos)
    presentes = presentes[presentes > 0]
    mapa = np.zeros(len(areas), dtype=np.int32)
    mapa[presentes] = np.arange(1, len(presentes) + 1)
    return mapa[rotulos]


def watershed(relevo, marcas):
    """Inundação a partir dos marcadores com fila de prioridade (aula).

    O pixel mais baixo ainda não processado sai primeiro da fila e passa seu rótulo
    aos vizinhos sem rótulo, então cada bacia cresce "subindo" pelo relevo e para
    onde encontra outra. O contador desempata níveis iguais na ordem de chegada (FIFO).

    Adaptação: a versão da aula marcava a fronteira com -1 durante a inundação, e esse
    -1 se espalhava para os vizinhos ainda não rotulados. Aqui todo pixel recebe uma
    bacia e as fronteiras são calculadas depois, em `contornos`.
    """
    if relevo.shape != marcas.shape:
        raise ValueError('O relevo e os marcadores devem ter o mesmo formato.')
    if not np.any(marcas > 0):
        raise ValueError('Nenhum marcador positivo. Reduza frac_area ou ajuste o percentil dos marcadores.')
    h, w = relevo.shape
    altura = relevo.tolist()  # listas: mesmo motivo de rotular_componentes
    rotulos = marcas.tolist()
    fila, ordem = [], 0
    for i, j in zip(*np.nonzero(marcas)):
        i, j = int(i), int(j)
        heappush(fila, (altura[i][j], ordem, i, j))
        ordem += 1
    while fila:
        _, _, i, j = heappop(fila)
        for dy, dx in VIZINHOS_8:
            ni, nj = i + dy, j + dx
            if 0 <= ni < h and 0 <= nj < w and rotulos[ni][nj] == 0:
                rotulos[ni][nj] = rotulos[i][j]
                heappush(fila, (altura[ni][nj], ordem, ni, nj))
                ordem += 1
    return np.array(rotulos, dtype=np.int32)


def segmentar_watershed(imagem, percentil=75, frac_area=0.001):
    """Pipeline completo para qualquer imagem (RGB ou cinza, float em [0, 1]).

    Os parâmetros são relativos à própria imagem, para valerem em qualquer entrada:
    - limiar = percentil do gradiente: os `percentil`% pixels mais planos podem virar
      marcador, em vez de um valor fixo que depende do contraste e do ruído;
    - área mínima = fração do total de pixels, em vez de um número fixo de pixels.
    Devolve (gradiente, marcadores, rótulos).
    """
    grad = gradiente_sobel(para_cinza(imagem))
    marcas = marcadores(grad, np.percentile(grad, percentil), max(1, round(frac_area * grad.size)))
    return grad, marcas, watershed(grad, marcas)


def slic(imagem, n_superpixels=200, m=10, iteracoes=10):
    """SLIC da aula: k-means local em que cada pixel se junta ao centro mais próximo
    em cor e posição, D = sqrt(dc² + (m/S)²·ds²), procurando só numa janela 2S×2S.

    - S = sqrt(N/K): lado esperado de cada superpixel; centros iniciais numa grade de passo S.
    - m: compacidade. Grande = a posição pesa mais (blocos regulares); pequeno = a cor
      pesa mais (contornos seguem as bordas, formas irregulares).
    Cores na escala 0-255, como no exemplo da aula, para m ~ 10 ter o mesmo efeito.
    Adaptação: cada janela é calculada de uma vez com NumPy, em vez de pixel a pixel.
    Devolve rótulos 1..K (0 = pixel não alcançado por nenhuma janela).
    """
    img = np.asarray(imagem, dtype=np.float64) * 255.0
    if img.ndim == 2:
        img = img[..., None]
    h, w, canais = img.shape
    S = max(1, int(np.sqrt(h * w / n_superpixels)))
    grade_y, grade_x = np.mgrid[S // 2:h:S, S // 2:w:S]
    centros = np.column_stack([grade_y.ravel(), grade_x.ravel()]).astype(np.float64)
    cores = img[grade_y.ravel(), grade_x.ravel()]
    k_total = len(centros)
    yy, xx = np.mgrid[0:h, 0:w]

    for _ in range(iteracoes):
        # Atribuição: cada pixel fica com o centro de menor D entre as janelas que o cobrem.
        rotulos = np.zeros((h, w), dtype=np.int32)
        dist = np.full((h, w), np.inf)
        for k, ((yc, xc), cor) in enumerate(zip(centros, cores), start=1):
            y0, y1 = int(max(yc - S, 0)), int(min(yc + S + 1, h))
            x0, x1 = int(max(xc - S, 0)), int(min(xc + S + 1, w))
            dc2 = ((img[y0:y1, x0:x1] - cor) ** 2).sum(axis=2)
            ds2 = (yy[y0:y1, x0:x1] - yc) ** 2 + (xx[y0:y1, x0:x1] - xc) ** 2
            d = np.sqrt(dc2 + (m / S) ** 2 * ds2)
            menor = d < dist[y0:y1, x0:x1]
            dist[y0:y1, x0:x1][menor] = d[menor]
            rotulos[y0:y1, x0:x1][menor] = k

        # Atualização: cada centro vai para a média de posição e cor dos seus pixels.
        r = rotulos.ravel()
        n = np.bincount(r, minlength=k_total + 1)[1:]
        ok = n > 0  # centro sem pixels fica onde está (como na aula)
        soma = lambda valores: np.bincount(r, valores.ravel(), k_total + 1)[1:]
        centros[ok, 0] = soma(yy)[ok] / n[ok]
        centros[ok, 1] = soma(xx)[ok] / n[ok]
        for c in range(canais):
            cores[ok, c] = soma(img[..., c])[ok] / n[ok]
    return unir_fragmentos(rotulos, S * S // 4)


def unir_fragmentos(rotulos, area_min):
    """Garante regiões conexas, como no passo final do SLIC original (Achanta et al., 2012).

    O k-means não obriga um rótulo a ser uma peça só: sobram pedacinhos soltos que
    inflariam o número de regiões. Percorre a imagem em ordem de leitura, separa cada
    componente conexo (8-vizinhança, mesmo rótulo) e, se tiver menos de `area_min`
    pixels, junta ao componente vizinho já visitado. Devolve rótulos 1..n.
    """
    h, w = rotulos.shape
    r = rotulos.tolist()
    novo = [[0] * w for _ in range(h)]
    atual = 0
    for i in range(h):
        for j in range(w):
            if novo[i][j]:
                continue
            atual += 1
            valor, vizinho = r[i][j], 0
            novo[i][j] = atual
            componente = [(i, j)]
            for y, x in componente:  # a lista cresce durante o laço: busca em largura
                for dy, dx in VIZINHOS_8:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        if not novo[ny][nx] and r[ny][nx] == valor:
                            novo[ny][nx] = atual
                            componente.append((ny, nx))
                        elif novo[ny][nx] and novo[ny][nx] != atual:
                            vizinho = novo[ny][nx]
            if len(componente) < area_min and vizinho:
                for y, x in componente:
                    novo[y][x] = vizinho
                atual -= 1
    return np.array(novo, dtype=np.int32)


def contornos(rotulos):
    """Máscara das fronteiras: pixel cujo vizinho da direita ou de baixo tem outro rótulo."""
    borda = np.zeros(rotulos.shape, dtype=bool)
    borda[:, :-1] |= rotulos[:, :-1] != rotulos[:, 1:]
    borda[:-1, :] |= rotulos[:-1, :] != rotulos[1:, :]
    return borda


def dilatar(mascara, raio):
    """Dilatação binária por um quadrado (2·raio+1)²: OU das cópias deslocadas da máscara."""
    h, w = mascara.shape
    p = np.pad(mascara, raio)
    saida = np.zeros_like(mascara)
    for dy in range(2 * raio + 1):
        for dx in range(2 * raio + 1):
            saida |= p[dy:dy + h, dx:dx + w]
    return saida


def comparar_contornos(rotulos, referencia, tolerancia=2):
    """Precisão, revocação e F1 de contorno com tolerância, como no benchmark BSDS
    (Martin et al., 2004). Um pixel de contorno "acerta" se houver contorno do outro
    lado a até `tolerancia` px (distância em quadrado):
    - precisão: fração do contorno obtido que existe na referência (baixa = bordas falsas);
    - revocação: fração do contorno da referência reencontrado (baixa = bordas perdidas).
    shortcut: sem o pareamento um-para-um do BSDS, um contorno grosso pode acertar
    várias vezes; trocar pelo pareamento se a métrica for usada contra gabarito humano.
    """
    c, ref = contornos(rotulos), contornos(referencia)
    precisao = (c & dilatar(ref, tolerancia)).sum() / max(c.sum(), 1)
    revocacao = (ref & dilatar(c, tolerancia)).sum() / max(ref.sum(), 1)
    f1 = 2 * precisao * revocacao / (precisao + revocacao) if precisao + revocacao else 0.0
    return float(precisao), float(revocacao), float(f1)
