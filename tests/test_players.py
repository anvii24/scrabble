"""Step 5 (players and evaluation): planned tests for the greedy and random players."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_greedy_takes_highest_score():
    """The chosen move has the maximum score among generate_moves."""


@pytest.mark.skip(reason="TODO")
def test_greedy_exchanges_whole_rack_when_stuck():
    """No play and at least 7 in the bag gives an exchange of all tiles."""


@pytest.mark.skip(reason="TODO")
def test_greedy_passes_when_stuck_and_bag_low():
    """No play and fewer than 7 in the bag gives a pass."""


@pytest.mark.skip(reason="TODO")
def test_greedy_is_deterministic():
    """The same position gives the same move."""


@pytest.mark.skip(reason="TODO")
def test_random_returns_legal_move():
    """The chosen move is in generate_moves."""


@pytest.mark.skip(reason="TODO")
def test_random_is_seeded():
    """The same seed gives the same sequence of choices."""


@pytest.mark.skip(reason="TODO")
def test_random_falls_back_when_stuck():
    """With no play it uses the greedy fallback."""
