"""Step 6: game loop.

Owns the turn-by-turn lifecycle of a Scrabble game: dealing a fresh game,
applying a validated move to a `GameState`, deciding when the game is over,
and running a full game between two `Player`s end to end.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.bag import TileBag
from scrabble.board import Board
from scrabble.constants import RACK_SIZE
from scrabble.rack import Rack
from scrabble.rules import validate
from scrabble.scoring import end_game_adjust, score_move
from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon

# Standard club rule: the game ends once six consecutive scoreless turns
# (pass or exchange) have gone by, i.e. three fruitless turns each for two
# players, regardless of how many players are seated at the table.
SCORELESS_TURN_LIMIT = 6


def new_game(seed: int, n_players: int = 2) -> GameState:
    """Deal a fresh game: an empty board, a shuffled bag, and full racks.

    Args:
        seed: seeds the tile bag's shuffle, so the whole deal is reproducible.
        n_players: number of players to deal racks for. Must be at least 2.

    Returns:
        A `GameState` with scores at zero, the bag's starting tiles dealt out
        into `n_players` racks of `RACK_SIZE` tiles, and player 0 to move.

    Raises:
        ValueError: if `n_players` is less than 2.
    """
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
    """Check whether `rack` contains every tile in `tiles` (as a multiset)."""
    remaining = rack.tiles.copy()

    for tile in tiles:
        if tile not in remaining:
            return False
        remaining.remove(tile)

    return True


def _rack_tiles_for_play(rack: Rack, placements: list) -> list:
    """Resolve the actual rack `Tile`s spent by a "play" move's placements.

    A placed tile that came from a blank is relettered to whatever letter
    it is standing in for (e.g. a blank played as "Z" shows up in the move
    as ``Tile("Z", 0, True)``), so it will not be `==` to the rack's own
    blank tile, `Tile("?", 0, True)`. This matches each placement to a
    concrete tile still sitting in the rack -- an exact match for ordinary
    letters, or any remaining blank for a blank placement -- instead of
    comparing placement tiles to rack tiles by value.

    Args:
        rack: the rack the tiles are being taken from.
        placements: the move's placements.

    Returns:
        The list of actual rack `Tile` objects consumed by the move, in
        placement order.

    Raises:
        ValueError: if the rack does not hold a tile for every placement.
    """
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
    """Apply `move` to `state` in place, mutating the board, racks and bag.

    For a "play" move the tiles must already be on the current player's
    rack (callers are expected to have validated the move with
    `scrabble.rules.validate` first; this function re-checks rack
    ownership as a safety net). The move's `score` is computed here with
    `scrabble.scoring.score_move` if it was not already set by the caller.

    For an "exchange" move the given tiles are swapped for fresh ones drawn
    from the bag. Exchanging counts as a scoreless turn, the same as a pass.

    For a "pass" move nothing moves, only the pass counter advances.

    Args:
        state: the game state to update.
        move: the move to apply. Its `kind` must be "play", "exchange" or
            "pass".

    Raises:
        ValueError: if the move's tiles are not on the current player's
            rack, if an exchange is attempted with too few tiles left in
            the bag, or if `move.kind` is not recognised.
    """
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
    """Check whether the game has reached an end condition.

    The game is over when either:

    * the bag is empty and some player's rack is also empty (that player
      went out), or
    * `SCORELESS_TURN_LIMIT` consecutive scoreless turns (passes or
      exchanges) have been taken.

    Args:
        state: the game state to inspect.

    Returns:
        True if the game has ended, False otherwise.
    """
    if state.bag.remaining() == 0:
        if any(len(rack.tiles) == 0 for rack in state.racks):
            return True

    if state.passes >= SCORELESS_TURN_LIMIT:
        return True

    return False


def _who_went_out(state: GameState) -> int | None:
    """Return the index of the player who emptied their rack, if any."""
    for i, rack in enumerate(state.racks):
        if len(rack.tiles) == 0:
            return i

    return None


def play_game(p1: Player, p2: Player, seed: int, lexicon: Lexicon) -> dict:
    """Play a complete two-player game between `p1` and `p2`.

    Each player is asked for a move via `choose_move`, in turn; the move is
    validated with `scrabble.rules.validate` and then applied. An illegal
    move ends the game immediately with an error, since every `Player`
    implementation in this project is expected to only offer legal moves.

    Args:
        p1: the player to move first.
        p2: the second player.
        seed: seeds `new_game`, so the deal is reproducible.
        lexicon: the word list used to validate moves.

    Returns:
        A dict with keys:

        * "scores": final scores (after the end-of-game rack adjustment),
          in player order ``[p1's score, p2's score]``.
        * "winner": 0 if `p1` won, 1 if `p2` won, or None for a tie.
        * "turns": number of turns played (one per `apply_move` call).

    Raises:
        ValueError: if a player returns an illegal move.
    """
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
