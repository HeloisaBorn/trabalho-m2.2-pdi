"""Ruído e passa-baixa na frequência, implementados com operações NumPy.

Convenção: imagens reais em [0, 1], HxW ou HxWx3; frequência em ciclos/pixel.
NumPy calcula a FFT; as funções de filtragem não usam filtros prontos.
"""
import numpy as np


def validar_imagem(imagem):
    x = np.asarray(imagem, dtype=np.float64)
    if x.ndim not in (2, 3) or min(x.shape[:2]) < 2:
        raise ValueError('Esperada imagem HxW ou HxWx3, com dimensões >= 2.')
    if x.ndim == 3 and x.shape[2] != 3:
        raise ValueError('Imagens coloridas devem ser RGB.')
    if not np.all(np.isfinite(x)) or x.min() < 0 or x.max() > 1:
        raise ValueError('A imagem deve conter valores finitos em [0, 1].')
    return x


def ruido_gaussiano(imagem, sigma=0.08, seed=42):
    """Soma N(0,sigma²) independente por pixel/canal e limita em [0,1]."""
    x = validar_imagem(imagem)
    if not np.isfinite(sigma) or sigma < 0:
        raise ValueError('sigma deve ser finito e não negativo.')
    rng = np.random.default_rng(seed)
    return np.clip(x + rng.normal(0, sigma, x.shape), 0, 1)


def mascara_passa_baixa(shape, corte=0.12, tipo='gaussiano', ordem=2):
    """Máscara centrada. H_G=exp(-D²/(2D0²)); H_B=1/(1+(D/D0)^(2n)).

    D é distância radial em ciclos/pixel. No Gaussiano, corte é o desvio
    da resposta radial (H(D0)=exp(-1/2)); no Butterworth, H(D0)=1/2.
    """
    if len(shape) != 2 or any(int(v) != v or v < 2 for v in shape):
        raise ValueError('shape deve conter duas dimensões inteiras >= 2.')
    if not np.isfinite(corte) or not 0 < corte <= np.sqrt(0.5):
        raise ValueError('corte deve estar entre 0 e sqrt(0.5) ciclos/pixel.')
    fy = np.fft.fftshift(np.fft.fftfreq(shape[0]))
    fx = np.fft.fftshift(np.fft.fftfreq(shape[1]))
    d2 = fy[:, None] ** 2 + fx[None, :] ** 2
    if tipo == 'gaussiano':
        return np.exp(-d2 / (2 * corte ** 2))
    if tipo == 'butterworth':
        if not isinstance(ordem, (int, np.integer)) or ordem < 1:
            raise ValueError('ordem deve ser inteiro positivo.')
        return 1 / (1 + (d2 / corte ** 2) ** ordem)
    raise ValueError('tipo deve ser gaussiano ou butterworth.')


def filtrar_frequencia(imagem, corte=0.12, tipo='gaussiano', ordem=2, padding=32):
    """FFT2 por canal, máscara manual, IFFT2 real e recorte ao tamanho original.

    Espelhamento reduz descontinuidades de borda da extensão periódica da FFT.
    Retorna a imagem limitada em [0,1] e os espectros complexos antes/depois,
    além da máscara, para inspeção. Não normaliza o resultado por min/max.
    """
    x = validar_imagem(imagem)
    if not isinstance(padding, (int, np.integer)) or padding < 0:
        raise ValueError('padding deve ser inteiro não negativo.')
    widths = [(padding, padding), (padding, padding)] + ([(0, 0)] if x.ndim == 3 else [])
    padded = np.pad(x, widths, mode='reflect') if padding else x
    h = mascara_passa_baixa(padded.shape[:2], corte, tipo, ordem)
    f = np.fft.fftshift(np.fft.fft2(padded, axes=(0, 1)), axes=(0, 1))
    g = f * (h[..., None] if x.ndim == 3 else h)
    inversa = np.fft.ifft2(np.fft.ifftshift(g, axes=(0, 1)), axes=(0, 1))
    real = inversa.real
    if padding:
        real = real[padding:-padding, padding:-padding]
    return np.clip(real, 0, 1), {
        'mascara': h, 'espectro_antes': f, 'espectro_depois': g,
        'residuo_imaginario_max': float(np.abs(inversa.imag).max()),
    }
