"""Step 7 (optimisation): planned tests for the shared fitness function."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_reset_calls_zeroes_counter():
    """CALLS is 0 after reset_calls."""


@pytest.mark.skip(reason="TODO")
def test_calls_counts_once_per_fitness_call():
    """CALLS rises by 1 per call, whatever n_games is."""


@pytest.mark.skip(reason="TODO")
def test_fitness_is_deterministic():
    """Identical arguments give identical values."""


@pytest.mark.skip(reason="TODO")
def test_score_only_weights_near_zero():
    """Weights [1, 0, 0, 0, 0, 0] mirror greedy, so the margin stays small."""


@pytest.mark.skip(reason="TODO")
def test_starting_player_alternates():
    """Half the games have WeightedPlayer as p1 and the margin sign is correct for both."""


@pytest.mark.skip(reason="TODO")
def test_uses_requested_seed_range():
    """play_game receives exactly seed .. seed + n_games - 1."""


@pytest.mark.skip(reason="TODO")
def test_zero_games_raises():
    """n_games=0 raises ValueError."""
