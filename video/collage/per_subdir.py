import os
import pathlib

import click
import numpy as np
from moviepy.editor import (ColorClip, VideoFileClip, clips_array,
                            concatenate_videoclips)


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
    count = 1
    n_subdirs = sum([1 for _ in input.iterdir()])

    output.mkdir(exist_ok=True, parents=True)

    for action in input.iterdir():
        print(f"{count}/{n_subdirs} {action.name}")

        if not os.path.isdir(action):
            continue

        count = 0
        clips = []
        group = []
        group_size = shape[0] * shape[1]

        for video in action.iterdir():
            if video.suffix != f".{extension}":
                continue

            count += 1

            group.append(VideoFileClip(str(video)))

            if count % group_size == 0:
                group = np.array(group).reshape(shape)
                group = clips_array(group)

                clips.append(group)

                group = []

        if len(group) > 0:
            max_size, max_width, max_height = 0, 0, 0

            for clip in group:
                if clip.w * clip.h > max_size:
                    max_size = clip.w * clip.h
                    max_width = clip.w
                    max_height = clip.h

            for count in range((count % group_size) + 1, group_size + 1):
                black = ColorClip((max_width, max_height), color=(0, 0, 0), duration=1)

                group.append(black)

            group = np.array(group).reshape(shape)
            group = clips_array(group)
            clips.append(group)

        concatenate_videoclips(clips).without_audio().write_videofile(
            str(output / (action.name + ".mp4"))
        )


if __name__ == "__main__":
    main()
