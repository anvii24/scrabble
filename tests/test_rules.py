"""Step 3 (rules and scoring): planned tests for word detection and move validation."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_words_formed_main_word_only():
    """A play with no neighbours returns just the main word."""


@pytest.mark.skip(reason="TODO")
def test_words_formed_includes_cross_words():
    """Parallel plays return the main word and each cross word."""


@pytest.mark.skip(reason="TODO")
def test_words_formed_extends_through_existing_tiles():
    """Tiles at either end of the run and in gaps are included in order."""


@pytest.mark.skip(reason="TODO")
def test_words_formed_single_tile_both_directions():
    """One tile touching tiles on two axes returns both words."""


@pytest.mark.skip(reason="TODO")
def test_words_formed_skips_length_one():
    """Single-letter runs are never returned."""


@pytest.mark.skip(reason="TODO")
def test_words_formed_does_not_mutate_board():
    """The board is unchanged afterwards."""


@pytest.mark.skip(reason="TODO")
def test_validate_accepts_legal_first_move():
    """A word through (7, 7) on an empty board is legal."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_first_move_off_centre():
    """A first word missing the centre is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_single_tile_first_move():
    """One tile on the centre forms no word and is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_not_in_line():
    """Placements on two rows and two columns are rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_gap():
    """A gap in the line that no existing tile fills is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_accepts_gap_filled_by_board():
    """A gap filled by an existing tile is legal."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_unconnected():
    """A later word touching nothing is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_invalid_main_word():
    """A main word not in the lexicon is rejected, and the reason names it."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_invalid_cross_word():
    """A valid main word with an invalid cross word is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_rejects_occupied_or_duplicate_square():
    """Placing on a filled square, or twice on one square, is rejected."""


@pytest.mark.skip(reason="TODO")
def test_validate_accepts_pass_and_exchange():
    """Pass and exchange return (True, '')."""
