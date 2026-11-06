"""Step 1 (foundations): checks the shared data types."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from scrabble.types import Move, Placement, Player, Tile


def test_tile_is_frozen_and_hashable():
    tile = Tile("A", 1)
    assert not tile.is_blank
    assert len({tile, Tile("A", 1)}) == 1
    with pytest.raises(FrozenInstanceError):
        tile.letter = "B"


def test_placement_is_frozen():
    with pytest.raises(FrozenInstanceError):
        Placement(7, 7, Tile("A", 1)).row = 0


def test_move_defaults_are_not_shared():
    first, second = Move("pass"), Move("pass")
    first.placements.append(Placement(7, 7, Tile("A", 1)))
    assert second.placements == []
    assert (second.exchanged, second.score, second.words) == ([], 0, [])


def test_player_choose_move_is_abstract():
    with pytest.raises(NotImplementedError):
        Player().choose_move(None, None)
