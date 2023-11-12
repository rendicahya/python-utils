import os
from contextlib import nullcontext
from pathlib import Path
from typing import Union

from tqdm import tqdm


def assert_dir(path: Union[Path, str], name: str) -> None:
    path = pathify(path)

    assert path.exists(), f"{name} not found."
    assert path.is_dir(), f"{name} must be a directory."
    assert os.access(path, os.R_OK), f"{name} not readable."


def assert_file(path: Union[Path, str], name: str, ext: str = None) -> None:
    path = pathify(path)

    assert path.exists(), f"{name} not found."
    assert path.is_file(), f"{name} must be a file."
    assert os.access(path, os.R_OK), f"{name} not readable."

    if ext is not None:
        ext = correct_suffix(ext)

        assert path.suffix == ext, f"{name} must be in a {ext} format."


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


def count_files(path: Union[Path, str], recursive=True, ext: str = None) -> int:
    assert_dir(path, 'Path for count_files()')

    path = pathify(path)
    pattern = "**/*" if recursive else "*"

    if ext is not None:
        pattern += correct_suffix(ext)

    return sum(1 for f in path.glob(pattern))


def correct_suffix(suffix: str) -> str:
    return suffix if suffix.startswith(".") else "." + suffix


def pathify(path: Union[Path, str]):
    return Path(path) if type(path) is str else path
