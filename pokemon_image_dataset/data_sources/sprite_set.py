from dataclasses import dataclass, field
from pathlib import Path
import shutil
from typing import Dict, Optional

from pokemon_image_dataset.utils import SPRITE_SET_FORM_DELIMITER, get_image_frames
from .archive import RemoteArchiveDataSource


@dataclass
class SpriteSetConfig:
    glob: str
    """Glob pattern for relevant image files."""
    extra: Dict[str, str] = field(default_factory=dict)
    dest: Optional[str] = None
    """Rename sprite set folder."""
    post_process: Optional[str] = None

    def get_dest(self, default: str = None) -> str:
        return self.dest if self.dest is not None else default


class SpriteSetDataSource(RemoteArchiveDataSource):
    sprite_sets: Dict[str, SpriteSetConfig] = {}
    """Keys are folders in the (unpacked) data source."""

    def run(self, force=False):
        super().run(force)
        self.animations2frames()

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
        for src, conf in self.sprite_sets.items():
            yield from self.get_dest(conf, Path(src).name).iterdir()

    def animations2frames(self):
        for src, conf in self.sprite_sets.items():
            if conf.post_process is not None:
                method = getattr(self, conf.post_process)
                method(src, conf)

    def split_gif_frames(self, src: str, conf: SpriteSetConfig, ignore_single_color=True):
        for gif in self.get_dest(conf, Path(src).name).iterdir():
            for i, frame in enumerate(get_image_frames(gif)):
                if ignore_single_color and frame.colors == 1:
                    print(f'excluding single color frame {i} from {gif}')
                    continue

                frame.save(filename=(
                    gif
                    .with_stem(f'{gif.stem}{SPRITE_SET_FORM_DELIMITER}{i}')
                    .with_suffix('.png')
                ))
            gif.unlink()
