from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form


class Gen4(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/generation-4.tar.gz'
    checksum = 'b1b69463aac872b54adf56f1159e8e6d2dfcbbecb7d71c7ebf832fe44140da41'
    sprite_sets = {
        'pokemon/main-sprites/diamond-pearl': Conf(glob='*.png'),
        'pokemon/main-sprites/diamond-pearl/frame2': Conf(
            dest='diamond-pearl-frame2',
            glob='*.png',
        ),
        'pokemon/main-sprites/platinum': Conf(glob='*.png'),
        'pokemon/main-sprites/platinum/frame2': Conf(
            dest='platinum-frame2',
            glob='*.png',
        ),
        'pokemon/main-sprites/heartgold-soulsilver': Conf(glob='*.png'),
        'pokemon/main-sprites/heartgold-soulsilver/frame2': Conf(
            dest='heartgold-soulsilver-frame2',
            glob='*.png',
        ),
    }

    def assign_forms(self):
        return PathDict(**{
            'diamond-pearl/201': get_form(201, 'a'),
            'diamond-pearl/386-normal': get_form(386, Form.NORMAL),
            'diamond-pearl/412': get_form(412, 'plant'),
            'diamond-pearl/413': get_form(413, 'plant'),
            'diamond-pearl/421': get_form(421, 'overcast'),
            'diamond-pearl/422': get_form(422, 'west'),
            'diamond-pearl/423': get_form(423, 'west'),
            'diamond-pearl/487': get_form(487, 'altered'),
            'diamond-pearl/492': get_form(492, 'land'),
            'diamond-pearl/493-normal': get_form(493, Form.NORMAL),
            'diamond-pearl/493-unknown': DISMISS_FORM,  # invalid form
            'diamond-pearl-frame2/201*': DISMISS_FORM,  # empty image
            'diamond-pearl-frame2/386-normal': get_form(386, Form.NORMAL),
            'diamond-pearl-frame2/412': get_form(412, 'plant'),
            'diamond-pearl-frame2/413': get_form(413, 'plant'),
            'diamond-pearl-frame2/421': get_form(421, 'overcast'),
            'diamond-pearl-frame2/422': DISMISS_FORM,  # invalid form, seems mixed
            'diamond-pearl-frame2/423': DISMISS_FORM,  # invalid form, seems mixed
            'diamond-pearl-frame2/487': get_form(487, 'altered'),
            'diamond-pearl-frame2/492': get_form(492, 'land'),
            'diamond-pearl-frame2/493-normal': get_form(493, Form.NORMAL),
            'diamond-pearl-frame2/493-unknown': DISMISS_FORM,  # invalid form
            'platinum/201': get_form(201, 'a'),
            'platinum/386-normal': get_form(386, Form.NORMAL),
            'platinum/412': get_form(412, 'plant'),
            'platinum/413': get_form(413, 'plant'),
            'platinum/421': get_form(421, 'overcast'),
            'platinum/422': get_form(422, 'west'),
            'platinum/423': get_form(423, 'west'),
            'platinum/487': get_form(487, 'altered'),
            'platinum/492': get_form(492, 'land'),
            'platinum/493-normal': get_form(493, Form.NORMAL),
            'platinum/493-unknown': DISMISS_FORM,  # invalid form
            'platinum-frame2/201*': DISMISS_FORM,  # empty image
            'platinum-frame2/351*': DISMISS_FORM,  # empty image
            'platinum-frame2/386*': DISMISS_FORM,  # empty image
            'platinum-frame2/412': get_form(412, 'plant'),
            'platinum-frame2/413': get_form(413, 'plant'),
            'platinum-frame2/421': get_form(421, 'overcast'),
            'platinum-frame2/422': get_form(422, 'west'),
            'platinum-frame2/423': get_form(423, 'west'),
            'platinum-frame2/487': get_form(487, 'altered'),
            'platinum-frame2/492': get_form(492, 'land'),
            'platinum-frame2/493-normal': get_form(493, Form.NORMAL),
            'platinum-frame2/493-unknown': DISMISS_FORM,  # invalid form
            'heartgold-soulsilver/172-beta': DISMISS_FORM,  # invalid form
            'heartgold-soulsilver/201': get_form(201, 'a'),
            'heartgold-soulsilver/386-normal': get_form(386, Form.NORMAL),
            'heartgold-soulsilver/412': get_form(412, 'plant'),
            'heartgold-soulsilver/412-beta': DISMISS_FORM,
            'heartgold-soulsilver/413': get_form(413, 'plant'),
            'heartgold-soulsilver/421': get_form(421, 'overcast'),
            'heartgold-soulsilver/421-beta': DISMISS_FORM,
            # different animation frame than 422-west
            'heartgold-soulsilver/422': get_form(422, 'west'),
            # different animation frame than 423-west
            'heartgold-soulsilver/423': get_form(423, 'west'),
            'heartgold-soulsilver/487': get_form(487, 'altered'),
            'heartgold-soulsilver/492': get_form(492, 'land'),
            'heartgold-soulsilver/493-normal': get_form(493, Form.NORMAL),
            'heartgold-soulsilver/493-unknown': DISMISS_FORM,  # invalid form
            'heartgold-soulsilver/egg': DISMISS_FORM,  # no pokemon
            'heartgold-soulsilver/egg-manaphy': DISMISS_FORM,  # no pokemon
            'heartgold-soulsilver/substitute': DISMISS_FORM,  # no pokemon
            'heartgold-soulsilver-frame2/201*': DISMISS_FORM,  # empty image
            'heartgold-soulsilver-frame2/386-normal': get_form(386, Form.NORMAL),
            'heartgold-soulsilver-frame2/412': get_form(412, 'plant'),
            'heartgold-soulsilver-frame2/413': get_form(413, 'plant'),
            'heartgold-soulsilver-frame2/421': get_form(421, 'overcast'),
            'heartgold-soulsilver-frame2/422': get_form(422, 'west'),
            'heartgold-soulsilver-frame2/423': get_form(423, 'west'),
            'heartgold-soulsilver-frame2/487': get_form(487, 'altered'),
            'heartgold-soulsilver-frame2/492': get_form(492, 'land'),
            'heartgold-soulsilver-frame2/493-normal': get_form(493, Form.NORMAL),
            'heartgold-soulsilver-frame2/493-unknown': DISMISS_FORM,  # invalid form
            'heartgold-soulsilver-frame2/egg': DISMISS_FORM,  # no pokemon
            'heartgold-soulsilver-frame2/egg-manaphy': DISMISS_FORM,  # no pokemon
            'heartgold-soulsilver-frame2/substitute': DISMISS_FORM,  # no pokemon
        })
