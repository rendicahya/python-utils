import os
import pathlib

import click
import numpy as np
from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips


@click.command()
@click.argument(
    "input",
    nargs=1,
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.argument(
    "output",
    nargs=1,
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True,
        writable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--extension",
    "-x",
    type=str,
    nargs=1,
    default="mp4",
    help="The filename extension filter.",
)
@click.option(
    "--shape",
    "-s",
    type=int,
    nargs=2,
    default=(2, 3),
    help="The shape (# of rows and columns) of the collage.",
)
def main(input, output, extension, shape):
    for action in input.iterdir():
        if not os.path.isdir(action):
            continue

        count = 0
        clips = []
        group = []

        for video in action.iterdir():
            if video.suffix != f".{extension}":
                continue

            count += 1

            group.append(VideoFileClip(str(video)))

            if count % (shape[0] * shape[1]) == 0:
                group = np.array(group).reshape(shape)
                group = clips_array(group)

                clips.append(group)

                group = []

        concatenate_videoclips(clips).without_audio().write_videofile(
            str(output / (action.name + ".mp4"))
        )


if __name__ == "__main__":
    main()
