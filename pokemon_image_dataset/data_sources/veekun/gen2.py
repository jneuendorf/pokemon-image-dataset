from pokemon_image_dataset.data_sources import SpriteSetDataSource, PathDict
from pokemon_image_dataset.form import DISMISS_FORM, get_form


class Gen2(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/generation-2.tar.gz'
    checksum = '1a01266008cf726df5d273da96ec3cbbbd3da0f17bfada4b0b153a4c92b4517a'
    sprite_sets = {
        'pokemon/main-sprites/gold': dict(glob='*.png'),
        'pokemon/main-sprites/silver': dict(glob='*.png'),
        'pokemon/main-sprites/crystal': dict(glob='*.png'),
        'pokemon/main-sprites/crystal/animated': dict(dest='crystal-animated', glob='*.gif'),
    }

    def assign_forms(self):
        return PathDict(**{
            'gold/201': DISMISS_FORM,
            'silver/201': DISMISS_FORM,
            'crystal/201': DISMISS_FORM,
            'crystal-animated/201': get_form(201, 'u'),
        })
