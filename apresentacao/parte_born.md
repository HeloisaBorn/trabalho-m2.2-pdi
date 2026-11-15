# Seção da Born — roteiro de apresentação (aproximadamente 3 minutos)

## Slide 1 — Imagem e ruído

- VOC2012, `2009_003974`, RGB 500 × 335, original sem anotações.
- Ruído gaussiano: sigma 0,08 em [0,1], seed 42, seguido de clipping.
- Comparação controlada: mesma imagem e mesmo ruído em todas as execuções.

Figura: `resultados/frequencia/comparacao_imagens.png`.

## Slide 2 — Filtragem na frequência

- FFT por canal, máscara radial própria e transformada inversa.
- Gaussiano e Butterworth de ordem 2, com 11 cortes por família.
- Padding refletido de 32 pixels e recorte ao tamanho original.

Figura: `resultados/frequencia/espectros_mascara.png`.

## Slide 3 — Resultado e limites

- PSNR: 22.61 dB com ruído e 26.12 dB após filtragem.
- Gaussiano, corte 0,25 ciclos/pixel, ganho de 3.51 dB.
- Escolha com referência limpa nesta imagem/seed. A melhoria na segmentação ainda depende da avaliação de Gustavo.

Figura: `resultados/frequencia/psnr_por_corte.png`; recorte de contorno como apoio.

## Perguntas para ensaiar

- Por que passa-baixa pode ajudar e também prejudicar? Ruído e bordas compartilham altas frequências.
- O que é a inversa? Reconstrói a imagem espacial a partir do espectro complexo filtrado.
- Por que L=1 no PSNR? Os valores estão normalizados em [0,1].
- Por que preservar a fase? A fase contém informação espacial indispensável à reconstrução.
- Por que não medir segmentação com PSNR? Ele mede diferenças de intensidade contra uma referência, não a correção dos rótulos.
- Qual código precisa saber explicar? Ruído, máscara, FFT/inversa, padding, PSNR e seleção dos parâmetros.

As figuras e os números estão prontos para incorporar à apresentação conjunta. Os três slides editáveis estão em `apresentacao/parte_born.pptx`. Este roteiro acompanha a seção da Born; a apresentação completa ainda depende das outras frentes.
