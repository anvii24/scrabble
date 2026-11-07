from __future__ import annotations

import pytest

import main
from scrabble.evaluation import WeightedPlayer
from scrabble.lexicon import Lexicon
from scrabble.players import GreedyPlayer


@pytest.fixture(scope="module")
def lexicon() -> Lexicon:
    lex = Lexicon()
    lex.load("data/enable1.txt")
    return lex


def test_choose_greedy(monkeypatch, lexicon):
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")
    player = main.choose_opponent(lexicon)
    assert isinstance(player, GreedyPlayer)


def test_choose_weights_file(monkeypatch, tmp_path, lexicon):
    weights_file = tmp_path / "weights.txt"
    weights_file.write_text("1.0, 2.0, -1.0, -3.0, 0.5, 4.0")

    inputs = iter(["2", str(weights_file)])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = main.choose_opponent(lexicon)
    assert isinstance(player, WeightedPlayer)
    assert player.weights == [1.0, 2.0, -1.0, -3.0, 0.5, 4.0]


def test_choose_weights_blank_uses_default(monkeypatch, lexicon):
    inputs = iter(["2", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = main.choose_opponent(lexicon)
    assert isinstance(player, WeightedPlayer)
    assert player.weights == main.DEFAULT_WEIGHTS


def test_choose_weights_missing_file_falls_back(monkeypatch, lexicon):
    inputs = iter(["2", "/no/such/file.txt"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = main.choose_opponent(lexicon)
    assert isinstance(player, WeightedPlayer)
    assert player.weights == main.DEFAULT_WEIGHTS


def test_bad_choice_reprompts(monkeypatch, lexicon):
    inputs = iter(["nonsense", "7", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    player = main.choose_opponent(lexicon)
    assert isinstance(player, GreedyPlayer)


def test_missing_word_list_exits_cleanly(monkeypatch):
    monkeypatch.setattr(main, "WORD_LIST_PATH", main.WORD_LIST_PATH.parent / "does_not_exist.txt")
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.value.code != 0
