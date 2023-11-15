from file_utils import *
from video_utils import *
from pathlib import Path

input = "v_Basketball_g01_c01.avi"
target = Path("video.mp4")

assert_file(input)

frames = get_frames(input, reader="pyav")
info = video_info(input, reader="opencv")

print("Source video:", info)
frames_to_video(frames, target=target, writer="moviepy", fps=info["fps"], codec="mp4v")

info = video_info(target, reader="opencv")
print("Result video:", info)

target.unlink()
