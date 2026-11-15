"""MSE e PSNR próprios, sem bibliotecas de métricas prontas."""
import numpy as np


def mse(referencia, imagem):
    a, b = np.asarray(referencia, dtype=np.float64), np.asarray(imagem, dtype=np.float64)
    if a.shape != b.shape or a.size == 0:
        raise ValueError('As imagens devem ter o mesmo formato e não ser vazias.')
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError('As imagens devem ter valores finitos.')
    return float(np.mean((a - b) ** 2))


def psnr(referencia, imagem, data_range=1.0):
    """10 log10(L²/MSE), com L=1 para imagens normalizadas."""
    if not np.isfinite(data_range) or data_range <= 0:
        raise ValueError('data_range deve ser positivo e finito.')
    erro = mse(referencia, imagem)
    return float('inf') if erro == 0 else float(10 * np.log10(data_range ** 2 / erro))
