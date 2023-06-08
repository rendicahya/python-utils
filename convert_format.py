import pathlib

import click
import utils
from moviepy.editor import VideoFileClip
from tqdm import tqdm


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
@click.argument(
    "source-format",
    type=str,
    nargs=1,
    required=True,
)
@click.argument(
    "dest-format",
    type=str,
    nargs=1,
    required=True,
)
def main(input, output, source_format, dest_format):
    n_files = utils.count_files(input, extension=source_format)

    with tqdm(total=n_files) as bar:
        for input_video in input.rglob(f"*.{source_format}"):
            bar.set_description(input_video.name)
            
            relative_input_path = input_video.relative_to(input)
            output_video_path = output / relative_input_path.with_suffix(
                f".{dest_format}"
            )

            output_video_path.parent.mkdir(parents=True, exist_ok=True)
            VideoFileClip(str(input_video)).write_videofile(
                str(output_video_path), logger=None
            )
            bar.update(1)


if __name__ == "__main__":
    main()
