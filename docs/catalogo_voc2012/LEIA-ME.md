# Catálogo visual de candidatos — VOC2012

Revisão em 12/11/2026. Foram inspecionadas as 160 miniaturas da galeria oficial vinculada à página VOC2012; 14 candidatos foram examinados ampliados. Esta seleção não é uma revisão de todas as imagens do dataset.

**Recomendação:** `car_04` para começar com menos dificuldade; `aeroplane_03` como alternativa; `cat_03` se o grupo preferir gato. `cat_06` é possível, mas difícil e não é a escolha mais segura para uma primeira implementação.

As dificuldades são julgamentos visuais relativos a esta seleção, não resultados medidos de Watershed/SLIC. A filtragem e a segmentação ainda não foram executadas. “Mais fácil” não significa segmentação perfeita.

## Atenção às prévias

Estas são imagens anotadas da galeria, com caixas e textos amarelos. Servem somente para escolher a cena. Não utilizar essas cópias na filtragem, PSNR ou segmentação: as marcações introduzem contornos artificiais.

`cat_06`, `car_04` etc. são aliases da galeria, não IDs originais confirmados em `JPEGImages/`. Depois de escolher, localizar a versão limpa no pacote VOC2012, registrar seu ID, conferir a presença no split pretendido e, se desejar referência de contorno, a disponibilidade da máscara. O mapeamento para o ID original ainda está pendente; os arquivos deste catálogo não são a entrada final.

A própria página VOC2012 aponta para uma galeria cujo título interno ainda diz VOC2011. A documentação informa o reaproveitamento das imagens de classificação/detecção de 2011. Isso explica a galeria, mas não prova por si só que cada exemplo tenha máscara de segmentação pública.

## Critérios utilizados

- Objeto grande e com pouca sobreposição.
- Bom contraste com o fundo.
- Pouca textura, sombras fortes e detalhes finos.
- Grandes regiões homogêneas, úteis para mostrar efeito de ruído e filtragem.

Watershed pode criar muitas regiões por causa de textura e ruído. SLIC gera superpixels: não reconhecerá automaticamente um gato ou cachorro, nem produzirá necessariamente um único rótulo para cada animal. Comparar regiões e contornos com parâmetros controlados, conforme o enunciado.

## Comparação

| Prévia | Cena | Dificuldade visual | Principal cuidado |
|---|---|---|---|
| [car_04](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/car_04.jpg) | Carro azul de perfil | Mais fácil | Janelas, rodas, reflexos e sombra ainda produzem regiões internas. |
| [aeroplane_03](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/aeroplane_03.jpg) | Avião em voo | Mais fácil | Fuselagem clara tem contraste menor com o céu; asas e motores criam detalhes. |
| [cat_03](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/cat_03.jpg) | Gato de frente | Intermediária | Pelagem multicolorida, bigodes e bordas escuras próximas do fundo. |
| [boat_08](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/boat_08.jpg) | Barco branco com vegetação ao fundo | Intermediária | Vegetação e água têm textura; mastros e estruturas finas. |
| [bird_08](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/bird_08.jpg) | Ave branca em primeiro plano | Intermediária | Galhos, partes cortadas pelo enquadramento e região clara podem fragmentar o objeto. |
| [sofa_03](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/sofa_03.jpg) | Sofá escuro | Intermediária | Couro com reflexos, almofadas, janela muito clara e móveis nas bordas. |
| [tvmonitor_06](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/tvmonitor_06.jpg) | Monitor CRT visto de frente | Intermediária | Texto na tela e tecido ao fundo geram detalhes; cores escuras próximas. |
| [aeroplane_04](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/aeroplane_04.jpg) | Avião na pista ao entardecer | Intermediária | Avião próximo da linha do horizonte, gradiente de iluminação e partes escuras. |
| [cat_08](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/cat_08.jpg) | Gato com iluminação lateral | Difícil | Sombra forte mistura parte do gato ao fundo; bigodes e pelos finos. |
| [cow_05](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/cow_05.jpg) | Vaca próxima da câmera | Difícil | Arame cruza a cena; manchas dividem o animal; contraste varia muito. |
| [boat_03](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/boat_03.jpg) | Veleiro pequeno no mar | Difícil | Objeto pequeno, água texturizada e mastro muito fino. |
| [dog_03](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/dog_03.jpg) | Cachorro deitado na grama | Difícil | Grama muito texturizada; cachorro relativamente pequeno e parcialmente parecido com o fundo. |
| [dog_07](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/dog_07.jpg) | Cachorro sentado com pessoa ao lado | Difícil | Pessoa próxima, partes sobrepostas e fundo de ambiente com vários elementos. |
| [cat_06](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/images/cat_06.jpg) | Gato parcialmente coberto por cachorro | Difícil | Dois animais sobrepostos; gato parcialmente oculto; fundo camuflado; tons semelhantes e pelos. |

## Avaliação da cat_06

Eu não escolheria para a primeira implementação. SLIC separa regiões locais, não entende gato/cachorro; Watershed pode fragmentar a pelagem e misturar fronteiras.

Dois animais sobrepostos; gato parcialmente oculto; fundo camuflado; tons semelhantes e pelos. A dificuldade não impede usar a cena: ela aumenta o tempo de ajuste e pode gerar resultados mais difíceis de explicar. A cat_03 preserva o tema de gato com menos sobreposição.

## Próximo passo depois da escolha

1. Obter a imagem original sem caixas/textos e registrar o ID de `JPEGImages/`.
2. Confirmar que pertence à edição VOC2012; se usar máscara, confirmar o par e excluir pixels void da avaliação.
3. Preservar a imagem limpa como referência do PSNR e definir seed, intensidade do ruído e escala de processamento.
4. Fazer um ensaio pequeno com a implementação do grupo antes de fixar a escolha. Examinar se o filtro reduz ruído sem apagar contornos e se os segmentadores executam em tempo adequado.

## Fontes

- [Página oficial VOC2012](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/).
- [Galeria de classificação/detecção](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/examples/index.html).
- [Exemplos com máscaras](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/segexamples/index.html).

As cópias em `previas/` são reproduções de exemplos anotados da fonte oficial para consulta local. Conferir termos das imagens antes de republicar o catálogo com fotos; não assumir que o dataset inteiro tem uma única licença livre.

## Escolha confirmada

O original da `car_04` foi localizado: **`2009_003974.jpg`**, RGB 500 × 335, presente no pacote oficial VOC2012 e no split Main/train. Disponível em `data/originais/`. A pendência de ID/original descrita na triagem está resolvida para esta candidata. Não há máscara declarada no XML. Detalhes em `data/README.md`.
