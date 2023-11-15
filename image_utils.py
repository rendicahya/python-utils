from pathlib import Path
from typing import Union
from file_utils import assert_dir
import cv2


def load_image_dir(path: Union[Path, str], flag: int = cv2.IMREAD_COLOR):
    assert_dir(path)

    path = Path(path)

    for file in path.iterdir():
        yield cv2.imread(str(file), flag)
