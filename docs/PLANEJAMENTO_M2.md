# Planejamento da M2 — grupo de três pessoas

Proposta inicial em 12/11/2026. Integrantes: Born, Gustavo e João Paulo.

## Requisitos confirmados no Trabalho M2.pdf

- Entrega: 16/11/2026 até 18h59, sem atraso.
- Python; funções prontas de filtragem e operações pontuais não são aceitas. A contagem de objetos deve ter implementação própria.
- Parte 1: imagem do BSD500 ou VOC2012; ruído gaussiano ou speckle; filtro no domínio da frequência, espectros antes/depois e transformada inversa; PSNR e SSIM opcional; Watershed e SLIC; comparação de regiões, contornos e resultados com metodologia explícita.
- Parte 2: usar as duas imagens indicadas no enunciado; escala de cinza; limiar global ou Otsu; análise de falhas; fechamento, preenchimento de buracos e abertura; contagem própria antes/depois; imagens originais, binárias, processadas e rótulos coloridos.
- Notebook .ipynb pré-executado, relatório acadêmico em PDF e slides. Enviar os materiais e o link do código na disciplina.
- Caso a entrega do código seja por repositório, mantê-lo público e disponível desde a entrega.
- Apresentação de 10 a 15 minutos; todos devem dominar todas as partes. O professor pode escolher quem explica e testar outra imagem.

## Divisão de responsabilidades

| Responsável | Implementação e experimentos | Entregáveis | Documentação |
|---|---|---|---|
| Born | Selecionar imagem BSD500/VOC2012, gerar ruído reprodutível, implementar máscara Gaussiana ou Butterworth na frequência, aplicar FFT/inversa, calcular PSNR | `src/frequencia.py`, `src/metricas.py`, `notebooks/rascunhos/01_frequencia.ipynb`, espectros e tabela de parâmetros/PSNR | Método e resultados da filtragem; slides correspondentes; README e dependências; montar tabelas/painéis comparativos e consolidar notebook final |
| Gustavo | Watershed e SLIC; comparar execução sobre imagem original, ruidosa e filtrada; medir regiões e sobrepor contornos | `src/segmentacao.py`, `notebooks/rascunhos/02_segmentacao.ipynb`, mapas de rótulos, contornos e tabela comparativa | Método e discussão da segmentação; slides correspondentes |
| João Paulo | Preparar as duas imagens celulares; limiarização, erosão/dilatação, fechamento/abertura, preenchimento e rotulagem/contagem próprios | `src/morfologia.py`, `src/contagem.py`, `notebooks/rascunhos/03_celulas.ipynb`, etapas e contagens para cada imagem | Método e resultados celulares; slides correspondentes; consolidar relatório com as seções fornecidas pelos colegas |

Cada pessoa entrega código, figuras, parâmetros, explicação e limitações de sua parte. Consolidar o relatório ou notebook não significa escrever sozinho o trabalho de todos. Gustavo concentra os dois segmentadores. Para equilibrar, Born assume integração final e montagem das comparações; João Paulo consolida o relatório com os textos de todos.

## Acordos para integrar

- Usar NumPy e Matplotlib como base; implementar explicitamente os algoritmos centrais. FFT via NumPy é uma proposta técnica a validar com a orientação da disciplina, pois o enunciado não especifica essa operação isoladamente.
- Implementar Watershed, SLIC e morfologia com base nos conceitos e exemplos didáticos, citando adaptações. Isso é uma escolha conservadora do grupo; a proibição textual explícita cobre filtros, operações pontuais e contagem própria.
- Padronizar imagens RGB e cinza como float em [0, 1], máscaras booleanas e mapas de rótulos inteiros. Converter no carregamento; indicar claramente fundo e bordas em cada algoritmo.
- Born entrega imagem original, ruidosa e filtrada com mesmas dimensões e parâmetros/seed. Gustavo pode começar com a imagem original sem esperar a filtragem.
- Calcular PSNR contra a imagem limpa original, usando o mesmo intervalo de intensidades. PSNR avalia restauração, não prova qualidade da segmentação.
- Manter parâmetros de Watershed/SLIC controlados nas comparações; registrar alterações. Contar rótulos válidos, excluindo fundo/bordas conforme convenção.
- Para células, registrar contagem após limiarização, fechamento, preenchimento e abertura. Preenchimento isolado pode não alterar a quantidade; não forçar melhoria. Fechamento pode unir células vizinhas, e objetos conectados não são necessariamente células individuais.
- Definir conectividade e elemento estruturante; justificar seus tamanhos. Validar rotulagem e preenchimento em pequenas máscaras com resposta conhecida.
- Manter entradas parametrizáveis para testar imagens diferentes durante a apresentação.

## Organização sugerida do repositório

Repositório: https://github.com/HeloisaBorn/trabalho-m2.2-pdi

