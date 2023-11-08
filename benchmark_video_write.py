from pathlib import Path

import av
import cv2
from decord import VideoReader, cpu
from moviepy.editor import ImageSequenceClip
from timer_py import Timer


def extract_data(file_list):
    frame_bank = {}

    for file in file_list:
        with open(file, "rb") as f:
            vr = VideoReader(f, ctx=cpu(0))
            filename = file.split("/")[-1]
            frames = [vr[i].asnumpy() for i in range(len(vr))]
            frame_bank[filename] = {"fps": vr.get_avg_fps(), "frames": frames}

    return frame_bank


def test_pyav(dataset, target_dir):
    for filename, data in dataset.items():
        target_path = (target_dir / "pyav" / filename).with_suffix(".mp4")
        target_path.parent.mkdir(exist_ok=True, parents=True)

        with av.open(str(target_path), "w", format="mp4") as container:
            output_stream = container.add_stream("h264", data["fps"])

            for frame in data["frames"]:
                new_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
                new_frame = output_stream.encode(new_frame)
                container.mux(new_frame)


def test_moviepy(dataset, target_dir):
    for filename, data in dataset.items():
        target_path = (target_dir / "moviepy" / filename).with_suffix(".mp4")

        target_path.parent.mkdir(exist_ok=True, parents=True)
        ImageSequenceClip(data["frames"], fps=data["fps"]).write_videofile(
            str(target_path), audio=False, logger=None
        )


def test_opencv(dataset, target_dir):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    for filename, data in dataset.items():
        target_path = (target_dir / "opencv" / filename).with_suffix(".mp4")
        target_path.parent.mkdir(exist_ok=True, parents=True)

        height, width, _ = data["frames"][0].shape
        video = cv2.VideoWriter(str(target_path), fourcc, data["fps"], (width, height))

        for frame in data["frames"]:
            video.write(frame)

        video.release()


if __name__ == "__main__":
    dataset_path = Path("/nas.dbms/randy/datasets/ucf101/ApplyEyeMakeup")

    assert dataset_path.exists() and dataset_path.is_dir()

    timer = Timer()
    target_path = Path("benchmark-temp")
    extension = ".avi"
    file_list = [str(file) for file in dataset_path.glob(f"**/*{extension}")]

    print("Extracting frames...")
    dataset = extract_data(file_list)

    print("Benchmarking MoviePy...")
    timer.set_tag("MoviePy")
    timer.start()
    test_moviepy(dataset, target_path)
    timer.stop()

    print("Benchmarking OpenCV...")
    timer.set_tag("OpenCV")
    timer.start()
    test_opencv(dataset, target_path)
    timer.stop()

    print("Benchmarking PyAV...")
    timer.set_tag("PyAV")
    timer.start()
    test_pyav(dataset, target_path)
    timer.stop()
