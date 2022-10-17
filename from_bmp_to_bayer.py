import click

import numpy as np
from PIL import Image
from tqdm import tqdm

from utils.color import Color, get_colors_map


@click.command()
@click.option(
    "--original_path", 
    type=click.Path(exists=True),
    required=True,
    help="Path to the .bmp image",
)
@click.option(
    "--output_path",
    type=click.Path(exists=False),
    help="Path to the resulting bayer image."
)
def main(original_path: click.Path, output_path: click.Path):
    with Image.open(str(original_path)) as img:
        original_np = np.array(img).astype(int)
        new_img = img.copy()
    
    colors = get_colors_map(original_np.shape[:2])
    for y in tqdm(range(original_np.shape[0])):
        for x in range(original_np.shape[1]):
            red = original_np[y][x][0]
            green = original_np[y][x][1]
            blue = original_np[y][x][2]

            if colors[y][x] == Color.RED:
                new_img.putpixel((x, y), (red, 0, 0))
            elif colors[y][x] == Color.GREEN:
                new_img.putpixel((x, y), (0, green, 0))
            elif colors[y][x] == Color.BLUE:
                new_img.putpixel((x, y), (0, 0, blue))

    new_img.save(str(output_path))
    

if __name__ == "__main__":
    main()