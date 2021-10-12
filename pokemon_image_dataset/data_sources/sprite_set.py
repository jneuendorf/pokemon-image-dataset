# from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Dict, Optional, TypedDict

from .archive import RemoteArchiveDataSource


class SpriteSetConfig(TypedDict):
    glob: str
    extra: Optional[Dict[str, str]]
    dest: Optional[str]


class SpriteSetDataSource(RemoteArchiveDataSource):
    sprite_sets: Dict[str, SpriteSetConfig] = {
        # 'pokemon/main-sprites/red-blue': {
        #     'dest': None,  # rename
        #     'glob': '*.png',
        # },
    }

    def arrange(self):
        """Moves sprite set folders into `self.tmp_dir` and
        saves the destinations for `self.get_files`.
        """

        for src, conf in self.sprite_sets.items():
            src = self.root / src
            pattern = conf['glob']
            extra = conf.get('extra', {})
            dest = self.tmp_dir / conf.get('dest', src.name)
            if dest.exists():
                print('deleting existing', dest)
                shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)
            # shutil.copytree(src, dest)
            for file in src.glob(pattern):
                shutil.move(file, dest / file.name)
            for extra_src, extra_dest in extra.items():
                shutil.move(src / extra_src, dest / extra_dest)

        shutil.rmtree(self.root)

    def get_dest(self, src: str, conf: SpriteSetConfig) -> Path:
        return self.tmp_dir / conf.get('dest', Path(src).name)

    def get_files(self):
        for src, conf in self.sprite_sets.items():
            yield from self.get_dest(src, conf).iterdir()
