"""Executa as frentes Born/Gustavo e o notebook integrado com o Python deste ambiente."""
from pathlib import Path
import os
import sys
import json
import nbformat
from nbclient import NotebookClient
from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager

root=Path(__file__).resolve().parents[1]
# Kernel local: não registra nem altera kernels do usuário/sistema.
config=root/'.venv/jupyter-local'
kernel=config/'kernels/python3';kernel.mkdir(parents=True,exist_ok=True)
(kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Python 3 (projeto)','language':'python'}),encoding='utf-8')
os.environ['JUPYTER_PATH']=str(config)
os.environ['JUPYTER_RUNTIME_DIR']=str(config/'runtime')
os.environ['IPYTHONDIR']=str(config/'ipython')
os.environ['MPLCONFIGDIR']=str(config/'matplotlib')
for folder in ['runtime','ipython','matplotlib']:
    (config/folder).mkdir(exist_ok=True)
ksm=KernelSpecManager(kernel_dirs=[str(config/'kernels')],ensure_native_kernel=False)
paths = sys.argv[1:] or ['notebooks/rascunhos/01_frequencia.ipynb','notebooks/rascunhos/02_segmentacao.ipynb','notebooks/trabalho_m2_2.ipynb']
for path in paths:
    target=root/path
    nb=nbformat.read(target,as_version=4)
    print('Iniciando:',path,flush=True)
    km=AsyncKernelManager(kernel_name='python3',kernel_spec_manager=ksm)
    NotebookClient(nb,km=km,timeout=240,startup_timeout=40,kernel_name='python3',resources={'metadata':{'path':str(target.parent)}}).execute()
    nbformat.validate(nb)
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
    nbformat.write(nb,target)
    print('Executado:',path,flush=True)
