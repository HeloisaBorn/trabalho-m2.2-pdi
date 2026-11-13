# Projeto M2.2 — Processamento Digital de Imagens

Filtragem na frequência, segmentação com Watershed/SLIC e processamento morfológico para contagem de células.

Disciplina: Processamento de Imagens — Professor Felipe Viel — Univali.

**Entrega oficial: 16/11/2026 até 18h59.** Meta interna: envio até 17h.

## Integrantes

- Heloisa Cavalcante Born
- Gustavo Corrêa de Mello
- João Paulo Jorge Aimi

## Equipe e divisão

| Integrante | Responsabilidades |
|---|---|
| Born | Ruído, filtro na frequência, espectros, inversa e PSNR; montagem das tabelas/painéis comparativos e integração do notebook final |
| Gustavo | Watershed e SLIC; comparação das segmentações, regiões e contornos; interpretação dos resultados |
| João Paulo | Limiarização, morfologia, preenchimento de buracos e contagem própria nas duas imagens celulares; consolidação do relatório |

Cada integrante entrega o código, as figuras, o texto e os slides da sua seção. Todos revisam o trabalho completo e devem saber explicar todas as partes.

## Estado inicial

Este repositório contém a organização e os roteiros de desenvolvimento. A imagem natural original escolhida já está disponível localmente. Os algoritmos, experimentos, duas imagens da Parte 2, resultados, relatório PDF e slides ainda precisam ser produzidos. Os notebooks iniciais não são a entrega pré-executada.

## Executar localmente

Recomendação de ambiente: Python 3.11 ou superior.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyterlab
```

Abrir os notebooks de cada frente e executar a célula de configuração. A imagem `data/originais/2009_003974.jpg` já está disponível localmente. Em outro computador, obtê-la com `python scripts/baixar_imagem_voc2012.py`. As fontes estão em `data/README.md`. O notebook final deverá importar os módulos de `src/` e executar as duas partes do trabalho do início ao fim.

## Estrutura

```text
src/                  Módulos dos algoritmos (a implementar)
notebooks/            trabalho_m2_2.ipynb (entrega) e rascunhos/ (individuais)
data/                 Fontes e imagens de entrada
resultados/           Figuras e tabelas dos experimentos
relatorio/            Texto e PDF do relatório
apresentacao/         Roteiro e slides
docs/                 Planejamento, tarefas e catálogo de imagens
```

Consulte [planejamento](docs/PLANEJAMENTO_M2.md), [tarefas](docs/TAREFAS.md) e [acordos técnicos](src/README.md).

## Trabalho em grupo

Usar branches `feat/frequencia` (Born), `feat/segmentacao` (Gustavo) e `feat/celulas` (João Paulo). Cada pessoa edita seu notebook em `notebooks/rascunhos/`; Born consolida `trabalho_m2_2.ipynb`. Integrar por pull request com revisão de outro integrante. Não atribuir código de colegas a si próprio.

## Checklist de entrega

- [ ] Parte 1 com imagem BSD500/VOC2012, ruído, filtro na frequência, espectros e inversa
- [ ] PSNR contra a imagem original limpa; SSIM opcional
- [ ] Watershed e SLIC, regiões e contornos comparados com metodologia explícita
- [ ] Parte 2 com as duas imagens celulares indicadas pelo professor
- [ ] Limiarização, fechamento, preenchimento e abertura documentados
- [ ] Contagem própria antes/depois e rótulos coloridos
- [ ] Notebook final executado integralmente, com saídas salvas
- [ ] Relatório acadêmico PDF e slides
- [ ] Repositório público e acessível; materiais enviados na disciplina
- [ ] Ensaio de 10 a 15 minutos e revisão por todos

## Referências

- Enunciado `Trabalho M2.pdf` fornecido na disciplina (referência normativa).
- [Materiais do professor](https://github.com/VielF/ColabProjects/tree/main/PDI).
- [Página da disciplina](https://private-zinc-3e1.notion.site/Processamento-Digital-de-Imagens-42c3c2abd8654404b1a1e05d70fa5eb0) — acesso pendente de conferência pelo grupo.

Funções prontas de filtragem e operações pontuais não são aceitas; a contagem deve ser própria. A proposta é também implementar os algoritmos centrais de segmentação e morfologia, citando os exemplos adaptados. O trabalho anterior do grupo já usa FFT do NumPy; esta proposta mantém essa abordagem, sujeita às orientações do enunciado atual. Os PDFs de aula não estão incluídos neste repositório.

## Mapa dos itens do enunciado

| Item | Implementação prevista | Responsável |
|---|---|---|
| Ruído, filtro na frequência, espectros e inversa | `src/frequencia.py` | Born |
| PSNR (SSIM opcional) | `src/metricas.py` | Born |
| Watershed e SLIC | `src/segmentacao.py` | Gustavo |
| Comparação das regiões e contornos | `notebooks/rascunhos/02_segmentacao.ipynb` | Gustavo; painéis por Born |
| Limiarização e morfologia | `src/morfologia.py` | João Paulo |
| Contagem própria e comparação por etapa | `src/contagem.py` | João Paulo |
| Integração das duas partes e resultados | `notebooks/trabalho_m2_2.ipynb` | Born, com revisão de todos |
| Relatório e apresentação | `relatorio/` e `apresentacao/` | Todos |

Os módulos listados são arquivos planejados, ainda não implementados.

## Dados indicados no PDF

- Parte 1: escolher uma imagem de [BSD500](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) ou [VOC2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/).
- Parte 2: [Imagem 1 — gap-region-filling.tif](https://github.com/VielF/ColabProjects/blob/main/dataset/OperacaoMorfologia/gap-region-filling.tif) e [Imagem 2 — 002f20ad-2ace-499c-9335-c9080bc3e6b5.png](https://github.com/VielF/ColabProjects/blob/main/dataset/OperacaoMorfologia/002f20ad-2ace-499c-9335-c9080bc3e6b5.png).

Links recuperados dos objetos internos do PDF. Ver instruções em `data/README.md`.

## Escolha da imagem VOC2012

Avaliação visual de 14 candidatos em [catálogo de opções](docs/catalogo_voc2012/LEIA-ME.md). Escolha confirmada: **`car_04` → `2009_003974.jpg`**, original VOC2012 disponível localmente (500 × 335, RGB, split de treino). Fonte, justificativa e reprodução em `data/README.md`. As fotos de prévia ficam locais, ignoradas pelo Git.
