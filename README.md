# Projeto M2.2 — Processamento Digital de Imagens

Filtragem na frequência, segmentação com Watershed/SLIC e processamento morfológico para contagem de células.

Disciplina: Processamento de Imagens — Professor Felipe Viel — Univali.

## Integrantes e responsabilidades

| Integrante | Responsabilidade | Arquivos |
|---|---|---|
| Gustavo Corrêa de Mello | Watershed, SLIC e comparação de regiões e contornos | `notebooks/rascunhos/02_segmentacao.ipynb`; módulo `src/segmentacao.py` |
| Heloisa Cavalcante Born | Ruído, filtragem na frequência, espectros, inversa e PSNR; integração do notebook | `src/frequencia.py`, `src/metricas.py`, `notebooks/rascunhos/01_frequencia.ipynb` |
| João Paulo Jorge Aimi | Limiarização, morfologia, preenchimento e contagem própria; consolidação do relatório | `notebooks/rascunhos/03_celulas.ipynb`; módulos `src/morfologia.py` e `src/contagem.py` |

## Executar

Ambiente utilizado: Python 3.12. Dependências em `requirements.txt`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/baixar_dados.py
python -m jupyterlab
```

Abrir `notebooks/trabalho_m2_2.ipynb` e executar do início ao fim: ele reúne filtragem, Watershed, SLIC, morfologia e contagem. A versão de entrega está salva com saídas. Os notebooks individuais permanecem em `notebooks/rascunhos/`.

Também é possível gerar os resultados e executar os testes pelo terminal:

```powershell
python scripts/experimento_frequencia.py
python scripts/executar_notebooks_born.py notebooks/trabalho_m2_2.ipynb
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
- As duas imagens da parte morfológica estão vinculadas na mesma documentação e são obtidas pelo mesmo script de dados.
- Resultados da filtragem: [instruções e arrays](resultados/frequencia/README.md).
- Comparação integrada: `resultados/comparacao_parte1.csv`; figuras de segmentação em `resultados/segmentacao/`.
- Morfologia e contagem: `resultados/celulas/contagem_etapas.csv` e figuras em `resultados/celulas/`.
- Relatório: [PDF](relatorio/relatorio.pdf) e [texto-fonte](relatorio/relatorio.md).
- Apresentação conjunta: [PowerPoint](apresentacao/apresentacao_final.pptx) e [PDF](apresentacao/apresentacao_final.pdf). As versões individuais foram preservadas como fontes.

O PowerPoint reúne 14 slides principais e 2 slides de apoio ocultos, com roteiro de fala nas anotações de cada slide; o PDF contém os 14 principais. Para editar o conteúdo, usar o PowerPoint.

## Desenvolvimento

[Tarefas do grupo](docs/TAREFAS.md) e [convenções dos módulos](src/README.md).

As implementações não usam funções prontas de filtragem ou operações pontuais. A contagem deve ser própria. NumPy fornece as operações numéricas e a FFT.

## Referências

- Enunciado do Trabalho M2 fornecido na disciplina.
- [Materiais do professor](https://github.com/VielF/ColabProjects/tree/main/PDI).
- [VOC2012](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/).
- [NumPy: transformada de Fourier](https://numpy.org/doc/stable/reference/routines.fft.html).
