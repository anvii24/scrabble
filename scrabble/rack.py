from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Tile

if TYPE_CHECKING:
    from scrabble.bag import TileBag


class Rack:
    def __init__(self, tiles: list[Tile] | None = None) -> None:
        raise NotImplementedError

    def add(self, tiles: list[Tile]) -> None:
        raise NotImplementedError

    def remove(self, tiles: list[Tile]) -> None:
        raise NotImplementedError

    def refill(self, bag: TileBag) -> None:
        raise NotImplementedError

    def letters(self) -> str:
        raise NotImplementedError

    def value(self) -> int:
        raise NotImplementedError
