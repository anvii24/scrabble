from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move, Placement, Tile

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon


def words_formed(
    board: Board, placements: list[Placement]
) -> list[list[tuple[int, int, Tile]]]:
    raise NotImplementedError


def validate(board: Board, move: Move, lexicon: Lexicon) -> tuple[bool, str]:
    raise NotImplementedError
