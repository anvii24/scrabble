"""Step 2 (board and tiles): a player's rack of up to seven tiles."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Tile

if TYPE_CHECKING:
    from scrabble.bag import TileBag


class Rack:
    """The tiles a player holds.

    Attributes:
        tiles: the held tiles, in rack form (blanks are Tile("?", 0, True)).
    """

    def __init__(self, tiles: list[Tile] | None = None) -> None:
        """Create a rack.

        Inputs:
            tiles: starting tiles, copied into a new list; None means empty.
        """
        raise NotImplementedError

    def add(self, tiles: list[Tile]) -> None:
        """Append `tiles` to the rack.

        Edge cases:
            Does not enforce RACK_SIZE; refill is what keeps the rack at size.
        """
        raise NotImplementedError

    def remove(self, tiles: list[Tile]) -> None:
        """Remove one rack tile for each tile in `tiles`.

        Inputs:
            tiles: the tiles to remove. Duplicates remove that many copies.
        Rules:
            A tile with is_blank=True matches a "?" tile whatever letter it was
            assigned, so placed tiles can be passed directly.
        Edge cases:
            Raises ValueError if a tile is not held, leaving the rack unchanged.
        """
        raise NotImplementedError

    def refill(self, bag: TileBag) -> None:
        """Draw from `bag` until the rack holds RACK_SIZE tiles or the bag is empty.

        Edge cases:
            Does nothing if the rack is already full.
        """
        raise NotImplementedError

    def letters(self) -> str:
        """Return the rack letters as a string in rack order, e.g. "AEI?RST"."""
        raise NotImplementedError

    def value(self) -> int:
        """Return the sum of tile points, used for end-game adjustment."""
        raise NotImplementedError
