
from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import Move, Placement, Tile
from scrabble.constants import CENTER
from scrabble.constants import CENTER, SIZE

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon


def words_formed(
    board: Board, placements: list[Placement]
) -> list[list[tuple[int, int, Tile]]]:

    if not placements:
        return []

    new_tiles = {}

    for p in placements:
        new_tiles[(p.row, p.col)] = p.tile

    def get_tile(r, c):
        if (r, c) in new_tiles:
            return new_tiles[(r, c)]

        return board.get(r, c)

    def get_word(r, c, dr, dc):

        while 0 <= r - dr < SIZE and 0 <= c - dc < SIZE:
            if get_tile(r - dr, c - dc) is None:
                break

            r -= dr
            c -= dc

        word = []

        while 0 <= r < SIZE and 0 <= c < SIZE:
            tile = get_tile(r, c)

            if tile is None:
                break

            word.append((r, c, tile))

            r += dr
            c += dc

        return word

    first = placements[0]

    same_row = all(p.row == first.row for p in placements)

    words = []

    if same_row:
        main_word = get_word(first.row, first.col, 0, 1)
        other_direction = (1, 0)
    else:
        main_word = get_word(first.row, first.col, 1, 0)
        other_direction = (0, 1)

    if len(main_word) > 1:
        words.append(main_word)

    for p in placements:
        cross_word = get_word(
            p.row, p.col,
            other_direction[0],
            other_direction[1]
        )

        if len(cross_word) > 1:
            words.append(cross_word)

    return words


def validate(board: Board, move: Move, lexicon: Lexicon) -> tuple[bool, str]:

    # Pass and exchange moves are valid
    if move.kind in ("pass", "exchange"):
        return True, "Valid move"

    if move.kind != "play":
        return False, "Invalid move type"

    placements = move.placements

    if not placements:
        return False, "No tiles placed"

    # Check that all positions are inside the board
    for p in placements:
        if not board.in_bounds(p.row, p.col):
            return False, "Tile is outside the board"

    # Check for duplicate or already occupied positions
    positions = set()

    for p in placements:
        position = (p.row, p.col)

        if position in positions:
            return False, "Duplicate placement"

        positions.add(position)

        if not board.is_empty_square(p.row, p.col):
            return False, "Square is already occupied"

    # Check that all tiles are in the same row or column
    same_row = all(p.row == placements[0].row for p in placements)
    same_col = all(p.col == placements[0].col for p in placements)

    if not same_row and not same_col:
        return False, "Tiles must be placed in one line"

    # Create a temporary board to check gaps and connections
    new_board = board.copy()

    for p in placements:
        new_board.place([p])

    # Check whether there are gaps between the placed tiles
    if same_row:
        row = placements[0].row
        start = min(p.col for p in placements)
        end = max(p.col for p in placements)

        for c in range(start, end + 1):
            if new_board.get(row, c) is None:
                return False, "There is a gap between tiles"

    else:
        col = placements[0].col
        start = min(p.row for p in placements)
        end = max(p.row for p in placements)

        for r in range(start, end + 1):
            if new_board.get(r, col) is None:
                return False, "There is a gap between tiles"

    # First move must cover the centre square
    if board.is_empty():
        if len(placements) < 2:
            return False, "First move must form a word"

        if CENTER not in positions:
            return False, "First move must cover the centre square"

    else:
        # At least one new tile must touch an existing tile
        connected = False

        for p in placements:
            neighbours = [
                (p.row - 1, p.col),
                (p.row + 1, p.col),
                (p.row, p.col - 1),
                (p.row, p.col + 1)
            ]

            for r, c in neighbours:
                if board.in_bounds(r, c) and board.get(r, c) is not None:
                    connected = True

        if not connected:
            return False, "Move is not connected to existing tiles"

    # Find all words created by this move
    words = words_formed(board, placements)

    if not words:
        return False, "Move does not form a word"

    # Check every word against the lexicon
    for word in words:
        word_string = "".join(tile.letter for r, c, tile in word)

        if not lexicon.is_word(word_string):
            return False, f"Invalid word: {word_string}"

    return True, "Valid move"
