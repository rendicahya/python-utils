import pathlib

import av
import cv2
import torchvision as tv
from decord import VideoReader, cpu
from moviepy.editor import VideoFileClip
from timer_py import Timer


def test_torchvision(file_list):
    for file in file_list:
        reader = tv.io.VideoReader(file)

        for frame in reader:
            pass


def test_opencv(file_list):
    for file in file_list:
        cap = cv2.VideoCapture(file)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

        cap.release()


def test_moviepy(file_list):
    for file in file_list:
        with VideoFileClip(file) as clip:
            fps = clip.fps

            for frame in clip.iter_frames():
                pass


def test_pyav(file_list):
    for file in file_list:
        with av.open(file) as container:
            fps = container.streams.video[0].average_rate

            for frame in container.decode(video=0):
                frame_np = frame.to_ndarray()


def test_decord(file_list):
    for file in file_list:
        with open(file, "rb") as f:
            vr = VideoReader(f, ctx=cpu(0))
            fps = vr.get_avg_fps

            for i in range(len(vr)):
                frame = vr[i].asnumpy()  # RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


def main():
    timer = Timer()
    dataset_path = pathlib.Path("../../../datasets/ucf101/ApplyEyeMakeup")

    assert dataset_path.exists() and dataset_path.is_dir()

    extension = ".avi"
    file_list = [str(file) for file in dataset_path.glob(f"**/*{extension}")]

    print(f"Benchmarking with {len(file_list)} videos...")

    timer.set_tag("OpenCV")
    timer.start()
    test_opencv(file_list)
    timer.stop()

    timer.set_tag("MoviePy")
    timer.start()
    test_moviepy(file_list)
    timer.stop()

    timer.set_tag("PyAV")
    timer.start()
    test_pyav(file_list)
    timer.stop()

    timer.set_tag("Decord")
    timer.start()
    test_decord(file_list)
    timer.stop()

    # timer.set_tag("Torchvision")
    # timer.start()
    # test_torchvision(file_list)
    # timer.stop()


if __name__ == "__main__":
    main()