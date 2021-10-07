import hashlib
from pathlib import Path
import shutil

import requests


def verify_sha256_checksum(path: Path, expected: str) -> None:
    CHUNK_SIZE = 1024 * 64
    hash_sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            hash_sha256.update(chunk)

    checksum = hash_sha256.hexdigest()
    if checksum != expected:
        raise ValueError(
            f'invalid checksum for {path}. expected {expected} but got {checksum}'
        )


def download(url: str, dest: Path) -> None:
    """https://stackoverflow.com/a/16696317/6928824"""
    print(f'downloading {url} to {dest}')
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(dest, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 16):
                file.write(chunk)


def replace_children_with_grandchildren(parent: Path) -> None:
    """Moves all grandchildren up one level and
    removes the then empty child directories.
    """
    child_dirs = [child for child in parent.iterdir() if child.is_dir()]
    for grandchild in parent.glob(f'*/*'):
        shutil.move(str(grandchild), str(parent))
    for child_dir in child_dirs:
        shutil.rmtree(child_dir)
