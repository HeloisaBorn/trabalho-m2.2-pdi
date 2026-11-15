"""Executa a frente da Born e exporta entradas sem perda para Gustavo."""
from pathlib import Path
import sys
import argparse
import csv
import json
import hashlib
import platform
import importlib.metadata
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.frequencia import ruido_gaussiano, filtrar_frequencia
from src.metricas import mse, psnr


def executar(imagem=None, destino=None, sigma=0.08, seed=42):
    entrada = Path(imagem) if imagem else ROOT/'data/originais/2009_003974.jpg'
    out = Path(destino) if destino else ROOT/'resultados/frequencia'
    out.mkdir(parents=True, exist_ok=True)
    with Image.open(entrada) as im:
        original = np.asarray(im.convert('RGB'), dtype=np.float64)/255
    ruidosa = ruido_gaussiano(original, sigma=sigma, seed=seed)
    cortes = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.16, 0.20, 0.25, 0.35, 0.50]
    baseline = psnr(original, ruidosa)
    tabela = []
    melhor = None
    for tipo in ['gaussiano', 'butterworth']:
        for corte in cortes:
            filtrada, info = filtrar_frequencia(ruidosa, corte, tipo, ordem=2, padding=32)
            score = psnr(original, filtrada)
            row = dict(filtro=tipo, corte=corte, ordem=2 if tipo=='butterworth' else '',
                       mse=mse(original, filtrada), psnr_db=score, ganho_db=score-baseline)
            tabela.append(row)
            if melhor is None or score > melhor['psnr_db']:
                melhor = dict(row); escolhida = filtrada; detalhes = info
    with (out/'comparacao_filtros.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=tabela[0].keys());w.writeheader();w.writerows(tabela)
    # Arrays float64 são a entrada oficial para a segmentação. PNGs são só visualização.
    np.savez_compressed(out/'entradas_segmentacao.npz', original_rgb=original,
                        ruidosa_rgb=ruidosa, filtrada_rgb=escolhida)
    for nome, x in [('original',original),('ruidosa',ruidosa),('filtrada',escolhida)]:
        Image.fromarray(np.rint(x*255).astype(np.uint8)).save(out/(nome+'.png'))

    fig, axes=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
    for ax,x,title in zip(axes,[original,ruidosa,escolhida],['Original limpa',f'Ruído: PSNR {baseline:.2f} dB',f"{melhor['filtro']}: PSNR {melhor['psnr_db']:.2f} dB"]):
        ax.imshow(x);ax.set_title(title);ax.axis('off')
    fig.savefig(out/'comparacao_imagens.png',dpi=150);plt.close(fig)

    # Mesmo intervalo da escala logarítmica nos espectros antes/depois.
    antes=np.log1p(np.abs(detalhes['espectro_antes']).mean(axis=2))
    depois=np.log1p(np.abs(detalhes['espectro_depois']).mean(axis=2))
    fig,axes=plt.subplots(1,3,figsize=(14,4.5),layout='constrained')
    extent=[-0.5,0.5,-0.5,0.5]
    for ax,z,title in zip(axes[:2],[antes,depois],['Espectro antes','Espectro depois']):
        shown=ax.imshow(z,cmap='magma',vmin=0,vmax=antes.max(),extent=extent,origin='lower')
        ax.set_title(title);ax.set_xlabel('Frequência x (ciclos/pixel)');ax.set_ylabel('Frequência y')
    fig.colorbar(shown,ax=list(axes[:2]),label='log(1 + amplitude média RGB)',shrink=0.8)
    h=axes[2].imshow(detalhes['mascara'],vmin=0,vmax=1,cmap='gray',extent=extent,origin='lower')
    axes[2].set_title('Máscara passa-baixa');axes[2].set_xlabel('Frequência x (ciclos/pixel)')
    fig.colorbar(h,ax=axes[2],shrink=0.8)
    fig.savefig(out/'espectros_mascara.png',dpi=150);plt.close(fig)

    fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    for tipo in ['gaussiano','butterworth']:
        rows=[r for r in tabela if r['filtro']==tipo]
        ax.plot([r['corte'] for r in rows],[r['psnr_db'] for r in rows],marker='o',label=tipo)
    ax.axhline(baseline,color='gray',linestyle='--',label='Ruidosa, sem filtragem')
    ax.set(xlabel='Parâmetro de corte (ciclos/pixel)',ylabel='PSNR contra a original (dB)',title='Mesma imagem, mesmo ruído, mesmo padding')
    ax.legend();ax.grid(alpha=0.2);fig.savefig(out/'psnr_por_corte.png',dpi=150);plt.close(fig)

    # Recorte idêntico próximo às rodas/carroceria, apenas para análise visual.
    height,width=original.shape[:2]
    y0,y1=int(height*0.48),int(height*0.87);x0,x1=int(width*0.60),int(width*0.94)
    fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout='constrained')
    for ax,x,title in zip(axes,[original,ruidosa,escolhida],['Original','Ruidosa','Filtrada']):
        ax.imshow(x[y0:y1,x0:x1]);ax.set_title(title);ax.axis('off')
    fig.savefig(out/'recorte_contornos.png',dpi=150);plt.close(fig)

    manifesto=dict(imagem=str(entrada.name),sha256_entrada=hashlib.sha256(entrada.read_bytes()).hexdigest(),
        shape=list(original.shape),intervalo=[0,1],dtype='float64',sigma=sigma,seed=seed,padding_reflect=32,
        ruido='N(0,sigma²), independente por canal, seguido de clipping em [0,1]',
        psnr_ruidosa_db=baseline,mse_ruidosa=mse(original,ruidosa),escolha=melhor,
        criterio='Maior PSNR na grade, com referência limpa conhecida. Ajuste demonstrativo nesta imagem/seed, sem validação independente.',
        comparabilidade='Mesmo D0 não implica mesma resposta: Gaussiano H(D0)=exp(-1/2); Butterworth H(D0)=1/2.',
        residuo_imaginario_max=detalhes['residuo_imaginario_max'],
        ambiente=dict(python=platform.python_version(),**{p:importlib.metadata.version(p) for p in ['numpy','matplotlib','Pillow']}))
    (out/'parametros.json').write_text(json.dumps(manifesto,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifesto,tabela


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--imagem',type=Path)
    parser.add_argument('--destino',type=Path)
    args=parser.parse_args()
    manifest,_=executar(args.imagem,args.destino)
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
