"""Step 7 (optimisation): planned tests for tabu search."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_spends_exactly_budget():
    """CALLS equals budget at the end, and len(history) equals budget."""


@pytest.mark.skip(reason="TODO")
def test_history_never_decreases():
    """history is non-decreasing."""


@pytest.mark.skip(reason="TODO")
def test_is_seeded():
    """The same seed gives the same Result, runtime aside."""


@pytest.mark.skip(reason="TODO")
def test_moves_downhill():
    """With a stub fitness, it moves to the best neighbour even when worse."""


@pytest.mark.skip(reason="TODO")
def test_tabu_blocks_undoing_a_move():
    """A neighbour in the forbidden direction is not taken."""


@pytest.mark.skip(reason="TODO")
def test_aspiration_overrides_tabu():
    """A tabu neighbour better than the best ever is taken."""


@pytest.mark.skip(reason="TODO")
def test_tabu_list_limited_to_size():
    """The list never exceeds tabu_size."""


@pytest.mark.skip(reason="TODO")
def test_weight_0_stays_fixed():
    """best_weights[0] is 1.0."""
