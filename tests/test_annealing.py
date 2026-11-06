"""Step 7 (optimisation): planned tests for simulated annealing."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_spends_exactly_budget():
    """CALLS equals budget at the end, and len(history) equals budget."""


@pytest.mark.skip(reason="TODO")
def test_history_never_decreases():
    """history is non-decreasing even though the current point can get worse."""


@pytest.mark.skip(reason="TODO")
def test_is_seeded():
    """The same seed gives the same Result, runtime aside."""


@pytest.mark.skip(reason="TODO")
def test_always_accepts_improvement():
    """With a stub fitness, a better neighbour is always accepted."""


@pytest.mark.skip(reason="TODO")
def test_accepts_worse_when_hot():
    """At a very high T0, worse moves are accepted."""


@pytest.mark.skip(reason="TODO")
def test_rejects_worse_when_cold():
    """At a tiny T0, worse moves are not accepted."""


@pytest.mark.skip(reason="TODO")
def test_temperature_cools_geometrically():
    """extra['final_T'] matches T0 * alpha ** steps."""


@pytest.mark.skip(reason="TODO")
def test_weight_0_stays_fixed():
    """best_weights[0] is 1.0."""
