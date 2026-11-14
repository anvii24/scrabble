from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.constants import PREMIUM, SIZE
from scrabble.rules import validate, words_formed
from scrabble.scoring import score_move
from scrabble.types import GameState, Move, Placement, Player, Tile

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack

ROW_LETTERS = "ABCDEFGHIJKLMNO"
DIRECTIONS = {"across": (0, 1), "down": (1, 0)}


def _row_label(row: int) -> str:
    return ROW_LETTERS[row]


def show(state: GameState, player_idx: int) -> None:
    lines = []

    header = "    " + "".join(f"{c + 1:>3}" for c in range(SIZE))
    lines.append(header)

    for r in range(SIZE):
        row_cells = []

        for c in range(SIZE):
            tile = state.board.get(r, c)

            if tile is not None:
                cell = tile.letter
            else:
                cell = PREMIUM.get((r, c), ".")

            row_cells.append(f"{cell:>3}")

        lines.append(f"{_row_label(r):>3} " + "".join(row_cells))

    lines.append("")
    lines.append("Scores: " + ", ".join(f"Player {i}: {s}" for i, s in enumerate(state.scores)))
    lines.append(f"Tiles left in bag: {state.bag.remaining()}")

    rack = state.racks[player_idx]
    rack_display = " ".join(("_" if t.is_blank else t.letter) for t in rack.tiles)
    lines.append(f"Player {player_idx}'s rack: {rack_display}")

    turn_note = "your turn" if state.turn == player_idx else f"player {state.turn}'s turn"
    lines.append(f"It is {turn_note}.")

    print("\n".join(lines))


def _parse_coordinate(token: str) -> tuple[int, int]:
    if len(token) < 2:
        raise ValueError(f"Malformed coordinate: {token!r}")

    row_letter = token[0].upper()
    col_part = token[1:]

    if row_letter not in ROW_LETTERS or not col_part.isdigit():
        raise ValueError(f"Malformed coordinate: {token!r}")

    row = ROW_LETTERS.index(row_letter)
    col = int(col_part) - 1

    if not (0 <= row < SIZE) or not (0 <= col < SIZE):
        raise ValueError(f"Coordinate out of bounds: {token!r}")

    return row, col


def _take_rack_tile(available: list[Tile], letter: str, want_blank: bool) -> Tile:
    if want_blank:
        match = next((t for t in available if t.is_blank), None)
    else:
        match = next((t for t in available if not t.is_blank and t.letter == letter), None)

    if match is None:
        kind = "a blank tile" if want_blank else f"tile {letter!r}"
        raise ValueError(f"Rack does not hold {kind}")

    available.remove(match)
    return match


def parse_move(text: str, board: Board, rack: Rack) -> Move:
    tokens = text.strip().split()

    if not tokens:
        raise ValueError("Empty move")

    command = tokens[0].lower()

    if command == "pass":
        if len(tokens) != 1:
            raise ValueError("'pass' takes no further arguments")
        return Move(kind="pass")

    if command == "exchange":
        if len(tokens) != 2:
            raise ValueError("Usage: exchange <letters>")

        letters = tokens[1]
        if not letters.isalpha():
            raise ValueError("Exchange letters must be alphabetic")

        available = rack.tiles.copy()
        exchanged = [
            _take_rack_tile(available, letter.upper(), want_blank=False)
            for letter in letters
        ]
        return Move(kind="exchange", exchanged=exchanged)

    if len(tokens) != 3:
        raise ValueError(
            "Usage: <coord> <across|down> <word>, 'exchange <letters>' or 'pass'"
        )

    coord_token, direction_token, word = tokens
    direction = DIRECTIONS.get(direction_token.lower())

    if direction is None:
        raise ValueError("Direction must be 'across' or 'down'")

    if not word.isalpha():
        raise ValueError("Word must contain only letters")

    start_row, start_col = _parse_coordinate(coord_token)
    dr, dc = direction

    available = rack.tiles.copy()
    placements: list[Placement] = []

    for i, char in enumerate(word):
        row, col = start_row + i * dr, start_col + i * dc

        if not board.in_bounds(row, col):
            raise ValueError("Word runs off the edge of the board")

        letter = char.upper()
        is_blank = char.islower()
        existing = board.get(row, col)

        if existing is not None:
            if existing.letter != letter:
                raise ValueError(
                    f"{coord_token} already holds {existing.letter!r}, not {letter!r}"
                )
            continue

        tile = _take_rack_tile(available, letter, is_blank)
        tile = Tile(letter, tile.points, is_blank) if is_blank else tile
        placements.append(Placement(row, col, tile))

    if not placements:
        raise ValueError("Move does not place any new tiles")

    return Move(kind="play", placements=placements, score=0, words=[])


class HumanPlayer(Player):
    def __init__(self, lexicon: Lexicon, name: str = "Human") -> None:
        self.lexicon = lexicon
        self.name = name

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        player_idx = state.racks.index(rack)
        show(state, player_idx)

        while True:
            text = input(f"{self.name}, enter your move: ")

            try:
                move = parse_move(text, state.board, rack)

                if move.kind == "play":
                    move.score = score_move(state.board, move)
                    move.words = [
                        "".join(tile.letter for _, _, tile in word)
                        for word in words_formed(state.board, move.placements)
                    ]

                ok, reason = validate(state.board, move, self.lexicon)

                if not ok:
                    print(f"Invalid move: {reason}")
                    continue

            except ValueError as exc:
                print(f"Could not understand that move: {exc}")
                continue

            return move
