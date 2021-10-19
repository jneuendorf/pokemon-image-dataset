from cairosvg import svg2png

from pokemon_image_dataset.data_sources import PathDict
from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf
from pokemon_image_dataset.data_sources import SpriteSetDataSource
from pokemon_image_dataset.form import Form, get_form


class DreamWorld(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/pokemon-dream-world.tar.gz'
    checksum = 'eaaf06ea99e71e34d8710f5cfd4923b8cd4d62f44124930afd02bc17046b6057'
    sprite_sets = {
        'pokemon/dream-world': Conf(
            glob='*.svg',
            extra={
                # 521-female not available
                'female/592.svg': '592-female.svg',
                'female/593.svg': '593-female.svg',
            },
        ),
    }

    def run(self, force=False):
        super().run(force)
        self.svg2png()

    def assign_forms(self):
        return PathDict(**{
            'dream-world/201': get_form(201, 'a'),
            'dream-world/386-normal': get_form(386, Form.NORMAL),
            'dream-world/412': get_form(412, 'plant'),
            'dream-world/413': get_form(413, 'plant'),
            'dream-world/421': get_form(421, 'overcast'),
            'dream-world/422': get_form(422, 'west'),
            'dream-world/423': get_form(423, 'west'),
            'dream-world/487': get_form(487, 'altered'),
            'dream-world/492': get_form(492, 'land'),
            'dream-world/493-normal': get_form(493, Form.NORMAL),
            'dream-world/550': get_form(550, 'red-striped'),
            'dream-world/555': get_form(555, Form.NORMAL),
            'dream-world/555-standard': get_form(555, Form.NORMAL),
            'dream-world/585': get_form(585, 'spring'),
            'dream-world/586': get_form(586, 'spring'),
            'dream-world/592-female': get_form(592, Form.FEMALE),
            'dream-world/593-female': get_form(593, Form.FEMALE),
            'dream-world/641': get_form(641, 'incarnate'),
            'dream-world/642': get_form(642, 'incarnate'),
            'dream-world/645': get_form(645, 'incarnate'),
            'dream-world/647': get_form(647, 'ordinary'),
            'dream-world/648': get_form(648, 'aria'),
        })

    # TODO: Use wand? https://stackoverflow.com/a/19718153/6928824
    def svg2png(self):
        dest = self.tmp_dir / 'dream-world'
        for filename in dest.iterdir():
            with open(filename, 'rb') as file:
                svg2png(
                    file_obj=file,
                    write_to=str(dest / f'{filename.stem}.png'),
                )
            filename.unlink()
