# Entrega da filtragem para Gustavo

Resultados gerados por `python scripts/experimento_frequencia.py` ou pelo notebook da Born. Para outra foto, usar `--imagem CAMINHO --destino OUTRA_PASTA`, evitando substituir o experimento oficial.

```python
import numpy as np
dados = np.load("resultados/frequencia/entradas_segmentacao.npz")
original = dados["original_rgb"]
ruidosa = dados["ruidosa_rgb"]
filtrada = dados["filtrada_rgb"]
```

Todos os arrays têm formato (335,500,3), float64 em [0,1], na ordem RGB. A filtrada escolhida é Gaussiana com corte 0,25 ciclos/pixel. Ruído sigma=0,08 e seed=42. Não gerar novo ruído para comparar os métodos. Caso use cinza, aplicar a mesma conversão às três entradas.

- `parametros.json`: configuração, versões e métricas.
- `comparacao_filtros.csv`: os 22 experimentos.
- `entradas_segmentacao.npz`: arrays exatos para processamento.
- `original.png`, `ruidosa.png`, `filtrada.png`: visualização em 8 bits, sujeita a arredondamento; não são os arrays usados no PSNR.
- `comparacao_imagens.png`, `espectros_mascara.png`, `psnr_por_corte.png`, `recorte_contornos.png`: figuras do relatório e apresentação.

Watershed/SLIC e a análise de regiões/contornos ainda devem ser implementados por Gustavo. PSNR melhor não garante segmentação melhor.
