from pathlib import Path

import utils
from moviepy.editor import VideoFileClip
from tqdm import tqdm

if __name__ == "__main__":
    input = Path("/nas.dbms/randy/datasets/ucf101")
    output = Path("/nas.dbms/randy/datasets/ucf101-mp4")

    assert input.exists() and input.is_dir()

    source_ext = ".avi"
    target_ext = ".mp4"
    mute = True
    n_files = utils.count_files(input, extension=source_ext)

    with tqdm(total=n_files) as bar:
        for input_video in input.rglob(f"*{source_ext}"):
            bar.set_description(input_video.name)

            relative_input_path = input_video.relative_to(input)
            output_video_path = output / relative_input_path.with_suffix(f"{target_ext}")

            output_video_path.parent.mkdir(parents=True, exist_ok=True)
            VideoFileClip(str(input_video)).write_videofile(
                str(output_video_path), logger=None, audio=not mute
            )
            bar.update(1)
