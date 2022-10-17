from typing import Tuple
import numpy as np


class ImageWithPadding:
    def __init__(self, original: np.ndarray):
        self.original = original

    def __getitem__(self, pos: Tuple) -> int:
        y, x = pos
        if x >= 0 and x < self.original.shape[1]:
            if y >= 0 and y < self.original.shape[0]:
                return self.original[y][x]
        return 0

    def __setitem__(self, pos: Tuple, value: int) -> None:
        y, x = pos
        self.original[y][x] = value

    @property
    def shape(self):
        return self.original.shape
