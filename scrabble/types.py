"""Step 1 (foundations): shared data types used by every other module.

This module and constants.py are the only ones the rest of the code imports at
module top level, which is what keeps the package free of circular imports.

Blank convention, used everywhere:
    on a rack or in the bag  Tile("?", 0, is_blank=True)
    on the board             Tile("E", 0, is_blank=True)  (letter = assigned letter)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrabble.bag import TileBag
    from scrabble.board import Board
    from scrabble.rack import Rack


@dataclass(frozen=True)
class Tile:
    """A single tile. Frozen, so tiles can be compared and hashed."""

    letter: str
    points: int
    is_blank: bool = False


@dataclass(frozen=True)
class Placement:
    """A tile put on square (row, col), both 0-indexed."""

    row: int
    col: int
    tile: Tile


@dataclass
class Move:
    """One turn. `kind` is 'play', 'exchange' or 'pass'."""

    kind: str
    placements: list[Placement] = field(default_factory=list)
    exchanged: list[Tile] = field(default_factory=list)
    score: int = 0
    words: list[str] = field(default_factory=list)


@dataclass
class GameState:
    """Everything needed to continue a game.

    `turn` counts turns taken, so the player to move is turn % len(racks).
    `passes` counts consecutive scoreless turns.
    """

    board: Board
    bag: TileBag
    racks: list[Rack]
    scores: list[int]
    turn: int = 0
    passes: int = 0


class Player:
    """Base class for anything that can take a turn."""

    name: str

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        """Return the Move this player makes with `rack` in position `state`."""
        raise NotImplementedError
