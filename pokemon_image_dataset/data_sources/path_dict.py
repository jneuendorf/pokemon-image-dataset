from pathlib import Path
from typing import Dict, Optional, TypeVar, Generic

T = TypeVar('T')


class PathDict(Generic[T], dict):
    """Keys are strings representing paths.
    Item access happens with `Path` instances.
    """

    @classmethod
    def with_prefix(cls, prefix: str, kwargs: Dict[str, T]):
        return cls({
            f'{prefix}{key}': value
            for key, value in kwargs.items()
        })

    def __getitem__(self, path: Path) -> Optional[T]:
        # assert isinstance(
        #     path, Path), f'expected key to be a Path but got {type(path).__name__}'
        for key, val in self.items():
            if path.match(key) or path.with_suffix('').match(key):
                return val
        return None
