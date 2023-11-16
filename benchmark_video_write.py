import shutil
from pathlib import Path

from file import assert_dir
from timer_py import Timer
from video import frames_to_video, get_frames, video_info

dataset_path = Path("/nas.dbms/randy/datasets/ucf101/ApplyEyeMakeup")

assert_dir(dataset_path)

timer = Timer()
target_dir = Path("benchmark-temp")
file_list = [str(file) for file in dataset_path.iterdir()]
libraries = "opencv", "moviepy"
dataset = {}

print(f"Extracting frames from {len(file_list)} videos...")

for file in file_list:
    frames = list(get_frames(file))
    info = video_info(file)
    filename = file.split("/")[-1]
    dataset[filename] = {"fps": info["fps"], "frames": frames}

for lib in libraries:
    timer.set_tag(lib)
    timer.start()

    for filename, data in dataset.items():
        target_path = (target_dir / lib / filename).with_suffix(".mp4")

        target_path.parent.mkdir(exist_ok=True, parents=True)
        frames_to_video(data["frames"], target=target_path, writer=lib, fps=data["fps"])

    timer.stop()

shutil.rmtree(target_dir)
