
from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Tile
from scrabble.constants import RACK_SIZE

if TYPE_CHECKING:
    from scrabble.bag import TileBag


class Rack:
    def __init__(self, tiles: list[Tile] | None = None) -> None:
        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles.copy()

    def add(self, tiles: list[Tile]) -> None:
        self.tiles.extend(tiles)

    def remove(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            if tile not in self.tiles:
                raise ValueError("Tile is not present in the rack")

        for tile in tiles:
            self.tiles.remove(tile)

    def refill(self, bag: TileBag) -> None:
        needed = RACK_SIZE - len(self.tiles)

        if needed > 0:
            new_tiles = bag.draw(needed)
            self.add(new_tiles)

    def letters(self) -> str:
        return "".join(tile.letter for tile in self.tiles)

    def value(self) -> int:
        total = 0

        for tile in self.tiles:
            total += tile.points

        return total
