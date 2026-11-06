from __future__ import annotations

from scrabble.types import Placement, Tile


class Board:
    def __init__(self) -> None:
        raise NotImplementedError

    def get(self, r: int, c: int) -> Tile | None:
        raise NotImplementedError

    def place(self, placements: list[Placement]) -> None:
        raise NotImplementedError

    def is_empty_square(self, r: int, c: int) -> bool:
        raise NotImplementedError

    def in_bounds(self, r: int, c: int) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def copy(self) -> Board:
        raise NotImplementedError

    def transpose(self) -> Board:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
