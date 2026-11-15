# Projeto M2.2 — Processamento Digital de Imagens

Filtragem na frequência, segmentação com Watershed/SLIC e processamento morfológico para contagem de células.

Disciplina: Processamento de Imagens — Professor Felipe Viel — Univali.

## Integrantes e responsabilidades

| Integrante | Responsabilidade | Arquivos |
|---|---|---|
| Heloisa Cavalcante Born | Ruído, filtragem na frequência, espectros, inversa e PSNR; integração do notebook | `src/frequencia.py`, `src/metricas.py`, `notebooks/rascunhos/01_frequencia.ipynb` |
| Gustavo Corrêa de Mello | Watershed, SLIC e comparação de regiões e contornos | `notebooks/rascunhos/02_segmentacao.ipynb`; módulo `src/segmentacao.py` |
| João Paulo Jorge Aimi | Limiarização, morfologia, preenchimento e contagem própria; consolidação do relatório | `notebooks/rascunhos/03_celulas.ipynb`; módulos `src/morfologia.py` e `src/contagem.py` a implementar |

## Executar

Ambiente utilizado: Python 3.12. Dependências em `requirements.txt`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/baixar_imagem_voc2012.py
python -m jupyterlab
```

Abrir `notebooks/trabalho_m2_2.ipynb` para executar a Parte 1 integrada: filtragem, Watershed, SLIC e comparação. O notebook identifica a Parte 2 (morfologia e contagem) ainda pendente. Os notebooks individuais permanecem em `notebooks/rascunhos/`.

Também é possível gerar os resultados e executar os testes pelo terminal:

```powershell
python scripts/experimento_frequencia.py
python scripts/executar_notebooks_born.py
python -m unittest discover -s tests -v
```

Para testar outra imagem sem substituir os resultados oficiais:

```powershell
python scripts/experimento_frequencia.py --imagem CAMINHO_DA_IMAGEM --destino resultados/teste
```

## Estrutura

```text
src/              Implementações dos algoritmos
scripts/          Obtenção da imagem, experimentos e execução dos notebooks
notebooks/        Notebook principal e desenvolvimento por frente
data/             Imagens, fontes e metadados
resultados/       Imagens, espectros, tabelas e arrays dos experimentos
tests/            Verificações matemáticas
relatorio/        Relatório do trabalho
apresentacao/     Slides
docs/             Tarefas de desenvolvimento
```

## Dados e resultados

- Imagem natural: **`2009_003974.jpg`**, VOC2012, RGB 500 × 335, conjunto de treino. Fonte, justificativa e reprodução em [dados](data/README.md).
- As duas imagens da parte morfológica estão vinculadas na mesma documentação.
- Resultados da filtragem: [instruções e arrays](resultados/frequencia/README.md).
- Comparação integrada: `resultados/comparacao_parte1.csv`; figuras de segmentação em `resultados/segmentacao/`.
- Relatório: [texto](relatorio/relatorio.md).
- Slides disponíveis: `apresentacao/parte_born.pptx` e `apresentacao/parte_gustavo.pptx`.

## Desenvolvimento

[Tarefas do grupo](docs/TAREFAS.md) e [convenções dos módulos](src/README.md).

As implementações não usam funções prontas de filtragem ou operações pontuais. A contagem deve ser própria. NumPy fornece as operações numéricas e a FFT.

## Referências

- Enunciado do Trabalho M2 fornecido na disciplina.
- [Materiais do professor](https://github.com/VielF/ColabProjects/tree/main/PDI).
- [VOC2012](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/).
- [NumPy: transformada de Fourier](https://numpy.org/doc/stable/reference/routines.fft.html).
