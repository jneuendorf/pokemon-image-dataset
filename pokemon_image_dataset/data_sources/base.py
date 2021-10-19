from abc import ABC, abstractmethod
from pathlib import Path
import shutil
from typing import Iterable

from pokemon_image_dataset.form import POKEMON_FORMS, DISMISS_FORM
from pokemon_image_dataset.utils import (
    parse_ndex,
    readlink,
    verify_sha256_checksum,
    with_stem,
)
from .path_dict import PathDict


class DataSource(ABC):
    checksum: str = None
    extra_ops = ()
    tmp_dir: Path = None

    _renamed_files = set()

    def __init__(self, *, tmp_dir: Path):
        self.tmp_dir = tmp_dir

    def run(self, force=False):
        self.root.mkdir(parents=True, exist_ok=True)
        data_path = self.get(force)
        self.verify_checksum(data_path)
        self.process(data_path)
        self.arrange()
        self.do_extra_ops()
        self._renamed_files = self.rename_forms()

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

    def do_extra_ops(self):
        for src, dst in self.extra_ops:
            print('extra_op', src, dst)
            if dst is None:
                try:
                    if (self.tmp_dir / src).is_dir():
                        shutil.rmtree(self.tmp_dir / src)
                    else:
                        (self.tmp_dir / src).unlink()
                except FileNotFoundError:
                    print('tried to delete', self.tmp_dir / src)
            else:
                shutil.move(str(self.tmp_dir / src), str(self.tmp_dir / dst))

    def rename_forms(self) -> None:
        files = set()

        assigned_forms = self.assign_forms()
        # NOTE: Sorting enhances value of printed operations
        #  but is essential for having a deterministic order so that
        #  the developer can solve issues with chained renames
        for filename in sorted(self.get_files()):
            if filename.is_symlink():
                print('dismissing detected symlink', filename, '=>', readlink(filename))
                filename.unlink()
            else:
                stem = filename.stem
                form = assigned_forms[filename]
                if form is None:
                    ndex = self.parse_ndex(stem)
                    forms = [
                        form
                        for form in POKEMON_FORMS[ndex]
                        if form.complete_name == stem
                    ]
                    assert len(forms) == 1, (
                        f'got {len(forms)} matching forms instead 1 for {filename}'
                    )
                    form = forms[0]

                if form is DISMISS_FORM:
                    print('dismissing', filename)
                    filename.unlink()
                else:

                    # Avoid unncessary renames
                    if form.complete_name != stem:
                        rename_to = with_stem(filename, form.complete_name)
                        print('rename:', filename, rename_to)
                        filename.rename(rename_to)
                        files.add(rename_to)
                    else:
                        files.add(filename)
        return files

    def assign_forms(self) -> PathDict:
        return PathDict()

    @abstractmethod
    def get_files(self) -> Iterable[Path]:
        ...

    def parse_ndex(self, filename: str) -> int:
        return parse_ndex(filename)

    @property
    def renamed_filenames(self):
        return self._renamed_files.copy()
