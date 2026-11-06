from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def show(state: GameState, player_idx: int) -> None:
    raise NotImplementedError


def parse_move(text: str, board: Board, rack: Rack) -> Move:
    raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, lexicon: Lexicon, name: str = "Human") -> None:
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        raise NotImplementedError
