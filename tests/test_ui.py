"""Step 6 (game loop and UI): planned tests for the text interface."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_show_hides_opponent_rack():
    """capsys output has this player's rack and not the opponent's."""


@pytest.mark.skip(reason="TODO")
def test_parse_across():
    """'H8 across CAT' gives placements on (7,7), (7,8), (7,9)."""


@pytest.mark.skip(reason="TODO")
def test_parse_down():
    """'H8 down CAT' gives placements on (7,7), (8,7), (9,7)."""


@pytest.mark.skip(reason="TODO")
def test_parse_coordinates():
    """A1 is (0, 0) and O15 is (14, 14); h8 works like H8."""


@pytest.mark.skip(reason="TODO")
def test_parse_lowercase_is_blank():
    """A lowercase letter gives Tile(letter, 0, True) from a '?'."""


@pytest.mark.skip(reason="TODO")
def test_parse_skips_tiles_on_board():
    """Letters over matching board tiles produce no placement."""


@pytest.mark.skip(reason="TODO")
def test_parse_conflicting_board_tile_raises():
    """A letter differing from the board tile raises ValueError."""


@pytest.mark.skip(reason="TODO")
def test_parse_exchange():
    """'exchange AEI' gives an exchange of those tiles, with ? for a blank."""


@pytest.mark.skip(reason="TODO")
def test_parse_pass():
    """'pass' gives a pass move, ignoring case."""


@pytest.mark.skip(reason="TODO")
def test_parse_tiles_not_held_raises():
    """Letters the rack lacks raise ValueError, counting duplicates."""


@pytest.mark.skip(reason="TODO")
def test_parse_malformed_raises():
    """Garbage, bad coordinates and off-board words raise ValueError."""


@pytest.mark.skip(reason="TODO")
def test_human_reprompts_after_bad_input():
    """With monkeypatched input, bad then good input returns the good move."""


@pytest.mark.skip(reason="TODO")
def test_human_fills_in_score_and_words():
    """The returned play has score and words set."""
