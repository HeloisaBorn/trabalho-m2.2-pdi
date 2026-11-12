# Comparação com os trabalhos anteriores do grupo

Revisão em 12/11/2026 dos arquivos listados no GitHub e dos READMEs completos.

| Repositório | Estrutura observada |
|---|---|
| [M1.1](https://github.com/mello745/trabalho-pdi) | Código real em `source/` (README descreve `src/`), `notebooks/projeto-m1.ipynb`, `notebooks/rascunhos/`, `dataset/` e `relatorio/` |
| [M1.2](https://github.com/mello745/trabalho-pdi-m1.2) | `src/pdi/`, subdivisões por integrante, notebook principal e dois auxiliares, `data/originais/`, `resultados/`, `relatorio/` e `apresentacao/` |
| [M2 anterior](https://github.com/mello745/trabalho-m2-pdi) | Módulos por assunto em `src/`, `notebooks/trabalho_m2.ipynb`, `data/`, `resultados/` e `tests.py`; relatório externo ao repositório segundo o README |

## Ajustes aplicados nesta M2.2

- Manter módulos por assunto em `src/`, seguindo a M2 anterior.
- Nomear o notebook principal `notebooks/trabalho_m2_2.ipynb`.
- Guardar os três roteiros individuais em `notebooks/rascunhos/`, como na M1.1.
- Usar `data/originais/` e `resultados/`, como na M1.2.
- Separar `relatorio/` e `apresentacao/`, como na M1.2; manter `docs/` apenas para organização.
- Registrar nomes completos e mapa dos itens no README.
- Preservar a divisão de responsabilidades ajustada; não copiar soluções nem restrições de trabalhos diferentes.

## Diferenças importantes do enunciado

A M2 anterior usa texto, Otsu/k-means/Canny e proíbe morfologia. A M2.2 atual exige Watershed/SLIC e processamento morfológico, com contagem própria. Portanto, a estrutura pode ser semelhante, mas a restrição antiga contra morfologia não se aplica e a chamada pronta de contagem do trabalho anterior não atende ao requisito atual.

A revisão comparou organização e documentação; não auditou a correção integral dos códigos anteriores.
