from pathlib import Path
from typing import Tuple, Type

from pokemon_image_dataset.data_sources import (
    DataSource,
    BattlersDataSource,
    veekun,
)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent / 'tmp'
    print(BASE_DIR)

    data_sources_classes: Tuple[Type[DataSource]] = (
        veekun.Gen1,
        veekun.Gen2,
        veekun.Gen3,
        veekun.Gen4,
        veekun.Gen5,
        veekun.Icons,
        veekun.Sugimori,
        veekun.DreamWorld,
        BattlersDataSource,
    )
    data_sources: Tuple[DataSource] = tuple(
        DataSource(tmp_dir=BASE_DIR)
        for DataSource in data_sources_classes
    )

    for data_source in data_sources:
        print(f'running {data_source.__class__.__name__}')
        data_source.run(force=False)
