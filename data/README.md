# Imagens e fontes

Imagens utilizadas no trabalho, conforme as fontes indicadas no enunciado.

## Parte 1 — imagem escolhida: carro azul (VOC2012)

- [BSD500, conforme link do enunciado](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/).
- [VOC2012, conforme link do enunciado](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/).

Escolha confirmada: **`2009_003974.jpg`**, correspondente à prévia **`car_04`**.

- Arquivo local: `data/originais/2009_003974.jpg`, original limpo, sem caixas ou textos desenhados.
- Dimensões: **500 × 335 pixels**, RGB.
- Dataset: VOC2012, listas `ImageSets/Main/train.txt` e `trainval.txt`; classe `car` positiva. A imagem é herdada do VOC2009, conforme o XML, e está efetivamente incluída no pacote VOC2012.
- Fonte: [pacote oficial VOC2012](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar), membro `VOCdevkit/VOC2012/JPEGImages/2009_003974.jpg`.
- Justificativa: um carro grande, sem oclusão na anotação, fundo claro e quase uniforme; bom ponto de partida para estudar ruído, filtragem e contornos. Reflexos, rodas, janelas e sombra continuam sendo desafios.
- O JPEG foi extraído do arquivo oficial sem edição, recorte ou remoção artificial de marcações. Correspondência visual com a prévia conferida.
- `segmented=0` no XML: não há máscara de segmentação declarada para esta imagem. Usar comparação visual/metodologia de contornos; não inventar métricas contra uma máscara inexistente.
- XML, SHA-256, caminho no pacote e evidências de split estão em `data/metadados/2009_003974.xml` e `.json`.

Para obter a mesma imagem em outro computador, executar na raiz do projeto:

```powershell
python scripts/baixar_dados.py
```

O script baixa somente os bytes do JPEG no pacote oficial e valida o SHA-256. Se o servidor deixar de oferecer leitura parcial, baixar o pacote e extrair o membro acima. A imagem local permanece ignorada pelo Git; o script e os metadados permitem reproduzir a obtenção.

## Parte 2 — as duas imagens exigidas

| Identificação no PDF | Nome do arquivo | Fonte |
|---|---|---|
| Imagem 1 | `gap-region-filling.tif` | [GitHub do professor](https://github.com/VielF/ColabProjects/blob/main/dataset/OperacaoMorfologia/gap-region-filling.tif) |
| Imagem 2 | `002f20ad-2ace-499c-9335-c9080bc3e6b5.png` | [GitHub do professor](https://github.com/VielF/ColabProjects/blob/main/dataset/OperacaoMorfologia/002f20ad-2ace-499c-9335-c9080bc3e6b5.png) |

Para baixar os arquivos originais (não o HTML da página) em `data/originais/`, executar na raiz do projeto:

```powershell
curl.exe -L -o data/originais/gap-region-filling.tif https://raw.githubusercontent.com/VielF/ColabProjects/main/dataset/OperacaoMorfologia/gap-region-filling.tif
curl.exe -L -o data/originais/002f20ad-2ace-499c-9335-c9080bc3e6b5.png https://raw.githubusercontent.com/VielF/ColabProjects/main/dataset/OperacaoMorfologia/002f20ad-2ace-499c-9335-c9080bc3e6b5.png
```

- Imagem 1: TIFF em cinza 8 bits, 512 × 512, já binária (só 0 e 255). Anéis brancos com buraco central em fundo preto; alguns cortados pela borda e dois encostados.
- Imagem 2: PNG RGB, 1600 × 1200. Esfregaço de sangue corado: hemácias roxas, com centro claro, em fundo branco, e uma célula maior escura no centro.

O texto cita BBBC006 como exemplo; usar os dois arquivos efetivamente vinculados, sem substituí-los automaticamente. Antes de interpretar o resultado como contagem de células, examinar o conteúdo real de cada imagem e discutir eventuais limitações.

Os dados locais estão ignorados pelo Git por padrão. Registrar fontes e condições de redistribuição antes de publicar arquivos; manter instruções de obtenção para reprodução. Não incluir datasets inteiros.
