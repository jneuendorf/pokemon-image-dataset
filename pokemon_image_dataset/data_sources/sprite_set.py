import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Collection, Dict, List, Optional, Tuple, Union

from pokemon_image_dataset.form import PokemonForm
from pokemon_image_dataset.utils import NAME_DELIMITER, get_image_frames, whiten_areas
from .archive import RemoteArchiveDataSource

PostProcessorSpec = Union[str, Tuple[str, dict]]


@dataclass
class SpriteSetConfig:
    glob: str
    """Glob pattern for relevant image files."""
    extra: Dict[str, str] = field(default_factory=dict)
    dest: Optional[str] = None
    """Rename sprite set folder."""
    post_process: List[PostProcessorSpec] = field(default_factory=list)
    """Method name or tuples of name and kwargs.
    Method that get called for a sprite set with
        (src: str, conf: SpriteSetConfig, **kwargs)
    in the specified order.
    """


class SpriteSetDataSource(RemoteArchiveDataSource):
    sprite_sets: Dict[str, SpriteSetConfig] = {}
    """Keys are folders in the (unpacked) data source."""

    def run(self, force=False):
        super().run(force)
        self.post_process()

    def arrange(self):
        """Moves sprite set folders into `self.tmp_dir` and
        saves the destinations for `self.get_files`.
        """

        for src, conf in self.sprite_sets.items():
            root = self.root / src
            pattern = conf.glob
            extra = conf.extra
            dest = self.get_dest(src)
            if dest.exists():
                print('deleting existing', dest)
                shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)
            for file in root.glob(pattern):
                shutil.move(file, dest / file.name)
            for extra_src, extra_dest in extra.items():
                shutil.move(root / extra_src, dest / extra_dest)

        shutil.rmtree(self.root)

    def get_dest(self, sprite_set: str, root: Path = None) -> Path:
        if root is None:
            root = self.tmp_dir

        conf = self.sprite_sets[sprite_set]
        return root / (conf.dest or Path(sprite_set).name)

    def get_files(self):
        for src in self.sprite_sets:
            yield from self.get_sprite_set_files(src)

    def get_sprite_set_files(self, src: str):
        yield from self.get_dest(src).iterdir()

    def post_process(self):
        for src, conf in self.sprite_sets.items():
            for method_spec in conf.post_process:
                method_name: str
                kwargs = {}
                if isinstance(method_spec, tuple):
                    method_name, kwargs = method_spec
                else:
                    method_name = method_spec
                method = getattr(self, method_name)
                method(src, conf, **kwargs)

    # POST PROCESSORS
    def split_gif_frames(self, src: str, conf: SpriteSetConfig):
        for gif in self.get_sprite_set_files(src):
            for i, frame in enumerate(get_image_frames(gif)):
                # Ignore single color frames
                if frame.colors == 1:
                    print(f'excluding single color frame {i} from {gif}')
                    continue

                frame.save(filename=(
                    gif
                    .with_stem(f'{gif.stem}{NAME_DELIMITER}{i}')
                    .with_suffix('.png')
                ))
            gif.unlink()

    def whiten_areas(
        self,
        src: str,
        conf: SpriteSetConfig,
        forms: Collection[Union[PokemonForm, Tuple[PokemonForm, List[Tuple[int, int]]]]] = (),
    ) -> None:
        forms_an_coords = [
            (form, [(0, 0)]) if isinstance(form, PokemonForm) else form
            for form in forms
        ]
        dest = self.get_dest(src)
        for form, coords in forms_an_coords:
            filename = dest / f'{form.name}.png'
            print('whitening area of', filename, 'at', coords)
            whiten_areas(filename, coords)
