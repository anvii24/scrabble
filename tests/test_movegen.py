"""Step 4 (lexicon and move generation): planned tests for anchors, cross-checks and move generation."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_anchors_empty_board_is_centre():
    """An empty board gives [CENTER]."""


@pytest.mark.skip(reason="TODO")
def test_anchors_surround_tiles():
    """A single tile gives its four neighbours, clipped at the edge."""


@pytest.mark.skip(reason="TODO")
def test_cross_checks_empty_board():
    """An empty board gives {}."""


@pytest.mark.skip(reason="TODO")
def test_cross_checks_limit_letters():
    """With A above a square and only AT and AN valid, the set is {T, N}."""


@pytest.mark.skip(reason="TODO")
def test_cross_checks_empty_set_when_nothing_fits():
    """A square nothing fits has an empty set, not a missing key."""


@pytest.mark.skip(reason="TODO")
def test_first_move_covers_centre():
    """Every move on an empty board covers (7, 7)."""


@pytest.mark.skip(reason="TODO")
def test_all_moves_pass_validate():
    """Every generated move is accepted by rules.validate."""


@pytest.mark.skip(reason="TODO")
def test_all_moves_scored():
    """Every move.score equals score_move on the original board."""


@pytest.mark.skip(reason="TODO")
def test_down_plays_are_found():
    """Plays in both directions appear, with row and col mapped back."""


@pytest.mark.skip(reason="TODO")
def test_blanks_produce_moves():
    """A rack with '?' gives moves with is_blank tiles at 0 points."""


@pytest.mark.skip(reason="TODO")
def test_no_duplicate_moves():
    """No two moves have the same placements, including one-tile plays."""


@pytest.mark.skip(reason="TODO")
def test_matches_brute_force():
    """generate_moves and brute_force_moves agree on small positions."""


@pytest.mark.skip(reason="TODO")
def test_output_order_is_deterministic():
    """Two calls return the same order, including across PYTHONHASHSEED values."""


@pytest.mark.skip(reason="TODO")
def test_inputs_not_mutated():
    """The board and rack are unchanged afterwards."""


@pytest.mark.skip(reason="TODO")
def test_empty_rack_gives_no_moves():
    """An empty rack returns []."""
