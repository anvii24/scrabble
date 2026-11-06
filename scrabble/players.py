from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


class GreedyPlayer(Player):
    def __init__(self, lexicon: Lexicon, name: str = "Greedy") -> None:
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, lexicon: Lexicon, seed: int = 0, name: str = "Random") -> None:
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        raise NotImplementedError
