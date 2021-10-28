from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from pokemon_image_dataset.form import POKEMON_FORMS, DISMISS_FORM, PokemonForm
from pokemon_image_dataset.utils import (
    parse_ndex,
    verify_sha256_checksum,
)
from .path_dict import PathDict


class DataSource(ABC):
    checksum: str = None
    extra_ops = ()
    tmp_dir: Path = None

    def __init__(self, *, tmp_dir: Path):
        self.tmp_dir = tmp_dir

    def run(self, force=False):
        self.root.mkdir(parents=True, exist_ok=True)
        data_path = self.get(force)
        self.verify_checksum(data_path)
        self.process(data_path)
        self.arrange()
        self.rename_forms()

    @abstractmethod
    def get(self, force: bool):
        ...

    def verify_checksum(self, data_path: Path) -> None:
        verify_sha256_checksum(data_path, self.checksum)

    def process(self, archive):
        ...

    @property
    def root(self) -> Path:
        return self.tmp_dir / f'__{self.__class__.__name__}'

    def arrange(self):
        ...

    def rename_forms(self) -> None:
        assigned_forms = self.assign_forms()
        # NOTE: Sorting enhances value of printed operations
        #  but is essential for having a deterministic order so that
        #  the developer can solve issues with chained renames
        for filename in sorted(self.get_files()):
            if filename.is_symlink():
                print('dismissing detected symlink', filename, '=>', filename.readlink())
                filename.unlink()
            else:
                stem = filename.stem
                form = assigned_forms[filename]
                found_form: PokemonForm
                if form is None:
                    ndex = self.parse_ndex(stem)
                    forms = [f for f in POKEMON_FORMS[ndex] if f.name == stem]
                    assert len(forms) == 1, (
                        f'got {len(forms)} matching forms instead 1 for {filename}'
                    )
                    found_form = forms[0]
                else:
                    found_form = form

                if found_form is DISMISS_FORM:
                    print('dismissing', filename)
                    filename.unlink()
                else:
                    # Avoid unnecessary renames
                    if found_form.name != stem:
                        rename_to = filename.with_stem(found_form.name)
                        print('rename:', filename, rename_to)
                        filename.rename(rename_to)

    def assign_forms(self) -> PathDict[PokemonForm]:
        return PathDict()

    @abstractmethod
    def get_files(self) -> Iterable[Path]:
        ...

    def parse_ndex(self, filename: str) -> int:
        return parse_ndex(filename)
