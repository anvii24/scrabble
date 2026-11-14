from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.bag import TileBag
from scrabble.board import Board
from scrabble.rack import Rack
from scrabble.rules import validate
from scrabble.scoring import end_game_adjust, score_move
from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon

SCORELESS_TURN_LIMIT = 6


def new_game(seed: int, n_players: int = 2) -> GameState:
    if n_players < 2:
        raise ValueError("A game needs at least two players")

    board = Board()
    bag = TileBag(seed)
    racks = [Rack() for _ in range(n_players)]

    for rack in racks:
        rack.refill(bag)

    return GameState(
        board=board,
        bag=bag,
        racks=racks,
        scores=[0 for _ in range(n_players)],
        turn=0,
        passes=0,
    )


def _held(rack: Rack, tiles: list) -> bool:
    remaining = rack.tiles.copy()

    for tile in tiles:
        if tile not in remaining:
            return False
        remaining.remove(tile)

    return True


def _rack_tiles_for_play(rack: Rack, placements: list) -> list:
    remaining = rack.tiles.copy()
    spent = []

    for placement in placements:
        wanted = placement.tile

        if wanted.is_blank:
            match = next((t for t in remaining if t.is_blank), None)
        else:
            match = wanted if wanted in remaining else None

        if match is None:
            raise ValueError("Move uses tiles that are not on the rack")

        remaining.remove(match)
        spent.append(match)

    return spent


def apply_move(state: GameState, move: Move) -> None:
    rack = state.racks[state.turn]

    if move.kind == "play":
        spent_tiles = _rack_tiles_for_play(rack, move.placements)

        state.board.place(move.placements)
        rack.remove(spent_tiles)

        if not move.score:
            move.score = score_move(state.board, move)

        state.scores[state.turn] += move.score
        rack.refill(state.bag)
        state.passes = 0

    elif move.kind == "exchange":
        if not _held(rack, move.exchanged):
            raise ValueError("Exchange uses tiles that are not on the rack")

        if state.bag.remaining() < len(move.exchanged):
            raise ValueError("Not enough tiles in the bag to exchange")

        rack.remove(move.exchanged)
        new_tiles = state.bag.exchange(move.exchanged)
        rack.add(new_tiles)
        state.passes += 1

    elif move.kind == "pass":
        state.passes += 1

    else:
        raise ValueError(f"Unknown move kind: {move.kind!r}")

    state.turn = (state.turn + 1) % len(state.racks)


def is_over(state: GameState) -> bool:
    if state.bag.remaining() == 0:
        if any(len(rack.tiles) == 0 for rack in state.racks):
            return True

    if state.passes >= SCORELESS_TURN_LIMIT:
        return True

    return False


def _who_went_out(state: GameState) -> int | None:
    for i, rack in enumerate(state.racks):
        if len(rack.tiles) == 0:
            return i

    return None


def play_game(p1: Player, p2: Player, seed: int, lexicon: Lexicon) -> dict:
    players = [p1, p2]
    state = new_game(seed, n_players=2)
    turns = 0

    while not is_over(state):
        current = players[state.turn]
        rack = state.racks[state.turn]
        move = current.choose_move(state, rack)

        ok, reason = validate(state.board, move, lexicon)

        if not ok:
            raise ValueError(f"{current.name} proposed an illegal move: {reason}")

        apply_move(state, move)
        turns += 1

    who_went_out = _who_went_out(state)
    final_scores = end_game_adjust(state.scores, state.racks, who_went_out)

    if final_scores[0] > final_scores[1]:
        winner = 0
    elif final_scores[1] > final_scores[0]:
        winner = 1
    else:
        winner = None

    return {
        "scores": final_scores,
        "winner": winner,
        "turns": turns,
    }
