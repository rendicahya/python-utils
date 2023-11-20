import os
from contextlib import nullcontext
from pathlib import Path
from typing import Union

from python_assert import assert_dir
from tqdm import tqdm


def iterate(
    path: Path, operation, extension=None, progress_bar=True, single=False
) -> None:
    n_files = count_files(path, recursive=True, extension=extension)

    with tqdm(total=n_files) if progress_bar else nullcontext() as bar:
        for action in path.iterdir():
            for video in action.iterdir():
                if video.suffix != extension:
                    continue

                if progress_bar:
                    bar.set_description(video.name[:30])
                    bar.update(1)

                operation(action, video)

                if single:
                    break

            if single:
                break


def count_files(path: Union[Path, str], recursive: bool = True, ext: str = None) -> int:
    assert_dir(path)

    path = Path(path)
    pattern = "**/*" if recursive else "*"
    ext = ".*" if ext is None else correct_suffix(ext)
    pattern += ext

    return sum(1 for f in path.glob(pattern))


def correct_suffix(suffix: str) -> str:
    return suffix if suffix.startswith(".") else "." + suffix
