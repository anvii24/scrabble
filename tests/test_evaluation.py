"""Step 5 (players and evaluation): planned tests for features and the weighted player."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_features_length_and_order():
    """Exactly 6 values, in the documented order."""


@pytest.mark.skip(reason="TODO")
def test_feature_score():
    """Feature 0 is move.score."""


@pytest.mark.skip(reason="TODO")
def test_feature_leave_rewards_s_and_blank():
    """Each kept S or blank adds 1."""


@pytest.mark.skip(reason="TODO")
def test_feature_leave_penalises_duplicates():
    """Each kept copy beyond the first subtracts 1."""


@pytest.mark.skip(reason="TODO")
def test_feature_leave_q_without_u():
    """Q with no U subtracts 2; a kept U or a played Q does not."""


@pytest.mark.skip(reason="TODO")
def test_feature_vowel_balance():
    """Three vowels kept gives 0; none gives -3; blanks and Y are not vowels."""


@pytest.mark.skip(reason="TODO")
def test_feature_tw_opened():
    """A play reaching a TW-adjacent square counts it."""


@pytest.mark.skip(reason="TODO")
def test_feature_dw_opened():
    """The same for DW; squares reachable before the play are not counted."""


@pytest.mark.skip(reason="TODO")
def test_feature_bag_frac():
    """A bag of 50 gives 0.5."""


@pytest.mark.skip(reason="TODO")
def test_features_do_not_mutate_state():
    """The board, bag and rack are unchanged afterwards."""


@pytest.mark.skip(reason="TODO")
def test_evaluate_is_dot_product():
    """evaluate returns the sum of pairwise products."""


@pytest.mark.skip(reason="TODO")
def test_evaluate_length_mismatch_raises():
    """Different lengths raise ValueError."""


@pytest.mark.skip(reason="TODO")
def test_weighted_picks_max_evaluation():
    """The chosen move maximises evaluate."""


@pytest.mark.skip(reason="TODO")
def test_score_only_weights_match_greedy():
    """With weights [1, 0, 0, 0, 0, 0] it picks the same move as GreedyPlayer."""


@pytest.mark.skip(reason="TODO")
def test_weighted_falls_back_when_stuck():
    """With no play it uses the greedy fallback."""
