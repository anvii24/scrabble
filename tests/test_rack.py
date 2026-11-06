"""Step 2 (board and tiles): planned tests for the Rack class."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_init_copies_list():
    """Mutating the list passed to Rack afterwards does not change the rack."""


@pytest.mark.skip(reason="TODO")
def test_add_appends_tiles():
    """add puts the tiles on the rack."""


@pytest.mark.skip(reason="TODO")
def test_remove_takes_one_copy():
    """With two A tiles, removing one A leaves one."""


@pytest.mark.skip(reason="TODO")
def test_remove_assigned_blank_matches_question_mark():
    """Removing Tile('E', 0, True) removes a '?' tile."""


@pytest.mark.skip(reason="TODO")
def test_remove_missing_raises_and_keeps_rack():
    """Removing an unheld tile raises ValueError and leaves the whole rack unchanged."""


@pytest.mark.skip(reason="TODO")
def test_refill_tops_up_to_rack_size():
    """A rack of 3 refills to 7 and the bag falls by 4."""


@pytest.mark.skip(reason="TODO")
def test_refill_with_short_bag():
    """Refill takes what is left when the bag runs out."""


@pytest.mark.skip(reason="TODO")
def test_refill_full_rack_is_noop():
    """A full rack draws nothing."""


@pytest.mark.skip(reason="TODO")
def test_letters_shows_blank_as_question_mark():
    """letters() gives the rack as a string with '?' for blanks."""


@pytest.mark.skip(reason="TODO")
def test_value_sums_points():
    """value() sums tile points, blanks counting 0."""
