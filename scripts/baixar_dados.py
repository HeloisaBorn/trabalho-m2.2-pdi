"""Obtém as três imagens do trabalho e verifica a integridade dos arquivos."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
from baixar_imagem_voc2012 import main as baixar_carro

FONTES = {
    'gap-region-filling.tif': '12d56d590b2d0c9c50c275c0b35f9059d6846a4124d5ff4f57f02366bc8b4659',
    '002f20ad-2ace-499c-9335-c9080bc3e6b5.png': '3923b7c4434c90db0576b03c794e1afa1dda777c5db4c0d9d075b5f7bd291f3e',
}


def main():
    baixar_carro()
    pasta = Path(__file__).resolve().parents[1]/'data/originais'
    for nome, esperado in FONTES.items():
        destino = pasta/nome
        if destino.exists():
            raw = destino.read_bytes()
        else:
            url = 'https://raw.githubusercontent.com/VielF/ColabProjects/main/dataset/OperacaoMorfologia/' + nome
            with urlopen(url, timeout=45) as response:
                raw = response.read()
        if hashlib.sha256(raw).hexdigest() != esperado:
            raise RuntimeError(f'Checksum divergente em {nome}; nenhum arquivo foi sobrescrito.')
        if not destino.exists(): destino.write_bytes(raw)
        print('Imagem verificada:', nome)


if __name__ == '__main__': main()
