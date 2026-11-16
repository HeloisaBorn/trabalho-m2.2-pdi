"""Parte 2: pré-processamento, limiarização (global e Otsu) e morfologia binária
(erosão, dilatação, abertura, fechamento e preenchimento de buracos).

Tudo implementado com NumPy, sem funções prontas de filtragem, limiarização ou
morfologia. Convenções do grupo (src/README.md): imagens em float [0, 1] e
máscaras booleanas, em que True = objeto (núcleo) e False = fundo.
"""
import numpy as np

from .segmentacao import para_cinza

NIVEIS = 256  # níveis de cinza usados no histograma do Otsu


# --------------------------------------------------------------------------
# 1. Pré-processamento
# --------------------------------------------------------------------------

def filtro_gaussiano(cinza, sigma=1.0):
    """Suavização gaussiana leve (etapa opcional do enunciado) para reduzir ruído
    antes de limiarizar.

    O núcleo gaussiano 2D é separável: filtrar as linhas com um núcleo 1D e depois
    as colunas com o mesmo núcleo dá o mesmo resultado da convolução 2D, com custo
    2k em vez de k² por pixel. Raio de 3·sigma cobre ~99,7% da área da gaussiana.
    Borda replicada ('edge') para a moldura não escurecer. sigma <= 0 não filtra.
    """
    cinza = np.asarray(cinza, dtype=np.float64)
    if sigma <= 0:
        return cinza
    raio = max(1, int(np.ceil(3 * sigma)))
    x = np.arange(-raio, raio + 1)
    nucleo = np.exp(-(x ** 2) / (2 * sigma ** 2))
    nucleo /= nucleo.sum()  # soma 1: preserva o brilho médio

    def convoluir_linhas(img):
        p = np.pad(img, ((0, 0), (raio, raio)), mode='edge')
        janelas = np.lib.stride_tricks.sliding_window_view(p, len(nucleo), axis=1)
        return janelas @ nucleo

    return convoluir_linhas(convoluir_linhas(cinza).T).T


# --------------------------------------------------------------------------
# 2. Limiarização
# --------------------------------------------------------------------------

def histograma(cinza, niveis=NIVEIS):
    """Histograma de uma imagem float [0, 1] quantizada em `niveis` níveis."""
    q = np.clip(np.rint(np.asarray(cinza, dtype=np.float64) * (niveis - 1)), 0, niveis - 1)
    return np.bincount(q.astype(np.int64).ravel(), minlength=niveis)


def limiar_otsu(cinza, niveis=NIVEIS):
    """Limiar de Otsu, devolvido na escala [0, 1].

    Para cada limiar t possível, os pixels se dividem em duas classes (<= t e > t).
    Otsu escolhe o t que maximiza a variância ENTRE as classes:
        sigma_b²(t) = w0(t) · w1(t) · (mu0(t) - mu1(t))²
    em que w são as proporções de pixels e mu as médias de cada classe. Maximizar a
    variância entre classes equivale a minimizar a variância dentro delas. As somas
    acumuladas do histograma dão w e mu de todos os t de uma vez.
    """
    hist = histograma(cinza, niveis).astype(np.float64)
    p = hist / hist.sum()                # probabilidade de cada nível
    nivel = np.arange(niveis)
    w0 = np.cumsum(p)                    # proporção da classe <= t
    w1 = 1.0 - w0
    soma0 = np.cumsum(p * nivel)         # soma parcial das intensidades
    total = soma0[-1]                    # média global
    with np.errstate(divide='ignore', invalid='ignore'):
        mu0 = soma0 / w0
        mu1 = (total - soma0) / w1
        var_entre = w0 * w1 * (mu0 - mu1) ** 2
    var_entre = np.nan_to_num(var_entre)  # classe vazia (w = 0) não é candidata
    # Em empates (planalto entre dois picos), fica com o meio do planalto.
    melhores = np.flatnonzero(var_entre == var_entre.max())
    # +0,5: a classe 0 do histograma é "nível arredondado <= t", ou seja, cinza
    # abaixo de (t + 0,5)/(niveis - 1); assim `cinza > limiar` separa as mesmas classes.
    return float((melhores.mean() + 0.5) / (niveis - 1))


