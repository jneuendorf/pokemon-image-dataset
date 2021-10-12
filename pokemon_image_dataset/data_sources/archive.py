from pathlib import Path
import shutil

from pokemon_image_dataset.utils import download
from .base import DataSource


class ArchiveDataSource(DataSource):

    def process(self, archive):
        shutil.unpack_archive(filename=archive, extract_dir=self.root)


class RemoteArchiveDataSource(ArchiveDataSource):
    url = None

    def get(self, force):
        download_dest = self.tmp_dir / Path(self.url).name
        if not download_dest.exists() or force:
            download(self.url, download_dest)
        return download_dest
