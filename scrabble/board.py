
from __future__ import annotations

from scrabble.types import Placement, Tile
from scrabble.constants import SIZE, PREMIUM


class Board:
    def __init__(self) -> None:
        self.grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    def get(self, r: int, c: int) -> Tile | None:
        if not self.in_bounds(r, c):
            return None
        return self.grid[r][c]

    def place(self, placements: list[Placement]) -> None:
        for p in placements:
            if not self.in_bounds(p.row, p.col):
                raise ValueError("Position is outside the board")

            if not self.is_empty_square(p.row, p.col):
                raise ValueError("Square is already occupied")

            self.grid[p.row][p.col] = p.tile

    def is_empty_square(self, r: int, c: int) -> bool:
        if not self.in_bounds(r, c):
            return False
        return self.grid[r][c] is None

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < SIZE and 0 <= c < SIZE

    def is_empty(self) -> bool:
        for row in self.grid:
            for tile in row:
                if tile is not None:
                    return False
        return True

    def copy(self) -> Board:
        new_board = Board()

        for r in range(SIZE):
            for c in range(SIZE):
                new_board.grid[r][c] = self.grid[r][c]

        return new_board

    def transpose(self) -> Board:
        new_board = Board()

        for r in range(SIZE):
            for c in range(SIZE):
                new_board.grid[c][r] = self.grid[r][c]

        return new_board

    def __str__(self) -> str:
        result = "    "

        for c in range(SIZE):
            result += f"{c:>3}"

        result += "\n"

        for r in range(SIZE):
            result += f"{r:>3} "

            for c in range(SIZE):
                tile = self.grid[r][c]

                if tile is not None:
                    cell = tile.letter
                else:
                    cell = PREMIUM.get((r, c), ".")

                result += f"{cell:>3}"

            result += "\n"

        return result
