"""Step 6 (game loop and UI): planned tests for the program entry point."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_choose_greedy():
    """Choosing greedy returns a GreedyPlayer."""


@pytest.mark.skip(reason="TODO")
def test_choose_weights_file():
    """A valid file returns a WeightedPlayer with those weights."""


@pytest.mark.skip(reason="TODO")
def test_bad_choice_reprompts():
    """A bad choice, missing file or wrong weight count asks again."""


@pytest.mark.skip(reason="TODO")
def test_missing_word_list_exits_cleanly():
    """With no word list it prints where to put one and exits."""
