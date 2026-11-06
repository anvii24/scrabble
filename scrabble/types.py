from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrabble.bag import TileBag
    from scrabble.board import Board
    from scrabble.rack import Rack


@dataclass(frozen=True)
class Tile:
    letter: str
    points: int
    is_blank: bool = False


@dataclass(frozen=True)
class Placement:
    row: int
    col: int
    tile: Tile


@dataclass
class Move:
    kind: str
    placements: list[Placement] = field(default_factory=list)
    exchanged: list[Tile] = field(default_factory=list)
    score: int = 0
    words: list[str] = field(default_factory=list)


@dataclass
class GameState:
    board: Board
    bag: TileBag
    racks: list[Rack]
    scores: list[int]
    turn: int = 0
    passes: int = 0


class Player:
    name: str

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        raise NotImplementedError
