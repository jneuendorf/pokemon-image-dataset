from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form


class Gen5(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/generation-5.tar.gz'
    checksum = 'ee037a3319b2a6143c5c90f679be13a06126c2f5424e46023fe0f53d2631aa62'
    sprite_sets = {
        'pokemon/main-sprites/black-white': Conf(
            glob='*.png',
            extra={
                'female/521.png': '521-female.png',
                'female/592.png': '592-female.png',
                'female/593.png': '593-female.png',
            },
        ),
    }

    def assign_forms(self):
        return PathDict(**{
            'black-white/0': DISMISS_FORM,  # no pokemon
            'black-white/201': get_form(201, 'a'),
            'black-white/386-normal': get_form(386, Form.NORMAL),
            'black-white/412': get_form(412, 'plant'),
            'black-white/413': get_form(413, 'plant'),
            'black-white/421': get_form(421, 'overcast'),
            'black-white/422': get_form(422, 'west'),
            'black-white/423': get_form(423, 'west'),
            'black-white/487': get_form(487, 'altered'),
            'black-white/492': get_form(492, 'land'),
            'black-white/493-normal': get_form(493, Form.NORMAL),
            'black-white/550': get_form(550, 'red-striped'),
            'black-white/555': get_form(555, Form.NORMAL),
            'black-white/555-standard': get_form(555, Form.NORMAL),
            'black-white/555-zen': get_form(555, 'zen'),
            'black-white/585': get_form(585, 'spring'),
            'black-white/586': get_form(586, 'spring'),
            'black-white/641': get_form(641, 'incarnate'),
            'black-white/642': get_form(642, 'incarnate'),
            'black-white/645': get_form(645, 'incarnate'),
            'black-white/647': get_form(647, 'ordinary'),
            'black-white/648': get_form(648, 'aria'),
            'black-white/female/521': get_form(521, Form.FEMALE),
            'black-white/female/592': get_form(592, Form.FEMALE),
            'black-white/female/593': get_form(593, Form.FEMALE),
            'black-white/egg': DISMISS_FORM,  # no pokemon
            'black-white/egg-manaphy': DISMISS_FORM,  # no pokemon
            'black-white/substitute': DISMISS_FORM,  # no pokemon
        })
