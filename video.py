import types
from pathlib import Path
from typing import Union

import av
import cv2
from decord import VideoReader, cpu
from file import assert_dir, assert_file
from moviepy.editor import ImageSequenceClip, VideoFileClip


def video_info(path: Union[Path, str], reader: str = "opencv"):
    assert_file(path)

    assert reader in (
        "opencv",
        "moviepy",
    ), 'Reader must be one of ["opencv", "moviepy"]'

    if reader == "opencv":
        video = cv2.VideoCapture(str(path))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    elif reader == "moviepy":
        clip = VideoFileClip(str(path))
        width = clip.w
        height = clip.h
        fps = clip.fps
        n_frames = clip.reader.nframes

    return {"width": width, "height": height, "fps": fps, "n_frames": n_frames}


def video_writer_like(path: Union[Path, str], format: str = "mp4"):
    assert_file(path)

    fourcc_formats = {"mp4": "mp4v"}
    fourcc_format = fourcc_formats[format]
    fourcc = cv2.VideoWriter_fourcc(*fourcc_format)
    info = video_info(path)
    width = info["width"]
    height = info["height"]
    fps = info["fps"]

    return cv2.VideoWriter(
        str(path),
        fourcc,
        fps,
        (width, height),
    )


def get_frames(path: Union[Path, str], reader: str = "opencv"):
    assert_file(path)

    assert reader in (
        "opencv",
        "moviepy",
        "pyav",
        "decord",
    ), 'Reader must be one of ["opencv", "moviepy", "pyav", "decord"]'

    if reader == "opencv":
        cap = cv2.VideoCapture(str(path))

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            yield frame

        cap.release()
    elif reader == "moviepy":
        with VideoFileClip(path) as clip:
            for frame in clip.iter_frames():
                yield frame
    elif reader == "pyav":
        with av.open(path) as container:
            for frame in container.decode(video=0):
                yield frame.to_ndarray(format="rgb24")
    elif reader == "decord":
        with open(path, "rb") as f:
            video_reader = VideoReader(f, ctx=cpu(0))

            for i in range(len(video_reader)):
                yield video_reader[i].asnumpy()


def frames_to_video(
    frames: Union[list, types.GeneratorType],
    target: Union[Path, str] = "video.mp4",
    writer: str = "opencv",
    fps: int = 30,
    codec: str = "mp4v",
) -> None:
    assert writer in (
        "opencv",
        "moviepy",
        # "pyav",
    ), 'Writer must be one of ["opencv", "moviepy"]'

    assert_dir(Path(target).parent)

    if writer == "opencv":
        fourcc = cv2.VideoWriter_fourcc(*codec)
        first_frame = next(frames) if type(frames) == types.GeneratorType else frames[0]
        height, width = first_frame.shape[:2]

        video_writer = cv2.VideoWriter(
            str(target),
            fourcc,
            fps,
            (width, height),
        )

        # If frames is a generator, the first frame has been
        # extracted above (next(frames)), so it should be written
        if type(frames) == types.GeneratorType:
            video_writer.write(first_frame)

        for frame in frames:
            video_writer.write(frame)

        video_writer.release()
    elif writer == "moviepy":
        ImageSequenceClip(list(frames), fps=fps).write_videofile(str(target), logger=None)
    # elif writer == "pyav":
    #     with av.open(str(target), "w", format="mp4") as container:
    #         out_stream = container.add_stream("h264", fps)

    #         for frame in frames:
    #             new_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
    #             new_frame = out_stream.encode(new_frame)
    #             container.mux(new_frame)
