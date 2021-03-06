import filecmp
import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from pprint import pprint
from typing import List

from skimage.color import gray2rgb, rgba2rgb
from skimage.io import imread
from skimage.transform import rescale
from tqdm import tqdm
from wand.image import Image

from pokemon_image_dataset.form import PokemonImage
from pokemon_image_dataset.data_sources import (BattlersDataSource, DataSource, SpriteSetDataSource,
                                                veekun)
from pokemon_image_dataset.utils import (FORM_NAME_DELIMITER,
                                         NAME_DELIMITER, dename, extent_gravity_center,
                                         get_bbox, get_scaling_factor, name)

BASE_DIR = Path(__file__).parent
TMP_DIR = BASE_DIR / 'tmp'
DATA_REPO_DIR = BASE_DIR / 'pokemon-image-dataset-files'
STATS_FILE = BASE_DIR / 'stats.json'

PADDING = 1
# This values are arbitrary such that 48x48 can be upscaled well and only 128x128 needs to be downscaled.
# This way, we don't loose to much information while also avoiding unnecessarily large images.
FINAL_SIZE = (96, 96)


def run_data_sources(data_sources: List[DataSource]) -> None:
    for data_source in data_sources:
        print(f'processing data source {data_source.__class__.__name__}')
        data_source.run(force=False)


# def remove_adjacent_duplicates(data_sources: List[SpriteSetDataSource]) -> None:
#     """Finds and removes duplicates within each data source, not across data sources."""
#
#     def filename_key(filename: Path) -> tuple[int, str, int]:
#         ndex: str
#         form: str
#         frame: int
#
#         ndex, *rest = re.split(
#             f'{FORM_NAME_DELIMITER}|{NAME_DELIMITER}',
#             filename.stem,
#         )
#         if rest:
#             try:
#                 frame = int(rest[-1])
#                 form = name(*rest[:-1])
#             except ValueError:
#                 frame = -1
#                 form = name(*rest)
#         else:
#             frame = -1
#             form = ''
#         return int(ndex), form, frame
#
#     for data_source in data_sources:
#         print(f'removing duplicates for {data_source.__class__.__name__}')
#         for src in data_source.sprite_sets:
#             duplicates = set()
#             dest = data_source.get_dest(src)
#             print('searching for duplicates in', dest)
#             # TODO: use data_source.images so only relevant images are regarded!
#             files = list(sorted(
#                 dest.iterdir(),
#                 key=filename_key,
#             ))
#             for a, b in tqdm(zip(files[:-1], files[1:]), total=len(files) - 1):
#                 if filecmp.cmp(a, b, shallow=False):
#                     duplicates.add(b)
#             for file in sorted(duplicates):
#                 file.unlink()
#                 print('removed duplicate', file)


def normalize_image_sizes(data_sources: List[DataSource]) -> None:
    for data_source in data_sources:
        print(f'normalizing image sizes for {data_source.__class__.__name__}')
        # for filename in tqdm(sorted(data_source.get_files())):
        for poke_image in sorted(data_source.images):
            filename = poke_image.source_file
            bbox = poke_image.bbox

            img = imread(str(filename))
            if img.shape[-1] == 4:
                img = rgba2rgb(img)
            elif len(img.shape) == 2 or img.shape[-1] == 1:
                img = gray2rgb(img)

            assert img.shape[-1] == 3, f'image must have 3 channels but got shape {img.shape}'

            min_row, min_col, max_row, max_col = bbox
            cropped = img[min_row:max_row, min_col:max_col]
            scaled = rescale(
                cropped,
                get_scaling_factor(bbox, final_size=FINAL_SIZE, padding=PADDING),
                multichannel=True,
                anti_aliasing=True,
                # channel_axis=-1,  # 0.19+
            )
            res_img = extent_gravity_center(
                scaled,
                width=FINAL_SIZE[0],
                height=FINAL_SIZE[1],
            )
            res_img.save(filename=filename)


def copy_images_to_data_repo(data_sources: List[DataSource]) -> None:
    for data_source in data_sources:
        print(f'copying images of {data_source.__class__.__name__}')
        # for filename in tqdm(sorted(data_source.get_files())):
        for poke_image in sorted(data_source.images):
            dest_dir = DATA_REPO_DIR / str(poke_image.form.ndex)
            dest_dir.mkdir(parents=True, exist_ok=True)
            # TODO: CHECK: fix dashes, i.e. 1/emerald-animated---28.png
            shutil.copyfile(poke_image.source_file, dest_dir / poke_image.filename)


def generate_stats(data_sources: List[SpriteSetDataSource]) -> None:
    """Gets some statistic data from the `DATA_REPO_DIR`.
    Only the structure of this directory is used, not the data sources data or meta data.
    This way, errors/inconsistencies should become obvious more easily.
    """

    stats = {
        'images': sum(1 for _ in DATA_REPO_DIR.glob('*/*.png')),
        # TODO: seems to be wrong for battlers
        'images_per_sprite_set': {
            data_source.get_dest(src).name: (
                sum(1 for _ in DATA_REPO_DIR.glob(
                    f'*/{data_source.get_dest(src).name}{NAME_DELIMITER}*.png'
                ))
                + sum(1 for _ in DATA_REPO_DIR.glob(
                    f'*/{data_source.get_dest(src).name}.png'
                ))
            )
            for data_source in data_sources
            for src in data_source.sprite_sets
        },
        'pokemon_per_sprite_set': {
            data_source.get_dest(src).name: (
                sum(1 for _ in {
                    filename.parent.name
                    for filename in DATA_REPO_DIR.glob(
                        f'*/{data_source.get_dest(src).name}{NAME_DELIMITER}*.png'
                    )
                })
                + sum(1 for _ in {
                    filename.parent.name
                    for filename in DATA_REPO_DIR.glob(
                        f'*/{data_source.get_dest(src).name}.png'
                    )
                })
            )
            for data_source in data_sources
            for src in data_source.sprite_sets
        },
        'images_per_pokemon': {
            int(ndex.name): sum(1 for _ in ndex.glob('*.png'))
            for ndex in DATA_REPO_DIR.glob('*')
            if ndex.is_dir()  # ignore e.g. .DS_Store
        },
    }
    with open(STATS_FILE, 'w') as fp:
        json.dump(stats, fp)
    pprint(stats)


###############################################################################
if __name__ == '__main__':
    data_sources: List[SpriteSetDataSource] = [
        DataSource(tmp_dir=TMP_DIR)
        for DataSource in (
            veekun.Gen1,
            veekun.Gen2,
            veekun.Gen3,
            veekun.Gen4,
            veekun.Gen5,
            veekun.Icons,
            veekun.Sugimori,
            veekun.DreamWorld,
            BattlersDataSource,
        )
    ]
    print('\nRUNNING DATA SOURCES')
    run_data_sources(data_sources)

    print('\nREMOVING DUPLICATES')
    remove_adjacent_duplicates(data_sources)

    print('\nNORMALIZING IMAGES')
    normalize_image_sizes(data_sources)

    print('\nMOVING IMAGES TO DATA REPO')
    copy_images_to_data_repo(data_sources)

    print('\nGENERATING STATS')
    generate_stats(data_sources)
