from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form


class Sugimori(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/pokemon-sugimori.tar.gz'
    checksum = '9dcb5ab803725db99ec235df72da9cc20e96ac843d88394cff95a6b0bb06da16'
    sprite_sets = {
        'pokemon/sugimori': Conf(
            glob='*.png',
            extra={
                'female/521.png': '521-female.png',
                'female/592.png': '592-female.png',
                'female/593.png': '593-female.png',
                'female/668.png': '668-female.png',
            },
        ),
    }

    def assign_forms(self):
        return PathDict(**{
            'sugimori/25-cosplay': get_form(25, 'cosplay'),
            'sugimori/25-rock-star': get_form(25, 'cosplay-rock-star'),
            'sugimori/25-belle': get_form(25, 'cosplay-belle'),
            'sugimori/25-pop-star': get_form(25, 'cosplay-pop-star'),
            'sugimori/25-phd': get_form(25, 'cosplay-phd'),
            'sugimori/25-libre': get_form(25, 'cosplay-libre'),
            'sugimori/201-f': get_form(201, 'f'),
            'sugimori/201': get_form(201, 'f'),
            'sugimori/386-normal': get_form(386, Form.NORMAL),
            'sugimori/412': get_form(412, 'plant'),
            'sugimori/413': get_form(413, 'plant'),
            'sugimori/421': get_form(421, 'sunshine'),
            'sugimori/422': get_form(422, 'east'),
            'sugimori/423': get_form(423, 'east'),
            'sugimori/487': get_form(487, 'altered'),
            'sugimori/492': get_form(492, 'land'),
            'sugimori/493-normal': get_form(493, Form.NORMAL),
            'sugimori/521-female': get_form(521, Form.FEMALE),
            'sugimori/550': get_form(550, 'red-striped'),
            'sugimori/555': get_form(555, Form.NORMAL),
            'sugimori/555-standard': get_form(555, Form.NORMAL),
            'sugimori/585': get_form(585, 'spring'),
            'sugimori/586': get_form(586, 'spring'),
            'sugimori/592-female': get_form(592, Form.FEMALE),
            'sugimori/593-female': get_form(593, Form.FEMALE),
            'sugimori/641': get_form(641, 'incarnate'),
            'sugimori/642': get_form(642, 'incarnate'),
            'sugimori/645': get_form(645, 'incarnate'),
            'sugimori/647': get_form(647, 'ordinary'),
            'sugimori/648': get_form(648, 'aria'),
            # TODO: 666 equals 666-meadow but is the actual sugimori image
            'sugimori/666': get_form(666, 'meadow'),
            'sugimori/668-female': get_form(668, Form.FEMALE),
            'sugimori/669': get_form(669, 'red'),
            'sugimori/670': get_form(670, 'red'),
            'sugimori/671': get_form(671, 'red'),
            'sugimori/676': get_form(676, Form.NORMAL),
            'sugimori/678': get_form(678, Form.NORMAL),
            'sugimori/678-female': get_form(678, Form.FEMALE),
            'sugimori/681': DISMISS_FORM,  # both forms in 1 image
            'sugimori/716': get_form(716, 'active'),
            'sugimori/718': get_form(718, '50-percent'),
            'sugimori/720': get_form(720, 'confined'),
        })
