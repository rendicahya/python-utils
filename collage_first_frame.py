import os
import pathlib

import click
import utils
from matplotlib import pyplot as plt
from moviepy.editor import VideoFileClip


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
    "--n-cols",
    "-c",
    type=int,
    nargs=1,
    default=4,
    help="The desired number of columns.",
)
def main(input, output, extension, n_cols):
    output.mkdir(exist_ok=True, parents=True)

    for action in input.iterdir():
        if not os.path.isdir(action):
            continue

        n_files = utils.count_files(action)
        n_rows = n_files // n_cols + 1
        fig = plt.figure(figsize=(n_cols * 3, n_rows * 2.5))

        plt.rcParams["font.size"] = 20
        plt.title(action.name)
        plt.axis("off")

        output_file = (output / action.name).with_suffix(".jpg")
        i = 0

        for video in action.iterdir():
            if video.suffix != f".{extension}":
                continue

            clip = VideoFileClip(str(video))
            frame = clip.get_frame(0)

            fig.add_subplot(n_rows, n_cols, i + 1)
            plt.axis("off")
            plt.imshow(frame)

            i += 1

        plt.savefig(output_file, bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    main()
