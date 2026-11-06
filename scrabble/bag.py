
from __future__ import annotations

import random

from scrabble.types import Tile
from scrabble.constants import LETTER_COUNTS, LETTER_POINTS


class TileBag:
    def __init__(self, seed: int) -> None:
        self.random = random.Random(seed)
        self.tiles = []

        for letter, count in LETTER_COUNTS.items():
            for _ in range(count):
                tile = Tile(
                    letter=letter,
                    points=LETTER_POINTS[letter],
                    is_blank=(letter == "?")
                )
                self.tiles.append(tile)

        self.random.shuffle(self.tiles)

    def draw(self, n: int) -> list[Tile]:
        drawn_tiles = self.tiles[:n]
        self.tiles = self.tiles[n:]
        return drawn_tiles

    def exchange(self, tiles: list[Tile]) -> list[Tile]:
        if len(self.tiles) < len(tiles):
            raise ValueError("Not enough tiles in the bag to exchange")

        new_tiles = self.draw(len(tiles))
        self.tiles.extend(tiles)
        self.random.shuffle(self.tiles)

        return new_tiles

    def remaining(self) -> int:
        return len(self.tiles)