from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.movegen import generate_moves
from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


class GreedyPlayer(Player):
    def __init__(self, lexicon: Lexicon, name: str = "Greedy") -> None:
        self.lexicon = lexicon
        self.name = name

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        moves = generate_moves(state.board, rack, self.lexicon)

        if moves:
            return max(moves, key=lambda move: move.score)

        if state.bag.remaining() >= len(rack.tiles) and rack.tiles:
            return Move("exchange", [], rack.tiles.copy(), 0, [])

        return Move("pass", [], [], 0, [])

