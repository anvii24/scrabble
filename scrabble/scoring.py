"""Step 3 (rules and scoring): move scores and end-of-game adjustment."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.rack import Rack


def score_move(board: Board, move: Move) -> int:
    """Return the points a play scores.

    Inputs:
        board: the position BEFORE the play (not mutated).
        move: the move. Its `score` field is ignored and not written.
    Outputs:
        The total score across every word in rules.words_formed.
    Rules:
        Letter premiums (DL, TL) multiply a tile's points, then word premiums
        (DW, TW) multiply the word total. Premiums apply only to squares
        receiving a newly placed tile; existing tiles count at face value. A
        new tile sitting on a premium applies it to BOTH words it is part of.
        Blanks score 0 but still trigger the word premium under them. Multiple
        word premiums multiply together. Placing exactly RACK_SIZE tiles adds
        BINGO once, after all words are summed.
    Edge cases:
        'pass' and 'exchange' moves score 0.
    """
    raise NotImplementedError


def end_game_adjust(
    scores: list[int], racks: list[Rack], who_went_out: int | None
) -> list[int]:
    """Return final scores after unplayed tiles are counted.

    Inputs:
        scores: scores before adjustment (not mutated).
        racks: each player's final rack, same order as `scores`.
        who_went_out: index of the player who emptied their rack, or None if
            the game ended on consecutive scoreless turns.
    Outputs:
        A new list of adjusted scores.
    Rules:
        Each player loses their own rack.value(). If someone went out, they
        also gain the sum of everyone else's rack values.
    Edge cases:
        The player who went out has an empty rack, so loses 0. Scores may go
        negative. With who_went_out=None nobody gains anything.
    """
    raise NotImplementedError