def limiarizar(cinza, limiar=None, objeto_claro=True):
    """Imagem binária a partir do cinza. Devolve (máscara, limiar usado).

    - limiar=None: usa Otsu; um número em [0, 1]: limiarização global fixa.
    - objeto_claro=True: objeto = pixels acima do limiar (núcleos claros em fundo
      escuro, fluorescência). False inverte, para objetos escuros em fundo claro.
    """
    cinza = para_cinza(np.asarray(cinza, dtype=np.float64))
    if limiar is None:
        limiar = limiar_otsu(cinza)
    mascara = cinza > limiar if objeto_claro else cinza <= limiar
    return mascara, float(limiar)


# --------------------------------------------------------------------------
# 3. Elemento estruturante e operações básicas
# --------------------------------------------------------------------------

def elemento_estruturante(raio=1, forma='disco'):
    """Elemento estruturante booleano de lado 2·raio+1, com origem no centro.

    - 'quadrado': todos os pixels (8-vizinhança quando raio=1);
    - 'cruz': só a linha e a coluna centrais (4-vizinhança quando raio=1);
    - 'disco': pixels a até `raio` do centro; o mais isotrópico, combina com núcleos
      arredondados (com raio=1 o disco coincide com a cruz).
    """
    y, x = np.mgrid[-raio:raio + 1, -raio:raio + 1]
    if forma == 'quadrado':
        return np.ones((2 * raio + 1, 2 * raio + 1), dtype=bool)
    if forma == 'cruz':
        return (y == 0) | (x == 0)
    if forma == 'disco':
        return y ** 2 + x ** 2 <= raio ** 2
    raise ValueError("forma deve ser 'quadrado', 'cruz' ou 'disco'.")


def _como_elemento(ee):
    """Aceita um elemento pronto (array) ou um raio inteiro (vira disco)."""
    if np.isscalar(ee):
        return elemento_estruturante(int(ee), 'disco')
    ee = np.asarray(ee, dtype=bool)
    if ee.ndim != 2 or ee.shape[0] % 2 == 0 or ee.shape[1] % 2 == 0:
        raise ValueError('O elemento estruturante deve ser 2D com lados ímpares.')
    return ee


def dilatar(mascara, ee=1):
    """Dilatação: o pixel vira objeto se o elemento, centrado nele, TOCA o objeto.

    Implementação: OU lógico das cópias da máscara deslocadas por cada posição ativa
    do elemento (um laço sobre o elemento, não sobre os pixels). O elemento é
    refletido, como na definição A ⊕ B; para elementos simétricos não muda nada.
    Fora da imagem conta como fundo. Efeito: engrossa objetos e fecha vãos.
    """
    mascara = np.asarray(mascara, dtype=bool)
    ee = _como_elemento(ee)
    h, w = mascara.shape
    ry, rx = ee.shape[0] // 2, ee.shape[1] // 2
    p = np.pad(mascara, ((ry, ry), (rx, rx)), constant_values=False)
    saida = np.zeros((h, w), dtype=bool)
    for dy, dx in zip(*np.nonzero(ee[::-1, ::-1])):
        saida |= p[dy:dy + h, dx:dx + w]
    return saida


def erodir(mascara, ee=1):
    """Erosão: o pixel continua objeto só se o elemento, centrado nele, CABE
    inteiro no objeto.

    Implementação: E lógico das cópias deslocadas. Fora da imagem conta como objeto,
    para a moldura não corroer células cortadas pela borda; assim o fechamento
    nunca apaga pixels e a abertura nunca cria. Efeito: afina objetos e remove os
    menores que o elemento.
    """
    mascara = np.asarray(mascara, dtype=bool)
    ee = _como_elemento(ee)
    h, w = mascara.shape
    ry, rx = ee.shape[0] // 2, ee.shape[1] // 2
    p = np.pad(mascara, ((ry, ry), (rx, rx)), constant_values=True)
    saida = np.ones((h, w), dtype=bool)
    for dy, dx in zip(*np.nonzero(ee)):
        saida &= p[dy:dy + h, dx:dx + w]
    return saida


