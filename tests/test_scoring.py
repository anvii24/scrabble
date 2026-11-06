"""Step 3 (rules and scoring): planned tests for move scoring and end-game adjustment."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_plain_word_sums_letters():
    """A word on no premiums scores the sum of its letters."""


@pytest.mark.skip(reason="TODO")
def test_letter_premiums_apply():
    """DL and TL multiply the tile on them."""


@pytest.mark.skip(reason="TODO")
def test_word_premiums_apply():
    """DW and TW multiply the word total, including the centre square."""


@pytest.mark.skip(reason="TODO")
def test_two_word_premiums_multiply():
    """A word across two DW squares scores times 4, across two TW times 9."""


@pytest.mark.skip(reason="TODO")
def test_premium_not_reused():
    """Existing tiles on premium squares count at face value."""


@pytest.mark.skip(reason="TODO")
def test_blank_scores_zero_but_triggers_word_premium():
    """A blank adds 0 but its DW still doubles the word."""


@pytest.mark.skip(reason="TODO")
def test_cross_words_are_scored():
    """Each cross word is added, and a new tile's premium counts in both words."""


@pytest.mark.skip(reason="TODO")
def test_bingo_adds_50_once():
    """Seven tiles add 50 once; six tiles do not."""


@pytest.mark.skip(reason="TODO")
def test_pass_and_exchange_score_zero():
    """Non-play moves score 0."""


@pytest.mark.skip(reason="TODO")
def test_score_move_does_not_mutate_board():
    """The board is unchanged afterwards."""


@pytest.mark.skip(reason="TODO")
def test_end_game_went_out():
    """The player who went out gains the opponent's rack value; the opponent loses it."""


@pytest.mark.skip(reason="TODO")
def test_end_game_no_one_went_out():
    """With who_went_out=None each player only loses their own rack value."""


@pytest.mark.skip(reason="TODO")
def test_end_game_does_not_mutate_scores():
    """The input list is unchanged, and scores can go negative."""
