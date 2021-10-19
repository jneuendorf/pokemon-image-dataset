from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form


class Gen3(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/generation-3.tar.gz'
    checksum = '15b733baf9ef91fbde3ae957edb4d2ba75615601a515b41590ab87043370319c'
    sprite_sets = {
        'pokemon/main-sprites/ruby-sapphire': Conf(glob='*.png'),
        'pokemon/main-sprites/emerald': Conf(glob='*.png'),
        'pokemon/main-sprites/emerald/animated': Conf(
            dest='emerald-animated',
            glob='*.gif',
            post_process='split_gif_frames',
        ),
        'pokemon/main-sprites/emerald/frame2': Conf(dest='emerald-frame2', glob='*.png'),
        'pokemon/main-sprites/firered-leafgreen': Conf(glob='*.png'),
    }

    def assign_forms(self):
        return PathDict(**{
            'ruby-sapphire/201': get_form(201, 'j'),
            'ruby-sapphire/386-normal': get_form(386, Form.NORMAL),
            'emerald/201': get_form(201, 'j'),
            'emerald/386-normal': get_form(386, Form.NORMAL),
            'emerald-animated/386-normal': get_form(386, Form.NORMAL),
            'emerald-frame2/201*': DISMISS_FORM,  # empty image
            'emerald-frame2/327': DISMISS_FORM,  # empty image
            'emerald-frame2/351*': DISMISS_FORM,  # empty image
            'emerald-frame2/386*': DISMISS_FORM,  # empty image
            'firered-leafgreen/386-normal': get_form(386, Form.NORMAL),
        })