def abrir(mascara, ee=1):
    """Abertura = erosão seguida de dilatação. Remove partículas e pontes menores
    que o elemento e devolve aos objetos restantes quase o tamanho original."""
    ee = _como_elemento(ee)
    return dilatar(erodir(mascara, ee), ee)


def fechar(mascara, ee=1):
    """Fechamento = dilatação seguida de erosão. Une fragmentos próximos e fecha
    frestas menores que o elemento. Cuidado: também pode fundir células vizinhas,
    o que reduz a contagem."""
    ee = _como_elemento(ee)
    return erodir(dilatar(mascara, ee), ee)


# --------------------------------------------------------------------------
# 4. Preenchimento de buracos (gap-filling)
# --------------------------------------------------------------------------

def preencher_buracos(mascara, conectividade_fundo=4):
    """Preenche os buracos internos dos objetos.

    Buraco = região de fundo que não consegue chegar à borda da imagem. Algoritmo
    (preenchimento de regiões por dilatação condicional, Gonzalez & Woods):
        X0 = pixels de fundo na borda da imagem
        Xk = (Xk-1 ⊕ B) ∩ Aᶜ      até Xk = Xk-1
    Ou seja: "inunda" o fundo de fora para dentro, sem nunca atravessar o objeto A.
    O que a inundação não alcança é buraco: resultado = complemento de X final.

    conectividade_fundo=4 (B em cruz) é o par correto para objetos em 8-vizinhança:
    a água não passa por frestas diagonais, por onde o objeto está conectado.
    Devolve a máscara preenchida; os buracos são `preenchida & ~mascara`.
    """
    mascara = np.asarray(mascara, dtype=bool)
    if conectividade_fundo not in (4, 8):
        raise ValueError('conectividade_fundo deve ser 4 ou 8.')
    b = elemento_estruturante(1, 'cruz' if conectividade_fundo == 4 else 'quadrado')
    fundo = ~mascara
    inundado = np.zeros_like(mascara)
    inundado[0, :] = fundo[0, :]
    inundado[-1, :] = fundo[-1, :]
    inundado[:, 0] = fundo[:, 0]
    inundado[:, -1] = fundo[:, -1]
    while True:
        novo = dilatar(inundado, b) & fundo
        if np.array_equal(novo, inundado):
            return ~inundado
        inundado = novo


# --------------------------------------------------------------------------
# 5. Pipeline do enunciado
# --------------------------------------------------------------------------

def segmentar_celulas(imagem, sigma=1.0, limiar=None, objeto_claro=True,
                      raio_fechamento=2, raio_abertura=2, forma='disco'):
    """Executa as etapas 1 a 4 do enunciado e devolve todas as intermediárias,
    para o notebook exibir e contar cada uma.

    Ordem: cinza -> gaussiano leve -> limiarização (Otsu se limiar=None) ->
    fechamento (conecta fragmentos) -> preenchimento de buracos -> abertura
    (remove partículas). Raio 0 pula a operação correspondente.

    Devolve um dicionário com: 'cinza', 'suavizada', 'limiar', 'binaria',
    'fechada', 'preenchida' e 'aberta' (máscara final).
    """
    cinza = para_cinza(np.asarray(imagem, dtype=np.float64))
    suavizada = filtro_gaussiano(cinza, sigma)
    binaria, limiar = limiarizar(suavizada, limiar, objeto_claro)
    fechada = fechar(binaria, elemento_estruturante(raio_fechamento, forma)) if raio_fechamento else binaria
    preenchida = preencher_buracos(fechada)
    aberta = abrir(preenchida, elemento_estruturante(raio_abertura, forma)) if raio_abertura else preenchida
    return {'cinza': cinza, 'suavizada': suavizada, 'limiar': limiar, 'binaria': binaria,
            'fechada': fechada, 'preenchida': preenchida, 'aberta': aberta}
