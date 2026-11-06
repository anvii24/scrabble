"""Step 2 (board and tiles): the seeded bag of undrawn tiles."""

from __future__ import annotations

from scrabble.types import Tile


class TileBag:
    """The tiles not yet drawn, shuffled by a private random.Random(seed).

    All randomness must come from this one Random instance (never the global
    `random` module) so a game is fully reproducible from its seed.
    """

    def __init__(self, seed: int) -> None:
        """Fill the bag with the full tile set and shuffle it.

        Inputs:
            seed: seed for the bag's random.Random.
        Outputs:
            A bag of 100 tiles built from LETTER_COUNTS and LETTER_POINTS, with
            blanks as Tile("?", 0, is_blank=True).
        """
        raise NotImplementedError

    def draw(self, n: int) -> list[Tile]:
        """Remove and return up to `n` tiles.

        Inputs:
            n: how many tiles to draw.
        Outputs:
            A list of min(n, remaining()) tiles.
        Edge cases:
            Drawing from a short or empty bag returns what is left, possibly
            []. Raises ValueError if n is negative.
        """
        raise NotImplementedError

    def exchange(self, tiles: list[Tile]) -> list[Tile]:
        """Swap `tiles` for the same number of new tiles.

        Inputs:
            tiles: the tiles handed back, in rack form.
        Outputs:
            len(tiles) freshly drawn tiles.
        Rules:
            Draw first, then return `tiles` to the bag and reshuffle, so a
            player cannot redraw a tile they just gave back. remaining() is
            unchanged overall.
        Edge cases:
            Raises ValueError if fewer than len(tiles) tiles remain, leaving the
            bag unchanged. The game-level rule that exchanges need at least
            RACK_SIZE tiles in the bag is enforced by game.apply_move.
        """
        raise NotImplementedError

    def remaining(self) -> int:
        """Return how many tiles are left in the bag."""
        raise NotImplementedError
