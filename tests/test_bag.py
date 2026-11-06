"""Step 2 (board and tiles): planned tests for the TileBag class."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_new_bag_has_100_tiles():
    """remaining() is 100 and the tile multiset matches LETTER_COUNTS."""


@pytest.mark.skip(reason="TODO")
def test_same_seed_same_order():
    """Two bags with one seed draw identical sequences."""


@pytest.mark.skip(reason="TODO")
def test_different_seed_different_order():
    """Two bags with different seeds draw different sequences."""


@pytest.mark.skip(reason="TODO")
def test_seed_ignores_global_random():
    """Calling random.seed or random.random between draws does not change them."""


@pytest.mark.skip(reason="TODO")
def test_draw_reduces_remaining():
    """draw(7) returns 7 tiles and leaves 93."""


@pytest.mark.skip(reason="TODO")
def test_draw_more_than_remaining():
    """Over-drawing returns what is left, then [] once empty."""


@pytest.mark.skip(reason="TODO")
def test_draw_negative_raises():
    """draw(-1) raises ValueError."""


@pytest.mark.skip(reason="TODO")
def test_exchange_keeps_count():
    """exchange returns len(tiles) tiles and remaining() is unchanged."""


@pytest.mark.skip(reason="TODO")
def test_exchange_too_few_raises():
    """Exchanging more tiles than remain raises ValueError and leaves the bag unchanged."""
