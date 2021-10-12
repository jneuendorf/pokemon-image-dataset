import hashlib
import os
from pathlib import Path
import shutil
from typing import Sequence

import requests


NAME_DELIMITER = '-'


def name(*parts: str) -> str:
    return NAME_DELIMITER.join(parts)


def dename(name: str) -> Sequence[str]:
    return name.split(NAME_DELIMITER)


def verify_sha256_checksum(path: Path, expected: str) -> str:
    chunk_size = 1024 * 64
    hash_sha256 = hashlib.sha256()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            hash_sha256.update(chunk)

    checksum = hash_sha256.hexdigest()
    if checksum != expected:
        raise ValueError(
            f'invalid checksum for {path}. expected {expected} but got {checksum}'
        )
    return checksum


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
    for grandchild in parent.glob('*/*'):
        shutil.move(str(grandchild), str(parent))
    for child_dir in child_dirs:
        shutil.rmtree(child_dir)


def with_stem(path: Path, stem) -> Path:
    """Polyfill function
    https://github.com/python/cpython/blob/56c1f6d7edad454f382d3ecb8cdcff24ac898a50/Lib/pathlib.py#L764-L766
    """
    return path.with_name(stem + path.suffix)


def readlink(path: Path) -> Path:
    """Polyfill function"""
    # return Path(os.readlink(str(path.resolve())))
    return Path(os.readlink(path))
