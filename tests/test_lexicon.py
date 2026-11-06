"""Step 4 (lexicon and move generation): planned tests for the trie word list."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO")
def test_load_reads_words():
    """Words in a tmp_path file are found by is_word."""


@pytest.mark.skip(reason="TODO")
def test_load_normalises_and_skips_bad_lines():
    """Lowercase is uppercased; blank and non-alphabetic lines are skipped."""


@pytest.mark.skip(reason="TODO")
def test_load_missing_file_raises():
    """A missing path raises FileNotFoundError."""


@pytest.mark.skip(reason="TODO")
def test_is_word_rejects_prefix():
    """With only CAT loaded, CA is not a word but CAT is."""


@pytest.mark.skip(reason="TODO")
def test_is_word_empty_string_is_false():
    """The empty string is not a word."""


@pytest.mark.skip(reason="TODO")
def test_is_word_ignores_case():
    """cat and CAT give the same answer."""


@pytest.mark.skip(reason="TODO")
def test_has_prefix():
    """CA and CAT are prefixes of CAT; CAB is not."""


@pytest.mark.skip(reason="TODO")
def test_child_walks_the_trie():
    """Following child letter by letter reaches a node holding '$'."""


@pytest.mark.skip(reason="TODO")
def test_child_returns_none_when_missing():
    """A missing letter, and '$' itself, return None."""
