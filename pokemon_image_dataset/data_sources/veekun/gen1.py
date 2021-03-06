from pokemon_image_dataset.data_sources import SpriteSetConfig as Conf, SpriteSetDataSource


class Gen1(SpriteSetDataSource):
    url = 'https://veekun.com/static/pokedex/downloads/generation-1.tar.gz'
    checksum = '2d0923f5abf1171b7e011b3ce9b879e8eee1fd56ec82dfbe597a2eafa63ca21c'
    sprite_sets = {
        'pokemon/main-sprites/red-blue': Conf(glob='*.png'),
        'pokemon/main-sprites/red-green': Conf(glob='*.png'),
        'pokemon/main-sprites/yellow': Conf(glob='*.png'),
        'pokemon/main-sprites/yellow/gbc': Conf(dest='yellow-gbc', glob='*.png'),
    }
