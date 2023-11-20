from pathlib import Path
from typing import Union

import cv2
from python_assert import assert_dir


def load_image_dir(path: Union[Path, str], flag: int = cv2.IMREAD_COLOR):
    assert_dir(path)

    path = Path(path)
    supported_formats = (
        ".bmp",
        ".jpeg",
        ".jpg",
        ".png",
        ".tiff",
        ".tif",
        ".gif",
        ".webp",
        ".jp2",
        ".j2k",
        ".pbm",
        ".pgm",
        ".ppm",
        ".sr",
        ".ras",
        ".jpeg2000",
        ".exr",
    )

    for file in path.iterdir():
        if not file.is_file or not file.suffix in supported_formats:
            continue

        yield cv2.imread(str(file), flag)
