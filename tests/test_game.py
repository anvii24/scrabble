"""Step 6 (game loop and UI): planned tests for game setup and the game loop."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_new_game_deals_full_racks():
    """Two racks of 7, 86 in the bag, scores [0, 0], turn 0, passes 0."""


@pytest.mark.skip(reason="TODO")
def test_new_game_is_seeded():
    """The same seed deals the same racks."""


@pytest.mark.skip(reason="TODO")
def test_new_game_too_few_players_raises():
    """n_players=1 raises ValueError."""


@pytest.mark.skip(reason="TODO")
def test_apply_play_updates_everything():
    """Board, rack, refill, score and turn change; passes resets to 0."""


@pytest.mark.skip(reason="TODO")
def test_apply_exchange_counts_as_pass():
    """Rack size is kept, the bag size is unchanged and passes rises by 1."""


@pytest.mark.skip(reason="TODO")
def test_apply_exchange_with_low_bag_raises():
    """An exchange with fewer than 7 in the bag raises ValueError."""


@pytest.mark.skip(reason="TODO")
def test_apply_pass_increments_passes():
    """Passes and turn rise by 1."""


@pytest.mark.skip(reason="TODO")
def test_apply_rejects_tiles_not_held():
    """Playing or exchanging unheld tiles raises ValueError."""


@pytest.mark.skip(reason="TODO")
def test_is_over_bag_and_rack_empty():
    """True once the bag and one rack are empty."""


@pytest.mark.skip(reason="TODO")
def test_is_over_not_when_only_bag_empty():
    """False while the bag is empty but both racks hold tiles."""


@pytest.mark.skip(reason="TODO")
def test_is_over_six_passes():
    """True at 6 passes and False at 5."""


@pytest.mark.skip(reason="TODO")
def test_play_game_returns_expected_keys():
    """The result has scores, winner and turns."""


@pytest.mark.skip(reason="TODO")
def test_play_game_applies_end_game_adjust():
    """Final scores include rack adjustment."""


@pytest.mark.skip(reason="TODO")
def test_play_game_reports_tie():
    """Equal scores give winner None."""


@pytest.mark.skip(reason="TODO")
def test_play_game_is_deterministic():
    """The same seed and players give identical results."""


@pytest.mark.skip(reason="TODO")
def test_play_game_rejects_illegal_move():
    """A player returning an illegal move raises ValueError."""
