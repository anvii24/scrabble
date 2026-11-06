from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def features(state: GameState, move: Move, rack: Rack) -> list[float]:
    raise NotImplementedError


def evaluate(weights: list[float], feats: list[float]) -> float:
    raise NotImplementedError


class WeightedPlayer(Player):
    def __init__(
        self, weights: list[float], lexicon: Lexicon, name: str = "Weighted"
    ) -> None:
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        raise NotImplementedError
