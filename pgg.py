import numpy as np
from PIL import Image
from utils.color import Color, get_colors_map
from utils.general import ImageWithPadding
from tqdm import tqdm


class PGGDemosaicer:
    def __init__(self, bayer_filter: Image.Image):
        bayer_filter_3d = np.array(bayer_filter).astype(int)

        self.bayer_filter = ImageWithPadding(
            self._flatten_bayer(bayer_filter_3d))
        self.colors = ImageWithPadding(get_colors_map(self.bayer_filter.shape))
        self.green_layer = ImageWithPadding(
            np.zeros_like(self.bayer_filter.original))
        self.red_layer = ImageWithPadding(
            np.zeros_like(self.bayer_filter.original))
        self.blue_layer = ImageWithPadding(
            np.zeros_like(self.bayer_filter.original))

        self.new_img = bayer_filter.copy()

    def demosaice(self) -> Image.Image:
        self._recover_green()
        self._recover_red_and_blue()
        self._clip_values()
        return self._merge_channels()

    def _clip_values(self):
        self.red_layer.original = np.clip(self.red_layer.original, 0, 255)
        self.green_layer.original = np.clip(self.green_layer.original, 0, 255)
        self.blue_layer.original = np.clip(self.blue_layer.original, 0, 255)

    def _merge_channels(self) -> Image.Image:
        for y in range(self.new_img.size[1]):
            for x in range(self.new_img.size[0]):
                red_value = self.red_layer[y, x]
                green_value = self.green_layer[y, x]
                blue_value = self.blue_layer[y, x]

                self.new_img.putpixel(
                    (x, y), (red_value, green_value, blue_value))
        return self.new_img

    def _recover_green(self):
        for y in tqdm(range(self.colors.shape[0])):
            for x in range(self.colors.shape[1]):
                if self.colors[y, x] == Color.GREEN:
                    self.green_layer[y, x] = self.bayer_filter[y, x]
                    continue

                delta_N = self.get_delta_N(x, y)
                delta_E = self.get_delta_E(x, y)
                delta_W = self.get_delta_W(x, y)
                delta_S = self.get_delta_S(x, y)

                all_deltas = [delta_N, delta_W, delta_E, delta_S]
                if delta_N == min(all_deltas):
                    self.green_layer[y, x] = int((self.bayer_filter[y - 1, x] * 3 + self.bayer_filter[y + 1, x] +
                                                  self.bayer_filter[y, x] - self.bayer_filter[y - 2, x]) / 4)
                elif delta_E == min(all_deltas):
                    self.green_layer[y, x] = int((self.bayer_filter[y, x + 1] * 3 + self.bayer_filter[y, x - 1] +
                                                  self.bayer_filter[y, x] - self.bayer_filter[y, x + 2]) / 4)
                elif delta_W == min(all_deltas):
                    self.green_layer[y, x] = int((self.bayer_filter[y, x - 1] * 3 + self.bayer_filter[y, x + 1] +
                                                  self.bayer_filter[y, x] - self.bayer_filter[y, x - 2]) / 4)
                elif delta_S == min(all_deltas):
                    self.green_layer[y, x] = int((self.bayer_filter[y + 1, x] * 3 + self.bayer_filter[y - 1, x] +
                                                  self.bayer_filter[y, x] - self.bayer_filter[y + 2, x]) / 4)

    def _hue_transit(self, l1: int, l2: int, l3: int, v1: int, v3: int) -> int:
        if (l1 < l2 and l2 < l3) or (l1 > l2 and l2 > l3):
            return v1 + (v3 - v1) * (l2 - l1) // (l3 - l1)
        return (v1 + v3) // 2 + (l2 * 2 - l1 - l3) // 4

    def get_delta_NE(self, x: int, y: int):
        c9 = self.bayer_filter[y - 1, x + 1]
        c17 = self.bayer_filter[y + 1, x - 1]

        c5 = self.bayer_filter[y - 2, x + 2]
        c13 = self.bayer_filter[y, x]
        c21 = self.bayer_filter[y + 2, x - 2]

        g9 = self.green_layer[y - 1, x + 1]
        g13 = self.green_layer[y, x]
        g17 = self.green_layer[y + 1, x - 1]

        return abs(c9 - c17) + abs(c5 - c13) + abs(c13 + c21) + abs(g9 - g13) + abs(g13 - g17)

    def get_delta_NW(self, x: int, y: int):
        c7 = self.bayer_filter[y - 1, x - 1]
        c19 = self.bayer_filter[y + 1, x + 1]

        c1 = self.bayer_filter[y - 2, x - 2]
        c13 = self.bayer_filter[y, x]
        c25 = self.bayer_filter[y + 2, x + 2]

        g7 = self.green_layer[y - 1, x - 1]
        g13 = self.green_layer[y, x]
        g19 = self.green_layer[y + 1, x + 1]

        return abs(c7 - c19) + abs(c1 - c13) + abs(c13 + c25) + abs(g7 - g13) + abs(g13 - g19)

    def _recover_blue_on_red(self, x: int, y: int):
        delta_NE = self.get_delta_NE(x, y)
        delta_NW = self.get_delta_NW(x, y)
        if delta_NE < delta_NW:
            self.blue_layer[y, x] = self._hue_transit(
                self.green_layer[y - 1, x + 1],
                self.green_layer[y, x],
                self.green_layer[y + 1, x - 1],
                self.bayer_filter[y - 1, x + 1],
                self.bayer_filter[y + 1, x - 1],
            )
        else:
            self.blue_layer[y, x] = self._hue_transit(
                self.green_layer[y - 1, x - 1],
                self.green_layer[y, x],
                self.green_layer[y + 1, x + 1],
                self.bayer_filter[y - 1, x - 1],
                self.bayer_filter[y + 1, x + 1],
            )

    def _recover_red_on_blue(self, x: int, y: int):
        delta_NE = self.get_delta_NE(x, y)
        delta_NW = self.get_delta_NW(x, y)
        if delta_NE < delta_NW:
            self.red_layer[y, x] = self._hue_transit(
                self.green_layer[y - 1, x + 1],
                self.green_layer[y, x],
                self.green_layer[y + 1, x - 1],
                self.bayer_filter[y - 1, x + 1],
                self.bayer_filter[y + 1, x - 1],
            )
        else:
            self.red_layer[y, x] = self._hue_transit(
                self.green_layer[y - 1, x - 1],
                self.green_layer[y, x],
                self.green_layer[y + 1, x + 1],
                self.bayer_filter[y - 1, x - 1],
                self.bayer_filter[y + 1, x + 1],
            )

    def get_hor_color(self, x: int, y: int):
        if x > 0:
            return self.colors[y, x - 1]
        return self.colors[y, x + 1]

    def _recover_red_and_blue_on_green(self, x: int, y: int):
        vertical_hue = self._hue_transit(
            self.green_layer[y - 1, x],
            self.green_layer[y, x],
            self.green_layer[y + 1, x],
            self.bayer_filter[y - 1, x],
            self.bayer_filter[y + 1, x],
        )

        horizontal_hue = self._hue_transit(
            self.green_layer[y, x - 1],
            self.green_layer[y, x],
            self.green_layer[y, x + 1],
            self.bayer_filter[y, x - 1],
            self.bayer_filter[y, x + 1]
        )

        if self.get_hor_color(x, y) == Color.RED:
            self.red_layer[y, x] = horizontal_hue
            self.blue_layer[y, x] = vertical_hue
        else:
            self.red_layer[y, x] = vertical_hue
            self.blue_layer[y, x] = horizontal_hue

    def _recover_red_and_blue(self):
        for y in tqdm(range(self.colors.shape[0])):
            for x in range(self.colors.shape[1]):
                if self.colors[y, x] == Color.RED:
                    self.red_layer[y, x] = self.bayer_filter[y, x]
                    self._recover_blue_on_red(x, y)

                if self.colors[y, x] == Color.BLUE:
                    self.blue_layer[y, x] = self.bayer_filter[y, x]
                    self._recover_red_on_blue(x, y)

                if self.colors[y, x] == Color.GREEN:
                    self._recover_red_and_blue_on_green(x, y)

    def get_delta_N(self, x: int, y: int):
        return abs(self.bayer_filter[y, x] - self.bayer_filter[y - 2, x]) * 2 + \
            abs(self.bayer_filter[y - 1, x] - self.bayer_filter[y + 1, x])

    def get_delta_E(self, x: int, y: int):
        return abs(self.bayer_filter[y, x] - self.bayer_filter[y, x + 2]) * 2 + \
            abs(self.bayer_filter[y, x - 1] - self.bayer_filter[y, x + 1])

    def get_delta_W(self, x: int, y: int):
        return abs(self.bayer_filter[y, x] - self.bayer_filter[y, x - 2]) * 2 + \
            abs(self.bayer_filter[y, x - 1] - self.bayer_filter[y, x + 1])

    def get_delta_S(self, x: int, y: int):
        return abs(self.bayer_filter[y, x] - self.bayer_filter[y + 2, x]) * 2 + \
            abs(self.bayer_filter[y - 1, x] - self.bayer_filter[y + 1, x])

    def _flatten_bayer(self, bayer_np_3d: np.ndarray) -> np.ndarray:
        bayer_flattened = []
        for row in bayer_np_3d:
            bayer_flattened.append([])
            for pix in row:
                bayer_flattened[-1].append(pix[0] or pix[1] or pix[2])
        return np.array(bayer_flattened)
