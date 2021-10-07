from pathlib import Path


DESTINATION_DIR = Path('data')


# 1. resize all to the maximum size
# https://scikit-image.org/docs/dev/api/skimage.transform.html#resize

def find_max_size(dest_dir):
    for pokedex_num_dir in dest_dir.iterdir():
        if pokedex_num_dir.is_dir():
            ...



# 2. PNG with alpha to JPEG with white
# https://stackoverflow.com/a/36279291/6928824


# 3. equalize padding
# NOTE: Different pokemon have different padding in the same sprite set
# => like EMNIST we make the padding the same for all pokemon (regardless their actual size)
