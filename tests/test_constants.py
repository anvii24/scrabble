from __future__ import annotations

from collections import Counter

from scrabble.constants import CENTER, LETTER_COUNTS, LETTER_POINTS, PREMIUM, SIZE


def test_total_tiles_is_100():
    assert sum(LETTER_COUNTS.values()) == 100


def test_two_blanks_worth_zero():
    assert LETTER_COUNTS["?"] == 2
    assert LETTER_POINTS["?"] == 0


def test_every_letter_has_points():
    assert set(LETTER_COUNTS) == set(LETTER_POINTS)


def test_premium_counts():
    counts = Counter(PREMIUM.values())
    assert counts == {"TW": 8, "DW": 17, "TL": 12, "DL": 24}


def test_centre_is_double_word():
    assert PREMIUM[CENTER] == "DW"


def test_premium_squares_on_board():
    assert all(0 <= r < SIZE and 0 <= c < SIZE for r, c in PREMIUM)


def test_board_is_symmetric():
    last = SIZE - 1
    for (r, c), kind in PREMIUM.items():
        assert PREMIUM.get((c, r)) == kind
        assert PREMIUM.get((r, last - c)) == kind
        assert PREMIUM.get((last - r, c)) == kind
