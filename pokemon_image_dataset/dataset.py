from pathlib import Path
import shutil
import tempfile
from typing import Optional

from torchvision.datasets import ImageFolder

from pokemon_image_dataset.utils import (
    download,
    replace_children_with_grandchildren,
    verify_sha256_checksum,
)


LATEST_VERSION = 'v0.0.0_1'
NEXT_VERSION = 'next'
CHECKSUM_BY_VERSION = {
    'v0.0.0_1': '9e0cd8a43d42bdcfefff941507756e4e8dc4d3add6595cbed854f0d3aa892044',
}


class PokemonImageDataset(ImageFolder):

    MAIN_URL = (
        'https://github.com/jneuendorf/pokemon-image-dataset-files/'
        'archive/refs/heads/main.zip'
    )
    VERSION_URL = (
        'https://github.com/jneuendorf/pokemon-image-dataset-files/'
        'archive/refs/tags/{version}.zip'
    )

    def __init__(
            self,
            *args,
            root: str,
            download: bool = False,
            version: str = 'latest',
            **kwargs
    ):
        if version == 'latest':
            version = LATEST_VERSION
        assert version in CHECKSUM_BY_VERSION or version == NEXT_VERSION, (
            f'invalid version "{version}", must be 1 of {", ".join(CHECKSUM_BY_VERSION)}'
        )
        self.version = version

        if download:
            self.download(Path(root))

        super().__init__(*args, root=root, **kwargs)

    def download(self, root: Path) -> None:
        download_dest = Path(tempfile.gettempdir()) / self.download_filename
        if not download_dest.exists():
            download(self.url, dest=download_dest)
        else:
            print(f'Using cached file at {download_dest}.')

        # We don't want to update the checksum for each commit.
        if self.version == NEXT_VERSION:
            print('Skipping checksum verification for bleeding edge version.')
        else:
            try:
                verify_sha256_checksum(download_dest, self.checksum)
            except ValueError:
                download_dest.unlink()

        root_path = Path(root)
        if root_path.exists():
            shutil.rmtree(root_path)
            # root_path.mkdir(parents=True)

        shutil.unpack_archive(download_dest, extract_dir=root)
        replace_children_with_grandchildren(root)

    @property
    def download_filename(self) -> Path:
        return Path(f'pokemon-image-dataset-{self.version}.zip')

    @property
    def url(self) -> str:
        if self.version == NEXT_VERSION:
            return self.MAIN_URL
        else:
            return self.VERSION_URL.format(version=self.version)

    @property
    def checksum(self) -> Optional[str]:
        return (
            CHECKSUM_BY_VERSION[self.version]
            if self.version != NEXT_VERSION
            else None
        )
