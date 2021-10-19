from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form


class Icons(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/pokemon-icons.tar.gz'
    checksum = 'f9850ce82d8e6e69c163112c47553458fd27805034217a5331a1ae12b2a1c8ac'
    sprite_sets = {
        'pokemon/icons': Conf(
            glob='*.png',
            extra={
                'female/521.png': '521-female.png',
                'female/592.png': '592-female.png',
                'female/593.png': '593-female.png',
                'female/668.png': '668-female.png',
                'female/678.png': '678-female.png',
            },
        ),
    }

    def assign_forms(self):
        return PathDict(**{
            'icons/25-cosplay': get_form(25, 'cosplay'),
            'icons/25-rock-star': get_form(25, 'cosplay-rock-star'),
            'icons/25-belle': get_form(25, 'cosplay-belle'),
            'icons/25-pop-star': get_form(25, 'cosplay-pop-star'),
            'icons/25-phd': get_form(25, 'cosplay-phd'),
            'icons/25-libre': get_form(25, 'cosplay-libre'),
            'icons/201': get_form(201, 'a'),
            'icons/386-normal': get_form(386, Form.NORMAL),
            'icons/412': get_form(412, 'plant'),
            'icons/413': get_form(413, 'plant'),
            'icons/421': get_form(421, 'overcast'),
            'icons/422': get_form(422, 'west'),
            'icons/423': get_form(423, 'west'),
            'icons/487': get_form(487, 'altered'),
            'icons/492': get_form(492, 'land'),
            'icons/493-*': DISMISS_FORM,  # invalid forms (equal normal)
            'icons/550': get_form(550, 'red-striped'),
            'icons/555': get_form(555, Form.NORMAL),
            'icons/555-standard': get_form(555, Form.NORMAL),
            'icons/555-zen': get_form(555, 'zen'),
            'icons/585': get_form(585, 'spring'),
            'icons/586': get_form(586, 'spring'),
            'icons/641': get_form(641, 'incarnate'),
            'icons/642': get_form(642, 'incarnate'),
            'icons/645': get_form(645, 'incarnate'),
            'icons/647': get_form(647, 'ordinary'),
            'icons/648': get_form(648, 'aria'),
            'icons/649-*': DISMISS_FORM,  # invalid forms (equal normal)
            'icons/666': get_form(666, 'meadow'),
            'icons/669': get_form(669, 'red'),
            'icons/670': get_form(670, 'red'),
            'icons/670-eternal': DISMISS_FORM,  # unknown form
            'icons/671': get_form(671, 'red'),
            'icons/676': get_form(676, Form.NORMAL),
            'icons/676-natural': get_form(676, Form.NORMAL),
            'icons/678-male': get_form(678, Form.NORMAL),
            'icons/678-female': get_form(678, Form.FEMALE),
            'icons/681': get_form(681, 'shield'),
            'icons/710-*': DISMISS_FORM,
            'icons/711-*': DISMISS_FORM,
            'icons/716': get_form(716, 'active'),
            'icons/718': get_form(718, '50-percent'),
            'icons/720': get_form(720, 'confined'),
            'icons/egg': DISMISS_FORM,
        })
