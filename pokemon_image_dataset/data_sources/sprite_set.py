import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Collection, Optional, Union

from pokemon_image_dataset.form import PokemonForm, PokemonImage
from pokemon_image_dataset.utils import NAME_DELIMITER, get_image_frames, whiten_areas
from .archive import RemoteArchiveDataSource

PostProcessorSpec = Union[str, tuple[str, dict]]


@dataclass
class SpriteSetConfig:
    glob: str
    """Glob pattern for relevant image files."""
    extra: dict[str, str] = field(default_factory=dict)
    dest: Optional[str] = None
    """Rename sprite set folder."""
    post_process: list[PostProcessorSpec] = field(default_factory=list)
    """Method name or tuples of name and kwargs.
    Method that get called for a sprite set with
        (src: str, conf: SpriteSetConfig, **kwargs)
    in the specified order.
    """


class SpriteSetDataSource(RemoteArchiveDataSource[PokemonImage]):
    sprite_sets: dict[str, SpriteSetConfig] = {}
    """Keys are folders in the (unpacked) data source."""

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

    def get_images(self, associated_forms: list[tuple[PokemonForm, Path]]) -> list[PokemonImage]:
        return [
            PokemonImage(
                data_source=self,
                form=form,
                source_file=filename,
                sprite_set=filename.parent.name,
                format=filename.suffix,
            )
            for form, filename in associated_forms
        ]

    def get_dest(self, sprite_set: str, root: Path = None) -> Path:
        if root is None:
            root = self.tmp_dir

        conf = self.sprite_sets[sprite_set]
        return root / (conf.dest or Path(sprite_set).name)

    def get_files(self):
        for src in self.sprite_sets:
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
        def split_image(image: PokemonImage) -> list[PokemonImage]:
            gif = image.source_file
            assert gif.suffix == '.gif', f'expected gif image but got {image.source_file}'
            images = []
            for i, frame in enumerate(get_image_frames(gif)):
                # Ignore single color frames
                if frame.colors == 1:
                    print(f'excluding single color frame {i} from {gif}')
                    continue

                frame_png = gif.with_stem(f'{gif.stem}{NAME_DELIMITER}{i}').with_suffix('.png')
                frame.save(filename=frame_png)
                images.append(PokemonImage(
                    data_source=image.data_source,
                    form=image.form,
                    source_file=frame_png,
                    sprite_set=image.sprite_set,
                    frame=i,
                    format='.png',
                ))
            return images

        # TODO: async
        images_to_replace = {image for image in self.images if image.sprite_set == src}
        replacements = {
            replacement
            for image in images_to_replace
            for replacement in split_image(image)
        }
        assert all(img.source_file.exists() for img in replacements), "some of the split images' files do not exist"
        self.images = (self.images - images_to_replace) | replacements

    def whiten_areas(
        self,
        src: str,
        conf: SpriteSetConfig,
        forms: Collection[Union[PokemonForm, tuple[PokemonForm, list[tuple[int, int]]]]] = (),
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
