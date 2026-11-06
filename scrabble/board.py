"""Step 2 (board and tiles): the 15x15 grid of placed tiles."""

from __future__ import annotations

from scrabble.types import Placement, Tile


class Board:
    """A SIZE x SIZE grid; each square is a Tile or None.

    Attributes:
        grid: list of SIZE rows, each a list of SIZE `Tile | None`, indexed
            grid[row][col] from 0. (7, 7) is the centre.
    """

    def __init__(self) -> None:
        """Create an empty board.

        Outputs:
            A board whose `grid` has SIZE independent rows of None. Rows must
            not be aliases of one list (avoid `[[None] * SIZE] * SIZE`).
        """
        raise NotImplementedError

    def get(self, r: int, c: int) -> Tile | None:
        """Return the tile on (r, c), or None if the square is empty.

        Inputs:
            r, c: 0-indexed row and column.
        Outputs:
            The Tile, or None.
        Edge cases:
            Off-board coordinates return None rather than raising, and must not
            wrap around through Python's negative indexing. This lets word
            scanning walk off the edge of the board safely.
        """
        raise NotImplementedError

    def place(self, placements: list[Placement]) -> None:
        """Put tiles on the board, mutating it.

        Inputs:
            placements: the tiles to put down. Blanks carry their assigned
                letter (see the blank convention in types.py).
        Rules:
            No word or lexicon checks are done here; that is rules.validate.
        Edge cases:
            Raises ValueError if any square is off the board or occupied, and
            changes nothing in that case. An empty list is a no-op.
        """
        raise NotImplementedError

    def is_empty_square(self, r: int, c: int) -> bool:
        """Return True if (r, c) is on the board and has no tile.

        Edge cases:
            Off-board coordinates return False: you cannot place a tile there.
        """
        raise NotImplementedError

    def in_bounds(self, r: int, c: int) -> bool:
        """Return True if 0 <= r < SIZE and 0 <= c < SIZE."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True if no tile has been placed (the first move is pending)."""
        raise NotImplementedError

    def copy(self) -> Board:
        """Return an independent copy.

        Outputs:
            A new Board with its own rows; placing on the copy must not affect
            the original. Tiles are frozen, so they can be shared.
        """
        raise NotImplementedError

    def transpose(self) -> Board:
        """Return a new board with rows and columns swapped.

        Outputs:
            A new Board where new.get(c, r) == self.get(r, c). `self` is
            unchanged. Applying transpose twice gives an equal board.
        Rules:
            movegen uses this to treat down plays as across plays. The premium
            layout is symmetric, so premiums need no adjustment.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Return a printable grid with labels.

        Outputs:
            A multi-line string with column labels A-O across the top and row
            labels 1-15 down the side, matching ui.parse_move, so "H8" is the
            centre square (row 7, col 7).
        Rules:
            Occupied squares show their letter, with blanks in lowercase.
            Empty premium squares show TW/DW/TL/DL from constants.PREMIUM.
            Other empty squares show a dot. All cells have equal width.
        """
        raise NotImplementedError
