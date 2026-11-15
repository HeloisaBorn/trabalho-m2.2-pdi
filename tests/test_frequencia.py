"""Verificações matemáticas independentes para frequência e PSNR."""
import unittest
import numpy as np
from src.frequencia import ruido_gaussiano, filtrar_frequencia, mascara_passa_baixa
from src.metricas import mse, psnr


class FrequenciaTests(unittest.TestCase):
    def test_psnr_conhecido_e_identidade(self):
        a = np.zeros((8, 8)); b = np.full((8, 8), 0.1)
        self.assertAlmostEqual(mse(a, b), 0.01)
        self.assertAlmostEqual(psnr(a, b), 20)
        self.assertEqual(psnr(a, a), float('inf'))

    def test_escala_psnr(self):
        a = np.zeros((4, 4)); b = np.full((4, 4), 0.2)
        self.assertAlmostEqual(psnr(a, b), psnr(a * 255, b * 255, 255))

    def test_ruido_reprodutivel_e_estatistica(self):
        a = np.full((512, 512), 0.5)
        b = ruido_gaussiano(a, 0.04, 123)
        np.testing.assert_array_equal(b, ruido_gaussiano(a, 0.04, 123))
        self.assertLess(abs((b-a).mean()), 0.0005)
        self.assertAlmostEqual((b-a).std(), 0.04, delta=0.0005)
        np.testing.assert_array_equal(a, ruido_gaussiano(a, 0, 123))

    def test_constante_dc_e_formatos_impares(self):
        for shape in [(31, 47), (31, 47, 3)]:
            a = np.full(shape, 0.37)
            for tipo in ['gaussiano', 'butterworth']:
                b, info = filtrar_frequencia(a, tipo=tipo)
                np.testing.assert_allclose(b, a, atol=1e-12)
                self.assertLess(info['residuo_imaginario_max'], 1e-12)

    def test_resposta_a_senoide(self):
        # Senoide exata da grade FFT: ganho teórico H(f) sem padding.
        n = 64; f = 8 / n; corte = 0.1
        a = np.tile(0.5 + 0.2 * np.cos(2*np.pi*f*np.arange(n)), (n, 1))
        b, _ = filtrar_frequencia(a, corte=corte, padding=0)
        esperado = 0.5 + (a-0.5)*np.exp(-f*f/(2*corte*corte))
        np.testing.assert_allclose(b, esperado, atol=1e-12)

    def test_resposta_butterworth_no_corte(self):
        h = mascara_passa_baixa((64, 64), corte=0.125, tipo='butterworth')
        self.assertAlmostEqual(h[32, 40], 0.5)
        self.assertAlmostEqual(h[32, 32], 1)

    def test_validacao(self):
        with self.assertRaises(ValueError): filtrar_frequencia(np.full((8, 8), np.nan))
        with self.assertRaises(ValueError): mascara_passa_baixa((8, 8), corte=0)
        with self.assertRaises(ValueError): mse(np.zeros((3, 3)), np.zeros((4, 4)))


if __name__ == '__main__': unittest.main()
