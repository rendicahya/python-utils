import concurrent.futures
import pathlib

import av
import cv2
from decord import VideoReader, cpu, gpu
from moviepy.editor import VideoFileClip
from timer_py import Timer

timer = Timer()
dataset_path = pathlib.Path("/nas.dbms/randy/datasets/ucf101/ApplyEyeMakeup")
video_list = [str(file) for file in dataset_path.iterdir() if file.is_file()]

print(f"Benchmarking with {len(video_list)} videos...")

timer.set_tag("OpenCV")
timer.start()

for file in video_list:
    cap = cv2.VideoCapture(file)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

    cap.release()

timer.stop()

timer.set_tag("MoviePy")
timer.start()

for file in video_list:
    with VideoFileClip(file) as clip:
        for frame in clip.iter_frames():
            pass

timer.stop()

timer.set_tag("PyAV")
timer.start()

for file in video_list:
    with av.open(file) as container:
        for frame in container.decode(video=0):
            pass

timer.stop()

timer.set_tag("Decord")
timer.start()

for file in video_list:
    with open(file, "rb") as f:
        vr = VideoReader(f, ctx=cpu(0))

        for i in range(len(vr)):
            frame = vr[i]

timer.stop()
