"""Confere morfologia e contagem da Parte 2 em entradas pequenas com resposta conhecida.

Uso (na raiz do projeto): python -m unittest discover -s tests -v
"""
import unittest

import numpy as np

from src.contagem import colorir_rotulos, comparar_etapas, contar_objetos, medidas, rotular
from src.morfologia import (abrir, dilatar, elemento_estruturante, erodir, fechar, limiar_otsu,
                            limiarizar, preencher_buracos, segmentar_celulas)


def anel(n=9):
    """Quadrado 5x5 com um buraco de 1 pixel no centro."""
    m = np.zeros((n, n), dtype=bool)
    m[2:7, 2:7] = True
    m[4, 4] = False
    return m


class MorfologiaTests(unittest.TestCase):
    def test_dilatar_e_erodir_seguem_a_definicao(self):
        # Elemento assimétrico: só confere com a definição se a reflexão estiver certa.
        ee = np.array([[0, 1, 1], [0, 1, 0], [0, 0, 0]], dtype=bool)
        a = np.random.default_rng(0).random((10, 12)) < 0.4
        h, w = a.shape
        desloc = [(y - 1, x - 1) for y, x in zip(*np.nonzero(ee))]
        dil = np.zeros_like(a)
        ero = np.ones_like(a)
        for y in range(h):
            for x in range(w):
                for dy, dx in desloc:
                    if 0 <= y - dy < h and 0 <= x - dx < w and a[y - dy, x - dx]:
                        dil[y, x] = True  # A ⊕ B: algum b com (y, x) - b em A
                    if 0 <= y + dy < h and 0 <= x + dx < w and not a[y + dy, x + dx]:
                        ero[y, x] = False  # A ⊖ B: B transladado cabe em A
        np.testing.assert_array_equal(dilatar(a, ee), dil)
        np.testing.assert_array_equal(erodir(a, ee), ero)

    def test_fechamento_so_acrescenta_e_abertura_so_remove(self):
        a = np.random.default_rng(1).random((30, 30)) < 0.5
        self.assertTrue(np.all(fechar(a, 2) >= a))
        self.assertTrue(np.all(abrir(a, 2) <= a))

    def test_abertura_remove_particula_menor_que_o_elemento(self):
        m = np.zeros((15, 15), dtype=bool)
        m[2:9, 2:9] = True   # objeto 7x7: sobrevive ao disco de raio 2
        m[12, 12] = True     # ruído de 1 pixel
        aberta = abrir(m, elemento_estruturante(2, 'disco'))
        self.assertFalse(aberta[12, 12])
        self.assertTrue(aberta[5, 5])

    def test_fechamento_une_fragmentos(self):
        m = np.zeros((9, 15), dtype=bool)
        m[2:7, 2:7] = True
        m[2:7, 8:13] = True  # fresta de 1 coluna entre os dois
        self.assertEqual(contar_objetos(m)[0], 2)
        self.assertEqual(contar_objetos(fechar(m, elemento_estruturante(1, 'quadrado')))[0], 1)

    def test_preencher_buraco_interno(self):
        cheio = preencher_buracos(anel())
        self.assertTrue(cheio[4, 4])
        self.assertEqual(int(cheio.sum()), 25)

    def test_fundo_em_4_nao_vaza_pela_diagonal(self):
        # Losango ligado só pelas quinas: é um objeto em 8-vizinhança e tem buraco.
        m = np.zeros((7, 7), dtype=bool)
        for y, x in [(1, 3), (2, 2), (2, 4), (3, 1), (3, 5), (4, 2), (4, 4), (5, 3)]:
            m[y, x] = True
        self.assertTrue(preencher_buracos(m, 4)[3, 3])
        self.assertFalse(preencher_buracos(m, 8)[3, 3])

    def test_buraco_aberto_para_a_borda_nao_e_preenchido(self):
        m = anel()
        m[4, 2:5] = False  # canal do buraco até fora do objeto
        np.testing.assert_array_equal(preencher_buracos(m), m)

    def test_otsu_separa_duas_populacoes(self):
        cinza = np.r_[np.full(500, 0.2), np.full(500, 0.7)]
        mascara, limiar = limiarizar(cinza.reshape(20, 50))
        self.assertTrue(0.2 < limiar < 0.7)
        self.assertEqual(int(mascara.sum()), 500)
        self.assertAlmostEqual(limiar_otsu(np.r_[np.zeros(10), np.ones(10)]), 0.5)

    def test_pipeline_conta_um_objeto_por_celula_oca(self):
        img = np.zeros((40, 40))
        img[5:15, 5:15] = 1.0
        img[9:11, 9:11] = 0.0      # célula oca
        img[25:35, 22:32] = 1.0
        etapas = segmentar_celulas(img, sigma=0, raio_fechamento=1, raio_abertura=1)
        self.assertTrue(etapas['preenchida'][10, 10])
        self.assertEqual(contar_objetos(etapas['aberta'])[0], 2)


class ContagemTests(unittest.TestCase):
    def test_conectividade_4_e_8(self):
        m = np.eye(4, dtype=bool)  # diagonal: um objeto em 8, quatro em 4
        self.assertEqual(rotular(m, 8)[1], 1)
        self.assertEqual(rotular(m, 4)[1], 4)

    def test_rotulos_em_ordem_de_leitura_e_area_minima(self):
        m = np.zeros((6, 6), dtype=bool)
        m[0, 4:6] = True   # 2 pixels, aparece primeiro na leitura
        m[3:6, 0:3] = True  # 9 pixels
        n, rot = contar_objetos(m)
        self.assertEqual(n, 2)
        self.assertEqual(rot[0, 5], 1)
        n, rot = contar_objetos(m, area_min=3)
        self.assertEqual(n, 1)
        self.assertEqual(rot[4, 1], 1)  # renumerado para 1, sem buraco na numeração

    def test_medidas_e_cores(self):
        m = np.zeros((5, 5), dtype=bool)
        m[1:4, 1:4] = True
        _, rot = contar_objetos(m)
        (obj,) = medidas(rot)
        self.assertEqual(obj['area'], 9)
        self.assertEqual(obj['centroide'], (2.0, 2.0))
        self.assertEqual(obj['caixa'], (1, 1, 3, 3))
        cores = colorir_rotulos(rot)
        np.testing.assert_array_equal(cores[0, 0], [0, 0, 0])
        self.assertTrue(np.all((cores >= 0) & (cores <= 1)))

    def test_comparar_etapas(self):
        um = np.zeros((5, 5), dtype=bool)
        um[1:4, 1:4] = True
        dois = um.copy()
        dois[:, 2] = False
        linhas = comparar_etapas({'a': dois, 'b': um})
        self.assertEqual([l['objetos'] for l in linhas], [2, 1])
        self.assertEqual(linhas[1]['variacao'], -1)


if __name__ == '__main__':
    unittest.main()
