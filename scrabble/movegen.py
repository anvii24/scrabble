from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def anchors(board: Board) -> list[tuple[int, int]]:
    raise NotImplementedError


def cross_checks(board: Board, lexicon: Lexicon) -> dict[tuple[int, int], set[str]]:
    raise NotImplementedError


def generate_moves(board: Board, rack: Rack, lexicon: Lexicon) -> list[Move]:
    raise NotImplementedError


def brute_force_moves(board: Board, rack: Rack, lexicon: Lexicon) -> list[Move]:
    raise NotImplementedError
