from typing import Tuple
import numpy as np


class Color:
    RED = 0
    GREEN = 1
    BLUE = 2


def get_colors_map(dimensions: Tuple[int]) -> np.ndarray:
    def change_color(color: Color):
        if color == Color.RED:
            return Color.BLUE
        return Color.RED

    color_row = Color.BLUE
    colors = np.zeros(dimensions)
    is_green_next = True
    for y in range(colors.shape[0]):
        color_row = change_color(color_row)  # type: ignore
        is_green_next = True if not is_green_next else False
        for x in range(colors.shape[1]):
            colors[y, x] = Color.GREEN if is_green_next else color_row
            is_green_next = True if not is_green_next else False

    return colors
