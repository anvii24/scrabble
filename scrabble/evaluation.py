from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.constants import PREMIUM, VOWELS
from scrabble.movegen import generate_moves
from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def features(state: GameState, move: Move, rack: Rack) -> list[float]:
    score = float(move.score)

    remaining = rack.tiles.copy()
    if move.kind == "play":
        for placement in move.placements:
            for tile in remaining:
                if tile.letter == placement.tile.letter and tile.is_blank == placement.tile.is_blank:
                    remaining.remove(tile)
                    break

    letters = [tile.letter for tile in remaining if not tile.is_blank]
    vowel_count = sum(letter in VOWELS for letter in letters)

    if not letters:
        vowel_balance = 0.0
    else:
        vowel_balance = -abs(vowel_count - 2.5)

    rack_leave = sum(tile.points for tile in remaining)
    rack_leave += 4 * sum(tile.is_blank for tile in remaining)

    opened_tw = 0.0
    opened_dw = 0.0

    if move.kind == "play":
        occupied = {
            (placement.row, placement.col)
            for placement in move.placements
        }

        for row, col in occupied:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                r, c = row + dr, col + dc
                if 0 <= r < 15 and 0 <= c < 15:
                    if state.board.get(r, c) is None:
                        premium = PREMIUM.get((r, c))
                        if premium == "TW":
                            opened_tw += 1
                        elif premium == "DW":
                            opened_dw += 1

    bag_left = float(state.bag.remaining())

    return [
        score,
        -float(rack_leave),
        vowel_balance,
        -opened_tw,
        -opened_dw,
        bag_left,
    ]


def evaluate(weights: list[float], feats: list[float]) -> float:
    if len(weights) != len(feats):
        raise ValueError("Weights and features must have the same length")
    return sum(weight * feature for weight, feature in zip(weights, feats))


class WeightedPlayer(Player):
    def __init__(
        self, weights: list[float], lexicon: Lexicon, name: str = "Weighted"
    ) -> None:
        if len(weights) != 6:
            raise ValueError("Exactly six weights are required")
        self.weights = weights.copy()
        self.lexicon = lexicon
        self.name = name

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        moves = generate_moves(state.board, rack, self.lexicon)

        if moves:
            return max(
                moves,
                key=lambda move: evaluate(self.weights, features(state, move, rack)),
            )

        if state.bag.remaining() >= len(rack.tiles) and rack.tiles:
            return Move("exchange", [], rack.tiles.copy(), 0, [])

        return Move("pass", [], [], 0, [])
