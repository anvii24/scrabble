"""Step 3 (rules and scoring): which words a play forms and whether it is legal."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move, Placement, Tile

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon


def words_formed(
    board: Board, placements: list[Placement]
) -> list[list[tuple[int, int, Tile]]]:
    """Return every word a play would create.

    Inputs:
        board: the position BEFORE the play. It is not mutated, and the
            placements are not on it yet.
        placements: the new tiles, assumed to lie on one line.
    Outputs:
        One list per word, each a list of (row, col, tile) in reading order and
        including tiles already on the board. The main word (along the line of
        the play) comes first, followed by cross words.
    Rules:
        Only words of length >= 2 are returned. Scan outwards past both ends of
        each run so that adjacent existing tiles are included.
    Edge cases:
        A single placed tile has no line of its own: both directions are
        checked, and it may form one word, two, or none. Placements that form
        no word of length >= 2 return []. Empty placements return [].
    """
    raise NotImplementedError


def validate(board: Board, move: Move, lexicon: Lexicon) -> tuple[bool, str]:
    """Check that a move is legal on this board.

    Inputs:
        board: the position before the move.
        move: the move; only 'play' moves are checked in detail.
        lexicon: the word list.
    Outputs:
        (True, "") if legal, otherwise (False, reason) with a message suitable
        for showing to a human player.
    Rules, for a 'play':
        1. At least one placement, on distinct empty squares, on the board.
        2. All placements share a single row or a single column.
        3. No gaps: every square between the first and last placement is either
           placed or already occupied.
        4. First move: must cover CENTER and form a word of length >= 2.
        5. Later moves: connected, i.e. at least one placement is orthogonally
           adjacent to an existing tile.
        6. Every word from words_formed is in the lexicon.
    Edge cases:
        'pass' and 'exchange' return (True, ""): this function cannot see the
        bag or rack, so game.apply_move checks those. Rack ownership of played
        tiles is also not checked here. An unknown `kind` returns False.
    """
    raise NotImplementedError
