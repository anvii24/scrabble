"""Step 4 (lexicon and move generation): Appel & Jacobson legal-move generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def anchors(board: Board) -> list[tuple[int, int]]:
    """Return the squares a new word must touch.

    Inputs:
        board: the current position.
    Outputs:
        Empty squares orthogonally adjacent to a tile, sorted by (row, col).
    Edge cases:
        An empty board returns [CENTER]. A full board returns [].
    """
    raise NotImplementedError


def cross_checks(board: Board, lexicon: Lexicon) -> dict[tuple[int, int], set[str]]:
    """Return which letters are allowed on squares with a vertical neighbour.

    Written for across plays; call it on board.transpose() for down plays.

    Inputs:
        board: the current position.
        lexicon: the word list.
    Outputs:
        A dict mapping each empty square with a tile directly above or below it
        to the set of uppercase letters that complete a valid vertical word.
    Rules:
        A square with no key is unconstrained: any letter fits. A key with an
        empty set means nothing fits, which is different from no key.
    Edge cases:
        An empty board returns {}.
    """
    raise NotImplementedError


def generate_moves(board: Board, rack: Rack, lexicon: Lexicon) -> list[Move]:
    """Return every legal play using the Appel & Jacobson algorithm.

    Inputs:
        board: the current position (not mutated).
        rack: the player's rack (not mutated).
        lexicon: the word list.
    Outputs:
        A list of 'play' Moves with `placements`, `score` and `words` filled in.
        Only plays are returned; exchange and pass are the player's decision.
    Rules:
        For each anchor, build a left part by DFS over the trie, then extend
        right, using existing tiles and rack tiles that pass cross_checks. A
        move is recorded when the node is a word end, the word covers the
        anchor, and the next square is empty or off the board. Left parts are
        limited by the empty non-anchor squares to the left of the anchor, so
        no move is found twice from different anchors.
        Across plays come from the board itself; down plays come from running
        the same search on board.transpose() and swapping row and col back.
        A blank may stand for any letter; it yields Tile(letter, 0, True) and
        is a separate move from playing the real letter. Score every move with
        scoring.score_move on the ORIGINAL board, not the transposed one.
    Edge cases:
        A one-tile play is found in both directions and must appear only once.
        Dedupe on the set of placements.
        The output order must be deterministic: sort it, and never iterate over
        a set of letters unsorted, because string hashing differs between
        Python runs and the max() in players would then break ties differently,
        making optimise.fitness non-deterministic.
        An empty rack or no legal play returns [].
    """
    raise NotImplementedError


def brute_force_moves(board: Board, rack: Rack, lexicon: Lexicon) -> list[Move]:
    """Return every legal play by exhaustive search, as a test reference.

    Inputs and outputs are the same as generate_moves.

    Rules:
        Try every start square, direction and ordered arrangement of rack tiles
        (with every letter for each blank), keeping those rules.validate
        accepts. Shares no logic with generate_moves apart from validate and
        score_move, so that the two can check each other.
    Edge cases:
        Far too slow for real games; intended for small racks and small
        lexicons. tests/test_movegen.py compares its output with generate_moves
        as sets of placements.
    """
    raise NotImplementedError
