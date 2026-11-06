from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.rack import Rack


def score_move(board: Board, move: Move) -> int:
    raise NotImplementedError


def end_game_adjust(
    scores: list[int], racks: list[Rack], who_went_out: int | None
) -> list[int]:
    raise NotImplementedError
