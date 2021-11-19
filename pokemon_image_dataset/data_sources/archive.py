import shutil
from abc import ABC
from pathlib import Path
from typing import Generic

from pokemon_image_dataset.utils import download
from .base import DataSource, T


class ArchiveDataSource(DataSource, ABC, Generic[T]):

    def process(self, archive):
        shutil.unpack_archive(filename=archive, extract_dir=self.root)


class RemoteArchiveDataSource(ArchiveDataSource, ABC, Generic[T]):
    url = None

    def get(self, force):
        download_dest = self.tmp_dir / Path(self.url).name
        if not download_dest.exists() or force:
            download(self.url, download_dest)
        return download_dest
