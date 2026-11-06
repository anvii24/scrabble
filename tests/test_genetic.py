"""Step 7 (optimisation): planned tests for the genetic algorithm."""

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
def test_gen_stats_recorded():
    """avg_per_gen and best_per_gen have one entry per generation."""


@pytest.mark.skip(reason="TODO")
def test_elites_survive_without_reevaluation():
    """The best individuals carry over and spend no fitness calls."""


@pytest.mark.skip(reason="TODO")
def test_best_per_gen_never_decreases():
    """Elitism keeps the generation best from falling."""


@pytest.mark.skip(reason="TODO")
def test_crossover_never_touches_gene_0():
    """All individuals keep gene 0 at 1.0."""


@pytest.mark.skip(reason="TODO")
def test_mutation_stays_in_bounds():
    """All genes stay within BOUNDS."""


@pytest.mark.skip(reason="TODO")
def test_bad_parameters_raise():
    """elite or tour_k above pop_size raises ValueError."""
