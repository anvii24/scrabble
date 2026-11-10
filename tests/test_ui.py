from __future__ import annotations

import io

import pytest

from scrabble.board import Board
from scrabble.game import new_game
from scrabble.lexicon import Lexicon
from scrabble.rack import Rack
from scrabble.rules import validate
from scrabble.types import Move, Placement, Tile
from scrabble.ui import HumanPlayer, parse_move, show


@pytest.fixture(scope="module")
def lexicon() -> Lexicon:
    lex = Lexicon()
    lex.load("data/enable1.txt")
    return lex


def _rack(letters: str, blanks: int = 0) -> Rack:
    tiles = [Tile(letter, 1, False) for letter in letters]
    tiles += [Tile("?", 0, True) for _ in range(blanks)]
    return Rack(tiles)


def test_show_hides_opponent_rack(capsys):
    state = new_game(seed=0, n_players=2)
    show(state, 0)
    captured = capsys.readouterr().out

    assert "Player 0's rack" in captured
    assert "Player 1's rack" not in captured


def test_parse_across():
    board = Board()
    rack = _rack("QUIZAE")
    move = parse_move("H8 across QUIZ", board, rack)
    assert move.kind == "play"
    cols = [p.col for p in move.placements]
    rows = {p.row for p in move.placements}
    assert rows == {7}
    assert cols == [7, 8, 9, 10]
    assert [p.tile.letter for p in move.placements] == list("QUIZ")


def test_parse_down():
    board = Board()
    rack = _rack("QUIZAE")
    move = parse_move("H8 down QUIZ", board, rack)
    assert move.kind == "play"
    rows = [p.row for p in move.placements]
    cols = {p.col for p in move.placements}
    assert cols == {7}
    assert rows == [7, 8, 9, 10]


def test_parse_coordinates():
    board = Board()
    rack = _rack("A")
    move = parse_move("A1 across A", board, rack)
    assert move.placements[0].row == 0
    assert move.placements[0].col == 0

    move2 = parse_move("O15 down A", board, rack)
    assert move2.placements[0].row == 14
    assert move2.placements[0].col == 14


def test_parse_lowercase_is_blank():
    board = Board()
    rack = _rack("QUI", blanks=1)
    move = parse_move("H8 across QUIz", board, rack)
    last = move.placements[-1]
    assert last.tile.is_blank is True
    assert last.tile.letter == "Z"


def test_parse_skips_tiles_on_board():
    board = Board()
    board.place([Placement(7, 7, Tile("Q", 10, False))])
    rack = _rack("UIZ")
    move = parse_move("H8 across QUIZ", board, rack)
    # The Q square already holds a Q, so no placement should be generated
    # for it, and no Q tile should have been required from the rack.
    assert (7, 7) not in {(p.row, p.col) for p in move.placements}
    assert len(move.placements) == 3


def test_parse_conflicting_board_tile_raises():
    board = Board()
    board.place([Placement(7, 7, Tile("X", 8, False))])
    rack = _rack("UIZ")
    with pytest.raises(ValueError):
        parse_move("H8 across QUIZ", board, rack)


def test_parse_exchange():
    board = Board()
    rack = _rack("AEIOU")
    move = parse_move("exchange AEI", board, rack)
    assert move.kind == "exchange"
    assert sorted(t.letter for t in move.exchanged) == ["A", "E", "I"]


def test_parse_pass():
    board = Board()
    rack = _rack("AEIOU")
    move = parse_move("pass", board, rack)
    assert move.kind == "pass"
    assert move.placements == []
    assert move.exchanged == []


def test_parse_tiles_not_held_raises():
    board = Board()
    rack = _rack("AEI")
    with pytest.raises(ValueError):
        parse_move("H8 across QUIZ", board, rack)
    with pytest.raises(ValueError):
        parse_move("exchange Z", board, rack)


def test_parse_malformed_raises():
    board = Board()
    rack = _rack("AEI")
    with pytest.raises(ValueError):
        parse_move("", board, rack)
    with pytest.raises(ValueError):
        parse_move("H8 sideways WORD", board, rack)
    with pytest.raises(ValueError):
        parse_move("ZZ99 across WORD", board, rack)
    with pytest.raises(ValueError):
        parse_move("notacommand", board, rack)


def test_human_reprompts_after_bad_input(monkeypatch, capsys, lexicon):
    state = new_game(seed=0, n_players=2)
    rack = state.racks[0]
    rack.tiles = _rack("AEI").tiles
    inputs = iter(["gibberish nonsense", "pass"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = HumanPlayer(lexicon, "Tester")
    move = player.choose_move(state, rack)

    assert move.kind == "pass"
    captured = capsys.readouterr().out
    assert "Could not understand" in captured


def test_human_fills_in_score_and_words(monkeypatch, lexicon):
    state = new_game(seed=0, n_players=2)
    rack = state.racks[0]
    rack.tiles = _rack("CAT", blanks=0).tiles
    inputs = iter(["H8 across CAT"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = HumanPlayer(lexicon, "Tester")
    move = player.choose_move(state, rack)

    assert move.kind == "play"
    assert move.score > 0
    assert move.words == ["CAT"]

    ok, _ = validate(state.board, move, lexicon)
    assert ok
