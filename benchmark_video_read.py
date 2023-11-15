import pathlib

from file_utils import assert_dir
from timer_py import Timer
from video_utils import *

timer = Timer()
dataset_path = pathlib.Path("../../datasets/ucf101/ApplyEyeMakeup")

assert_dir(dataset_path)

file_list = [str(file) for file in dataset_path.glob(f"**/*.avi")]
libraries = "opencv", "moviepy", "pyav", "decord"

print(f"Benchmarking with {len(file_list)} videos...")

for lib in libraries:
    timer.set_tag(lib)
    timer.start()

    for file in file_list:
        frames = list(get_frames(file, reader=lib))

    timer.stop()
