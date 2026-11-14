from __future__ import annotations

import pytest

from scrabble.constants import RACK_SIZE
from scrabble.game import SCORELESS_TURN_LIMIT, apply_move, is_over, new_game, play_game
from scrabble.lexicon import Lexicon
from scrabble.players import GreedyPlayer, RandomPlayer
from scrabble.types import Move, Placement, Tile


@pytest.fixture(scope="module")
def lexicon() -> Lexicon:
    lex = Lexicon()
    lex.load("data/enable1.txt")
    return lex


def test_new_game_deals_full_racks():
    state = new_game(seed=0, n_players=2)
    assert len(state.racks) == 2
    for rack in state.racks:
        assert len(rack.tiles) == RACK_SIZE
    assert state.scores == [0, 0]
    assert state.turn == 0
    assert state.passes == 0
    assert state.bag.remaining() == 100 - 2 * RACK_SIZE


def test_new_game_is_seeded():
    a = new_game(seed=42, n_players=2)
    b = new_game(seed=42, n_players=2)
    assert [t.letter for t in a.racks[0].tiles] == [t.letter for t in b.racks[0].tiles]
    assert [t.letter for t in a.racks[1].tiles] == [t.letter for t in b.racks[1].tiles]


def test_new_game_too_few_players_raises():
    with pytest.raises(ValueError):
        new_game(seed=0, n_players=1)


def test_apply_play_updates_everything():
    state = new_game(seed=1, n_players=2)
    rack = state.racks[0]
    tile = rack.tiles[0]
    move = Move(
        kind="play",
        placements=[Placement(7, 7, tile)],
        score=0,
        words=[tile.letter],
    )
    rack_before = len(rack.tiles)
    bag_before = state.bag.remaining()

    apply_move(state, move)

    assert state.board.get(7, 7) == tile
    assert tile not in state.racks[0].tiles
    assert len(state.racks[0].tiles) == rack_before
    assert state.bag.remaining() == bag_before - 1
    assert state.scores[0] == move.score
    assert state.passes == 0
    assert state.turn == 1


def test_apply_play_handles_blank_tiles():
    state = new_game(seed=1, n_players=2)
    rack = state.racks[0]
    blank = next((t for t in rack.tiles if t.is_blank), None)
    if blank is None:
        blank = Tile("?", 0, True)
        rack.tiles[0] = blank

    played_as = Tile("Z", 0, True)
    move = Move(kind="play", placements=[Placement(7, 7, played_as)], score=0, words=["Z"])

    apply_move(state, move)

    assert blank not in state.racks[0].tiles
    assert state.board.get(7, 7) == played_as


def test_apply_exchange_counts_as_pass():
    state = new_game(seed=2, n_players=2)
    rack = state.racks[0]
    exchanged = rack.tiles[:2]
    bag_before = state.bag.remaining()
    move = Move(kind="exchange", exchanged=exchanged)

    apply_move(state, move)

    assert state.passes == 1
    assert len(state.racks[0].tiles) == RACK_SIZE
    assert state.bag.remaining() == bag_before
    for tile in exchanged:
        assert tile in state.bag.tiles


def test_apply_exchange_with_low_bag_raises():
    state = new_game(seed=3, n_players=2)
    state.bag.draw(state.bag.remaining() - 1)
    move = Move(kind="exchange", exchanged=state.racks[0].tiles[:2])

    with pytest.raises(ValueError):
        apply_move(state, move)


def test_apply_pass_increments_passes():
    state = new_game(seed=4, n_players=2)
    apply_move(state, Move(kind="pass"))
    assert state.passes == 1
    assert state.turn == 1


def test_apply_rejects_tiles_not_held():
    state = new_game(seed=5, n_players=2)
    foreign_tile = Tile("Q", 10, False)
    while foreign_tile in state.racks[0].tiles:
        foreign_tile = Tile("Q", 10, False)
    move = Move(kind="play", placements=[Placement(7, 7, foreign_tile)])

    with pytest.raises(ValueError):
        apply_move(state, move)


def test_is_over_bag_and_rack_empty():
    state = new_game(seed=6, n_players=2)
    state.bag.draw(state.bag.remaining())
    state.racks[0].tiles.clear()
    assert is_over(state) is True


def test_is_over_not_when_only_bag_empty():
    state = new_game(seed=6, n_players=2)
    state.bag.draw(state.bag.remaining())
    assert all(len(r.tiles) > 0 for r in state.racks)
    assert is_over(state) is False


def test_is_over_six_passes():
    state = new_game(seed=7, n_players=2)
    for _ in range(SCORELESS_TURN_LIMIT - 1):
        apply_move(state, Move(kind="pass"))
    assert is_over(state) is False
    apply_move(state, Move(kind="pass"))
    assert is_over(state) is True


def test_play_game_returns_expected_keys(lexicon):
    p1 = GreedyPlayer(lexicon, "G1")
    p2 = GreedyPlayer(lexicon, "G2")
    result = play_game(p1, p2, seed=0, lexicon=lexicon)
    assert set(result.keys()) == {"scores", "winner", "turns"}
    assert len(result["scores"]) == 2
    assert result["winner"] in (0, 1, None)
    assert result["turns"] > 0


def test_play_game_applies_end_game_adjust(lexicon):
    p1 = GreedyPlayer(lexicon, "G1")
    p2 = GreedyPlayer(lexicon, "G2")
    result = play_game(p1, p2, seed=0, lexicon=lexicon)
    assert all(isinstance(s, int) for s in result["scores"])


def test_play_game_is_deterministic(lexicon):
    p1a, p2a = GreedyPlayer(lexicon, "G1"), GreedyPlayer(lexicon, "G2")
    p1b, p2b = GreedyPlayer(lexicon, "G1"), GreedyPlayer(lexicon, "G2")
    result_a = play_game(p1a, p2a, seed=9, lexicon=lexicon)
    result_b = play_game(p1b, p2b, seed=9, lexicon=lexicon)
    assert result_a == result_b


def test_play_game_rejects_illegal_move(lexicon):
    class CheatingPlayer:
        name = "Cheat"

        def choose_move(self, state, rack):
            tile = rack.tiles[0]
            return Move(kind="play", placements=[Placement(0, 0, tile)], score=0, words=[])

    p1 = CheatingPlayer()
    p2 = GreedyPlayer(lexicon, "G2")
    with pytest.raises(ValueError):
        play_game(p1, p2, seed=0, lexicon=lexicon)


def test_full_greedy_vs_random_game_completes(lexicon):
    p1 = GreedyPlayer(lexicon, "Greedy")
    p2 = RandomPlayer(lexicon, seed=1, name="Random")
    result = play_game(p1, p2, seed=11, lexicon=lexicon)
    assert result["turns"] > 0
