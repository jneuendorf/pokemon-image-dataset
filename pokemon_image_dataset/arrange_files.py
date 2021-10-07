from pathlib import Path
import shutil


# These sets contain PNG images with 1 pokemon each.
# After unpacking generation-*.tar.gz, pokemon-conquest.tar.gz, pokemon-icons.tar.gz
sprite_sets = (
    'black-white',
    'conquest',
    'crystal',
    'diamond-pearl',
    # 'dream-world',
    'emerald',
    'firered-leafgreen',
    'gold',
    'heartgold-soulsilver',
    'icons',
    'platinum',
    'red-blue',
    'red-green',
    'ruby-sapphire',
    'silver',
    'yellow',
    'yellow-gbc',
)



# print(p)
# print([x for x in p.iterdir() if x.name in sprite_sets])

def parse_pokedex_num(filename_no_suffix):
    # filename = filename_no_suffix
    # while len(filename) > 0:
    #     try:
    #         return int(filename)
    #     except ValueError:
    #         pass
    #     filename = filename[:-1]
    # raise ValueError(f'Invalid filename {filename_no_suffix}')
    try:
        num, *rest = filename_no_suffix.split('-')
        return int(num), '-'.join(rest)
    except ValueError:
        return None, filename_no_suffix


if __name__ == "__main__":
    for sprite_set in sprite_sets:
        p = Path('sprites') / sprite_set
        # print(p, type(p))
        # for file_path in p.iterdir():
        for file_path in p.glob('*.png'):
            pokedex_num, info = parse_pokedex_num(file_path.stem)
            pokedex_num_dir = (
                'unknown'
                if pokedex_num is None
                else str(pokedex_num)
            )
            dest_dir = Path('data') / pokedex_num_dir
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file_path = (
                dest_dir / f'{sprite_set}{"--" if info else ""}{info}.png'
            )
            # print(file_path, pokedex_num, info)
            # print('->', dest_file_path)
            # print()
            shutil.copy(file_path, dest_file_path)
