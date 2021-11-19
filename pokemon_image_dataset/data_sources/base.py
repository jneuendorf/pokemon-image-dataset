from abc import ABC, abstractmethod
from collections import Iterable, Collection, Callable
from pathlib import Path
from typing import TypeVar, Generic, Union

from pokemon_image_dataset.form import POKEMON_FORMS, DISMISS_FORM, PokemonForm, BasePokemonImage
from pokemon_image_dataset.utils import (
    parse_ndex,
    verify_sha256_checksum,
)
from .path_dict import PathDict


T = TypeVar('T', bound=BasePokemonImage)


# class DataSourceMeta(type(ABC), type(Generic[T])):
#     pass


class DataSource(ABC, Generic[T]):
    checksum: str = None
    extra_ops = ()
    tmp_dir: Path = None
    images: set[T] = []

    def __init__(self, *, tmp_dir: Path):
        self.tmp_dir = tmp_dir

    def run(self, force=False) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        data_path = self.get(force)
        self.verify_checksum(data_path)
        self.process(data_path)
        self.arrange()
        self.images = set(self.get_images(self.associate_forms()))
        self.post_process()

    @property
    def root(self) -> Path:
        return self.tmp_dir / f'__{self.__class__.__name__}'

    @abstractmethod
    def get(self, force: bool):
        ...

    def verify_checksum(self, data_path: Path) -> None:
        verify_sha256_checksum(data_path, self.checksum)

    def process(self, archive) -> None:
        ...

    def arrange(self) -> None:
        ...

    def associate_forms(self) -> list[tuple[PokemonForm, Path]]:
        form_path_tuples = []
        assigned_forms = self.assign_forms()
        # NOTE: Sorting enhances value of printed operations
        #  but is essential for having a deterministic order so that
        #  the developer can solve issues with chained renames
        for filename in sorted(self.get_files()):
            if filename.is_symlink():
                print('dismissing detected symlink', filename, '=>', filename.readlink())
                # filename.unlink()
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
                    # filename.unlink()
                else:
                    form_path_tuples.append((
                        found_form,
                        filename,
                    ))
                    # # Avoid unnecessary renames
                    # if found_form.name != stem:
                    #     rename_to = filename.with_stem(found_form.name)
                    #     print('rename:', filename, rename_to)
                    #     filename.rename(rename_to)
        print('form_path_tups', form_path_tuples)
        return form_path_tuples

    def assign_forms(self) -> PathDict[PokemonForm]:
        return PathDict()

    @abstractmethod
    def get_images(self, associated_forms: list[tuple[PokemonForm, Path]]) -> Collection[T]:
        """Allows subclasses to use their own according BasePokemonImage subclass."""
        ...

    # def replace_image(self, image: T, replacements: Collection[BasePokemonImage]):
    #     assert all(img.source_file.exists() for img in replacements), "some of the split images' files do not exist"
    #     # We want the KeyError in case the image is not in the set.
    #     self.images.remove(image)
    #     self.images |= set(replacements)

    def post_process(self):
        ...

    @abstractmethod
    def get_files(self) -> Iterable[Path]:
        ...

    def parse_ndex(self, filename: str) -> int:
        return parse_ndex(filename)
