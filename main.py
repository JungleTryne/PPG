from typing import Optional
from pgg import PGGDemosaicer
from PIL import Image

import click


@click.command()
@click.option(
    "--bayer_path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the Bayer Filter .bmp image",
)
@click.option(
    "--output_path",
    type=click.Path(exists=False),
    help="Path to the resulting image. \
        If not specified, the image will be shown in a pop-up window."
)
def main(bayer_path: click.Path, output_path: Optional[click.Path]):
    with Image.open(str(bayer_path)) as img:
        demosaicer = PGGDemosaicer(img)

    new_img = demosaicer.demosaice()
    if not output_path:
        new_img.show()
    else:
        new_img.save(str(output_path))


if __name__ == "__main__":
    main()
