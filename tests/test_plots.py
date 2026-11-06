"""Step 8 (experiments): planned tests for the figures and results table."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_convergence_creates_png():
    """Sample history files produce convergence.png."""


@pytest.mark.skip(reason="TODO")
def test_convergence_averages_over_seeds():
    """Averaging stops at the shortest history of a technique."""


@pytest.mark.skip(reason="TODO")
def test_convergence_parses_underscored_names():
    """history_hill_climb_0.csv gives technique hill_climb, seed 0."""


@pytest.mark.skip(reason="TODO")
def test_winrate_creates_png():
    """A sample summary.csv produces winrate.png."""


@pytest.mark.skip(reason="TODO")
def test_winrate_handles_single_seed():
    """One seed draws with no error bar."""


@pytest.mark.skip(reason="TODO")
def test_results_table_has_a_row_per_technique():
    """results_table.md has one row per technique."""


@pytest.mark.skip(reason="TODO")
def test_missing_inputs_raise():
    """An empty folder raises FileNotFoundError."""
