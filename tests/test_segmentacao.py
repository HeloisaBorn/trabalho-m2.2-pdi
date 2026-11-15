"""Confere a segmentação em entradas pequenas com resposta conhecida.

Uso (na raiz do projeto): python -m unittest discover -s tests -v
"""
import unittest

import numpy as np

from src.segmentacao import (comparar_contornos, contornos, dilatar, gradiente_sobel, marcadores,
                             rotular_componentes, segmentar_watershed, slic, unir_fragmentos,
                             watershed)


class WatershedTests(unittest.TestCase):
    def test_gradiente_degrau(self):
        # Metade preta, metade branca: o gradiente só aparece nas duas colunas da
        # transição; com padding de zeros apareceria também na moldura.
        degrau = np.zeros((5, 6))
        degrau[:, 3:] = 1
        np.testing.assert_allclose(gradiente_sobel(degrau), [[0, 0, 4, 4, 0, 0]] * 5)

    def test_rotulagem_8_vizinhanca(self):
        # Dois blocos separados e um pixel encostado na diagonal do primeiro.
        m = np.zeros((4, 6), dtype=bool)
        m[0:2, 0:2] = True
        m[2, 2] = True
        m[0:2, 4:6] = True
        r, n = rotular_componentes(m)
        self.assertEqual(n, 2)
        self.assertEqual(r[2, 2], r[0, 0])
        self.assertNotEqual(r[0, 4], r[0, 0])

    def test_inundacao_para_na_crista(self):
        # Duas bacias planas separadas por uma crista na coluna 3.
        relevo = np.zeros((5, 7))
        relevo[:, 3] = 9
        marcas = np.zeros((5, 7), dtype=np.int32)
        marcas[2, 0], marcas[2, 6] = 1, 2
        r = watershed(relevo, marcas)
        self.assertTrue((r[:, :3] == 1).all() and (r[:, 4:] == 2).all() and (r > 0).all())
        self.assertTrue(contornos(r)[:, 2:4].any() and not contornos(r)[:, :2].any())

    def test_marcadores_descarta_regiao_pequena(self):
        g = np.ones((6, 6))
        g[0:3, 0:3] = 0  # 9 pixels planos
        g[5, 5] = 0      # 1 pixel plano
        mk = marcadores(g, limiar=0.5, area_min=4)
        self.assertEqual(set(np.unique(mk)), {0, 1})
        self.assertTrue((mk[0:3, 0:3] == 1).all())
        self.assertEqual(mk[5, 5], 0)

    def test_pipeline_em_cinza(self):
        # Dois quadrados planos separados por uma borda forte: todo pixel recebe
        # uma bacia e as duas metades ficam em regiões diferentes.
        cinza = np.zeros((40, 40))
        cinza[:, 20:] = 1
        _, mk, r = segmentar_watershed(cinza)
        self.assertEqual(mk.max(), 2)
        self.assertTrue((r > 0).all())
        self.assertNotEqual(r[0, 0], r[0, 39])


class SlicTests(unittest.TestCase):
    def test_fronteira_na_troca_de_cor(self):
        duas_cores = np.zeros((20, 40))
        duas_cores[:, 20:] = 1
        r = slic(duas_cores, n_superpixels=2)
        self.assertEqual(r.max(), 2)
        self.assertTrue((r[:, :20] == r[0, 0]).all() and (r[:, 20:] == r[0, 39]).all())

    def test_unir_fragmentos(self):
        # Um pixel do rótulo 1 isolado dentro do rótulo 2 é absorvido pelo vizinho.
        frag = np.full((10, 10), 2)
        frag[:, :4] = 1
        frag[7, 8] = 1
        u = unir_fragmentos(frag, area_min=4)
        self.assertEqual(u.max(), 2)
        self.assertEqual(u[7, 8], u[7, 7])
        self.assertNotEqual(u[0, 0], u[0, 9])


class MetricaTests(unittest.TestCase):
    def test_dilatacao(self):
        d = np.zeros((5, 5), dtype=bool)
        d[2, 2] = True
        self.assertEqual(dilatar(d, 1).sum(), 9)
        self.assertTrue(dilatar(d, 1)[1:4, 1:4].all())

    def test_tolerancia_de_contorno(self):
        # Fronteira na coluna 10 (referência) e na coluna 11 (deslocada 1 px).
        ref = np.ones((20, 20), dtype=int)
        ref[:, 10:] = 2
        desloc = np.ones((20, 20), dtype=int)
        desloc[:, 11:] = 2
        self.assertEqual(comparar_contornos(ref, ref), (1.0, 1.0, 1.0))
        self.assertEqual(comparar_contornos(desloc, ref, tolerancia=2), (1.0, 1.0, 1.0))
        self.assertEqual(comparar_contornos(desloc, ref, tolerancia=0)[2], 0.0)

    def test_borda_falsa_derruba_precisao(self):
        ref = np.ones((20, 20), dtype=int)
        ref[:, 10:] = 2
        extra = ref.copy()
        extra[:5, :10] = 3
        p, r, _ = comparar_contornos(extra, ref)
        self.assertEqual(r, 1.0)
        self.assertLess(p, 1.0)


if __name__ == '__main__':
    unittest.main()
