from typing import Union

import cv2
from file_utils import assert_file, pathify


def get_video_writer_like(path: Union[Path, str], format: str = "mp4"):
    assert_file(path, "Input video")

    fourcc_formats = {"mp4": "mp4v"}
    video = cv2.VideoCapture(str(file))
    fourcc_format = fourcc_formats[format]
    fourcc = cv2.VideoWriter_fourcc(*fourcc_format)
    fps = float(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return cv2.VideoWriter(
        str(path),
        fourcc,
        fps,
        (width, height),
    )
