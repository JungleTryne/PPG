import click
import numpy as np

from PIL import Image


MAX_I = 255


def get_MSE(first: np.ndarray, second: np.ndarray) -> float:
    return np.sum((first - second) ** 2) / (first.shape[0] * first.shape[1]) # type: ignore


def get_PSNR(first: np.ndarray, second: np.ndarray) -> float:
    rmse = np.sqrt(get_MSE(first, second))
    return 20 * np.log10(MAX_I / rmse)


@click.command()
@click.option(
    "--original_path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the Bayer Filter .bmp image",
)
@click.option(
    "--recovered_path",
    type=click.Path(exists=False),
    required=True,
    help="Path to the resulting image. \
        If not specified, the image will be shown in a pop-up window."
)
def main(original_path: click.Path, recovered_path: click.Path):
    with Image.open(str(original_path)) as img:
        original = np.array(img)

    with Image.open(str(recovered_path)) as img:
        recovered = np.array(img)

    mse = get_MSE(original, recovered)
    psnr = get_PSNR(original, recovered)

    print(f"MSE: {mse}, PSNR: {psnr} db")


if __name__ == "__main__":
    main()
