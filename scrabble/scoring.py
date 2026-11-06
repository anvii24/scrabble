
from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move
from scrabble.constants import PREMIUM, BINGO
from scrabble.rules import words_formed

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.rack import Rack


def score_move(board: Board, move: Move) -> int:
    if move.kind != "play":
        return 0

    words = words_formed(board, move.placements)

    total_score = 0
    new_positions = set()

    for p in move.placements:
        new_positions.add((p.row, p.col))

    for word in words:
        word_score = 0
        word_multiplier = 1

        for r, c, tile in word:
            letter_multiplier = 1

            if (r, c) in new_positions:
                premium = PREMIUM.get((r, c))

                if premium == "DL":
                    letter_multiplier = 2
                elif premium == "TL":
                    letter_multiplier = 3
                elif premium == "DW":
                    word_multiplier *= 2
                elif premium == "TW":
                    word_multiplier *= 3

            word_score += tile.points * letter_multiplier

        total_score += word_score * word_multiplier

    if len(move.placements) == 7:
        total_score += BINGO

    return total_score


def end_game_adjust(
    scores: list[int], racks: list[Rack], who_went_out: int | None
) -> list[int]:
    final_scores = scores.copy()

    rack_values = []

    for rack in racks:
        rack_values.append(rack.value())

    for i in range(len(final_scores)):
        final_scores[i] -= rack_values[i]

    if who_went_out is not None:
        opponents_points = 0

        for i in range(len(rack_values)):
            if i != who_went_out:
                opponents_points += rack_values[i]

        final_scores[who_went_out] += opponents_points

    return final_scores
