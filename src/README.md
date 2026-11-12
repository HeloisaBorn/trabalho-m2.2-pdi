# Acordos técnicos

- Imagens RGB/cinza: arrays NumPy float em [0, 1]. RGB na entrada, sem confundir com BGR.
- Máscaras: arrays booleanos. Rótulos: inteiros, documentando fundo e bordas.
- Born: `frequencia.py` e `metricas.py`; Gustavo: `segmentacao.py`; João Paulo: `morfologia.py` e `contagem.py`.
- Funções recebem imagens e parâmetros; não carregam caminhos fixos nem abrem janelas por conta própria.
- Born fornece original, ruidosa e filtrada com mesmas dimensões, seed e parâmetros registrados.
- PSNR usa a imagem limpa como referência e intervalo consistente. Não é métrica de qualidade da segmentação.
- Na Parte 2, registrar contagens por etapa, conectividade e elemento estruturante. Preencher buracos pode manter a contagem; fechamento pode fundir células.
- Não usar filtros/operações pontuais prontos nem contadores prontos. Justificar e citar adaptações dos exemplos didáticos.
- Verificar algoritmos com pequenas entradas de resultado conhecido antes de usar imagens reais.