```text
README.md
requirements.txt
.gitignore
src/
  frequencia.py
  metricas.py
  segmentacao.py
  morfologia.py
  contagem.py
notebooks/
  trabalho_m2_2.ipynb
  rascunhos/
    01_frequencia.ipynb
    02_segmentacao.ipynb
    03_celulas.ipynb
data/
  README.md
  originais/
resultados/
  frequencia/
  segmentacao/
  celulas/
docs/
  PLANEJAMENTO_M2.md
  TAREFAS.md
relatorio/
  relatorio.md
  relatorio.pdf
apresentacao/
  roteiro_slides.md
  slides.pdf
```

O README de dados registra fontes, nomes e instruções de obtenção. Verificar condições de redistribuição antes de publicar imagens. Evitar subir datasets inteiros e os PDFs de aula; referenciar as fontes.

Uma branch por frente: `feat/frequencia`, `feat/segmentacao`, `feat/celulas`. Integrar por pull requests revisados por outro integrante. Trabalhar em notebooks separados e atribuir a edição do notebook final à Born evita conflitos. Todos revisam e executam a versão consolidada.

## Issues iniciais sugeridas

1. [Todos] Escolher imagem natural e localizar as duas imagens celulares.
2. [Born] Preparar dados, ambiente e README; documentar seed e intervalos de intensidade.
3. [Born] Implementar ruído, filtro na frequência, espectros, inversa e PSNR.
4. [Gustavo] Implementar e verificar Watershed e SLIC em exemplos pequenos.
5. [Gustavo] Comparar segmentação nas três condições e explicar a análise dos contornos.
6. [João Paulo] Implementar limiarização e operadores morfológicos.
7. [João Paulo] Implementar preenchimento e contagem; comparar etapas nas duas imagens.
8. [Todos] Entregar textos e figuras; consolidar relatório e slides.
9. [Born + revisão de todos] Executar notebook final do início ao fim em ambiente limpo.
10. [Todos] Ensaiar, conferir acesso público e enviar entrega completa.

Uma tarefa está concluída quando código executa, parâmetros estão registrados, resultados foram salvos, explicação foi escrita e outro integrante revisou.

## Cronograma proposto

| Data | Meta |
|---|---|
| 12/11 | Definir responsáveis, obter as imagens, estabelecer interfaces e criar repositório |
| 13/11 | Ter uma primeira execução funcional de cada frente e integrar filtragem com segmentação |
| 14/11 | Finalizar experimentos, revisar algoritmos e produzir figuras/textos |
| 15/11 | Consolidar notebook, relatório e slides; executar tudo e ensaiar |
| 16/11 até 17h | Meta interna para envio e conferência dos links; prazo oficial às 18h59 |

Ensaio sugerido de 12 minutos: contexto (1), filtragem (3), Watershed/SLIC (3), células (3), conclusões e limitações (2). Todos devem conseguir explicar os algoritmos das outras frentes.

## Fontes e pendências

- Fonte normativa principal: `Trabalho M2.pdf`, disponível na pasta do projeto.
- Repositório: https://github.com/VielF/ColabProjects/tree/main/PDI
- O notebook `Prática - Algoritmos de Segmentação.ipynb` contém exemplos didáticos explícitos de Otsu, Watershed e SLIC. Revisar e validar adaptações, sem presumir que o exemplo está pronto para a entrega.
- `Watershed.py` contém implementação por alagamento; possui trecho de execução com `scipy.misc.imsave`, que exige adaptação para ambientes atuais.
- `Exemplo_Morfologia.ipynb` demonstra chamadas prontas do OpenCV; serve como referência conceitual, mas o grupo deve respeitar as restrições do trabalho ao escolher sua implementação.
- Materiais locais de apoio: filtragem no domínio da frequência, processamento morfológico, segmentação/descrição e métricas de qualidade. Esta proposta não representa revisão integral de todos esses PDFs.
- Notion informado: https://private-zinc-3e1.notion.site/Processamento-Digital-de-Imagens-42c3c2abd8654404b1a1e05d70fa5eb0. Não acessível pelo conector nem pela consulta pública nesta sessão; conteúdo não incorporado.
- Os links do PDF foram recuperados examinando objetos internos, pois não apareciam nas anotações das páginas. Imagem 1: `gap-region-filling.tif`; Imagem 2: `002f20ad-2ace-499c-9335-c9080bc3e6b5.png`, ambas em `VielF/ColabProjects/dataset/OperacaoMorfologia`. URLs completos em `data/README.md`. Imagens ainda precisam ser baixadas; selecionar também uma imagem BSD500/VOC2012.
- Repositório remoto criado pela Born: https://github.com/HeloisaBorn/trabalho-m2.2-pdi. Commit e push serão feitos pela própria Born. Usuários GitHub de Gustavo e João Paulo ainda não informados.
