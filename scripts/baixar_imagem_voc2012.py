"""Recupera a imagem escolhida do pacote oficial, sem baixar o dataset todo."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json


def main():
    root = Path(__file__).resolve().parents[1]
    metadata = json.loads((root / 'data/metadados/2009_003974.json').read_text(encoding='utf-8'))
    target = root / metadata['arquivo']
    expected = metadata['sha256']
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'O arquivo existente difere do original: {target}. Preserve-o e confira antes de baixar novamente.')
        print(f'Imagem original já disponível: {target}')
        return
    start = metadata['archive_offset']
    end = start + metadata['archive_size'] - 1
    request = Request(metadata['source_archive'], headers={'Range': f'bytes={start}-{end}'})
    with urlopen(request, timeout=30) as response:
        if response.status != 206:
            raise RuntimeError('O servidor não aceitou a leitura parcial. Baixe o pacote oficial e extraia o membro indicado nos metadados.')
        expected_range = f"bytes {start}-{end}/"
        if not response.headers.get('Content-Range', '').startswith(expected_range):
            raise RuntimeError('O servidor retornou um trecho diferente do solicitado.')
        raw = response.read(metadata['archive_size'] + 1)
    if len(raw) != metadata['archive_size'] or hashlib.sha256(raw).hexdigest() != expected:
        raise RuntimeError('Tamanho ou SHA-256 divergente. Nenhum arquivo foi salvo.')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    print(f'Imagem original salva e SHA-256 conferido: {target}')


if __name__ == '__main__':
    main()
