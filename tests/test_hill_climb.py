"""Step 7 (optimisation): planned tests for hill climbing."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_spends_exactly_budget():
    """CALLS equals budget at the end, and len(history) equals budget."""


@pytest.mark.skip(reason="TODO")
def test_history_never_decreases():
    """history is non-decreasing."""


@pytest.mark.skip(reason="TODO")
def test_best_matches_history():
    """best_fitness equals history[-1]."""


@pytest.mark.skip(reason="TODO")
def test_is_seeded():
    """The same seed gives the same Result, runtime aside."""


@pytest.mark.skip(reason="TODO")
def test_restarts_at_local_optimum():
    """With a stub fitness that never improves, extra['restarts'] is above 0."""


@pytest.mark.skip(reason="TODO")
def test_weight_0_stays_fixed():
    """best_weights[0] is 1.0."""
