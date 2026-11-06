"""Step 2 (board and tiles): planned tests for the Board class."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_new_board_is_empty():
    """A new board has every square None and is_empty() is True."""


@pytest.mark.skip(reason="TODO")
def test_rows_are_independent():
    """Placing on one row leaves the other rows untouched."""


@pytest.mark.skip(reason="TODO")
def test_get_off_board_returns_none():
    """get(-1, 0) and get(15, 0) return None, with no negative-index wraparound."""


@pytest.mark.skip(reason="TODO")
def test_place_puts_tiles_on_squares():
    """After place, get returns each tile and is_empty() is False."""


@pytest.mark.skip(reason="TODO")
def test_place_on_occupied_square_raises():
    """Placing on an occupied square raises ValueError and changes nothing."""


@pytest.mark.skip(reason="TODO")
def test_place_off_board_raises():
    """Placing off the board raises ValueError and changes nothing."""


@pytest.mark.skip(reason="TODO")
def test_is_empty_square_false_off_board():
    """is_empty_square is False for off-board and occupied squares."""


@pytest.mark.skip(reason="TODO")
def test_in_bounds_edges():
    """in_bounds is True at 0 and 14, and False at -1 and 15."""


@pytest.mark.skip(reason="TODO")
def test_copy_is_independent():
    """Placing on a copy does not affect the original."""


@pytest.mark.skip(reason="TODO")
def test_transpose_swaps_rows_and_columns():
    """A tile at (r, c) appears at (c, r), and the original is unchanged."""


@pytest.mark.skip(reason="TODO")
def test_transpose_twice_is_identity():
    """Transposing twice gives an equal board."""


@pytest.mark.skip(reason="TODO")
def test_str_shows_labels_premiums_and_tiles():
    """str() has A-O and 1-15 labels, premiums on empty squares, letters on tiles, lowercase blanks."""
