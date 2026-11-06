from __future__ import annotations

from scrabble.types import Tile


class TileBag:
    def __init__(self, seed: int) -> None:
        raise NotImplementedError

    def draw(self, n: int) -> list[Tile]:
        raise NotImplementedError

    def exchange(self, tiles: list[Tile]) -> list[Tile]:
        raise NotImplementedError

    def remaining(self) -> int:
        raise NotImplementedError
