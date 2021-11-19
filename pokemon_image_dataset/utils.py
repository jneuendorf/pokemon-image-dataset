import hashlib
import shutil
from pathlib import Path
from typing import Union, Sequence, Tuple, List

import numpy as np
import requests
from skimage.color import rgb2gray
from skimage.measure import label, regionprops
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

PathLike = Union[str, Path]


NAME_DELIMITER = '--'
FORM_NAME_DELIMITER = '-'


###############################################################################
# FILENAMES
def name(*parts: str) -> str:
    return FORM_NAME_DELIMITER.join(parts)


def dename(name: PathLike) -> Sequence[str]:
    if isinstance(name, Path):
        name = name.stem
    return name.split(FORM_NAME_DELIMITER)


def parse_ndex(filename: str) -> int:
    ndex_str = dename(filename)[0]
    return int(ndex_str)


###############################################################################
# DATA SOURCES
def verify_sha256_checksum(path: Path, expected: str) -> str:
    chunk_size = 1024 * 64
    hash_sha256 = hashlib.sha256()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            hash_sha256.update(chunk)

    checksum = hash_sha256.hexdigest()
    if checksum != expected:
        raise ValueError(
            f'invalid checksum for {path}. expected {expected} but got {checksum}'
        )
    return checksum


def download(url: str, dest: Path) -> None:
    """https://stackoverflow.com/a/16696317/6928824"""
    print(f'downloading {url} to {dest}')
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(dest, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 16):
                file.write(chunk)


def replace_children_with_grandchildren(parent: Path) -> None:
    """Moves all grandchildren up one level and
    removes the then empty child directories.
    """
    child_dirs = [child for child in parent.iterdir() if child.is_dir()]
    for grandchild in parent.glob('*/*'):
        shutil.move(str(grandchild), str(parent))
    for child_dir in child_dirs:
        shutil.rmtree(child_dir)


###############################################################################
# IMAGES
def binarize(img: Image) -> Image:
    binary = img.clone()
    binary.format = 'png'
    # Set white background.
    binary.background_color = Color('white')
    # Remove transparency and replace with background_color.
    binary.alpha_channel = 'remove'

    binary.type = 'grayscale'
    binary.black_threshold(Color('white'))
    return binary


def get_bbox(img: Image, filename=None):
    binary = rgb2gray(np.array(binarize(img)))

    label_img = label(binary, background=1)
    regions = regionprops(label_img)

    if filename is not None:
        binarize(img).save(filename=f'binary-{filename}')
        Image.from_array(label_img.astype(float)).save(
            filename=f'labels-{filename}')

    assert len(regions) > 0, f'no objects detected for {filename}'
    if len(regions) == 1:
        region = regions[0]
    else:
        region = sorted(regions, key=lambda r: r.bbox_area, reverse=True)[0]
    return region.bbox


# def get_largest_bbox(bboxes) -> Tuple[float, float]:
#     max_width = 0
#     max_height = 0
#     for filename, bbox in bboxes.items():
#         width, height = bbox_size(bbox)
#         print(filename, width, height)
#         if width > max_width:
#             print('greater width')
#             max_width = width
#         if height > max_height:
#             print('greater height')
#             max_height = height

#     return max_width, max_height


def bbox_size(bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
    min_row, min_col, max_row, max_col = bbox
    width = max_col - min_col
    height = max_row - min_row
    return width, height


def get_scaling_factor(bbox: Tuple[int, int, int, int], final_size: Tuple[int, int], padding: int):
    width, height = bbox_size(bbox)
    return min(
        # x
        (final_size[0] - 2*padding) / width,
        # y
        (final_size[1] - 2*padding) / height,
    )


def extent_gravity_center(img: np.ndarray, width, height):
    """Helper function for apparently not working `wand.image.extent`
    with gravity and white background.
    See https://github.com/emcconville/wand/issues/554
    """

    img = Image.from_array(img)
    img.background_color = 'white'
    img.virtual_pixel = 'background'
    img.extent(
        width=width,
        height=height,
        x=(img.width - width) // 2,
        y=(img.height - height) // 2,
    )
    return img


def get_image_frames(filename: Path) -> Tuple[Image]:
    with Image(filename=filename) as img:
        return tuple(
            Image(frame, format='png')
            for frame in img.sequence
        )


# def save_image_frames(filename: Path, format: str = '{parent}/{stem}-{frame}{suffix}') -> None:
#     for i, frame in enumerate(get_image_frames(filename)):
#         frame.save(filename=format.format(
#             parent=filename.parent.name,
#             stem=filename.stem,
#             frame=i,
#             suffix=filename.suffix,
#         ))


def whiten_areas(filename: Path, coords: List[Tuple[int, int]], save_to: Path = None) -> None:
    if save_to is None:
        save_to = filename

    white = Color('white')
    with Image(filename=filename) as img:
        for x, y in coords:
            with Drawing() as draw:
                draw.fill_color = white
                draw.color(x, y, 'floodfill')
                draw.draw(img)
                img.save(filename=save_to)
