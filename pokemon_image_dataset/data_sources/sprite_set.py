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

    def get_dest(self, default: str = None) -> str:
        return self.dest if self.dest is not None else default


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
            src = self.root / src
            pattern = conf.glob
            extra = conf.extra
            dest = self.get_dest(conf, src.name)
            if dest.exists():
                print('deleting existing', dest)
                shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)
            for file in src.glob(pattern):
                shutil.move(file, dest / file.name)
            for extra_src, extra_dest in extra.items():
                shutil.move(src / extra_src, dest / extra_dest)

        shutil.rmtree(self.root)

    def get_dest(self, conf: SpriteSetConfig, default: str) -> Path:
        return self.tmp_dir / (
            conf.dest
            if conf.dest
            else default
        )

    def get_files(self):
        for src in self.sprite_sets:
            yield from self.get_sprite_set_files(src)

    def get_sprite_set_files(self, src: str):
        yield from self.get_dest(self.sprite_sets[src], Path(src).name).iterdir()

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
        dest = self.get_dest(self.sprite_sets[src], Path(src).name)
        for form, coords in forms_an_coords:
            filename = dest / f'{form.complete_name}.png'
            print('whitening area of', filename, 'at', coords)
            whiten_areas(filename, coords)
