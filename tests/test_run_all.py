"""Step 8 (experiments): planned tests for the experiment runner."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_parse_args_defaults():
    """No arguments give all techniques, seeds 0..4 and budget 100."""


@pytest.mark.skip(reason="TODO")
def test_parse_args_rejects_unknown_technique():
    """An unknown --tech exits with an error."""


@pytest.mark.skip(reason="TODO")
def test_save_history_format():
    """The CSV has header call,best_fitness and one row per history entry."""


@pytest.mark.skip(reason="TODO")
def test_append_summary_writes_header_once():
    """Two appends give one header and two rows."""


@pytest.mark.skip(reason="TODO")
def test_append_summary_quotes_weights():
    """The weights JSON reads back as one column."""


@pytest.mark.skip(reason="TODO")
def test_evaluate_weights_plays_held_out_seeds():
    """It plays exactly seeds 1000-1049, alternating who starts."""


@pytest.mark.skip(reason="TODO")
def test_main_runs_each_technique_and_seed():
    """With stub techniques, every combination writes its outputs."""
