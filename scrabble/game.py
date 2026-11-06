"""Step 6 (game loop and UI): game setup, turn application and the full game loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon


def new_game(seed: int, n_players: int = 2) -> GameState:
    """Return a fresh game.

    Inputs:
        seed: seed for the TileBag; the whole game follows from it.
        n_players: number of players.
    Outputs:
        A GameState with an empty Board, TileBag(seed), one full Rack per
        player (filled in player order), all scores 0, turn 0 and passes 0.
    Edge cases:
        Raises ValueError if n_players < 2.
    """
    raise NotImplementedError


def apply_move(state: GameState, move: Move) -> None:
    """Apply a move for the player to move, mutating `state`.

    Inputs:
        state: the current game; the mover is state.turn % len(state.racks).
        move: a move already accepted by rules.validate, with its score set.
    Rules:
        'play': place the tiles, remove them from the rack, refill it, add
            move.score to the mover's total, and reset passes to 0.
        'exchange': swap move.exchanged through the bag, and add 1 to passes.
        'pass': add 1 to passes.
        Every kind then adds 1 to turn.
        Exchanges count as passes (as in the official scoreless-turn rule).
        Otherwise two players who can only exchange would never end the game.
    Edge cases:
        Raises ValueError for an exchange with fewer than RACK_SIZE tiles in
        the bag, an exchange or play of tiles the mover does not hold, or an
        unknown kind.
    """
    raise NotImplementedError


def is_over(state: GameState) -> bool:
    """Return True if the game has ended.

    Outputs:
        True if the bag is empty and some rack is empty, or passes >= 6.
    """
    raise NotImplementedError


def play_game(p1: Player, p2: Player, seed: int, lexicon: Lexicon) -> dict:
    """Play one full game and return the result.

    Inputs:
        p1: moves first.
        p2: moves second.
        seed: passed to new_game.
        lexicon: used to validate each move.
    Outputs:
        A dict with:
            "scores": [p1 final score, p2 final score], after end_game_adjust.
            "winner": 0 if p1 won, 1 if p2 won, None for a tie.
            "turns": the number of turns taken.
    Rules:
        Loop until is_over: ask the player to move, validate, then apply_move.
        Then apply scoring.end_game_adjust, with who_went_out being the index
        of the player with an empty rack, or None if the game ended on passes.
        Deterministic for a given seed if both players are.
    Edge cases:
        Raises ValueError if a player returns an illegal move, so that bugs in
        a player are not silently played through. Pass the rack from
        state.racks directly; players must not mutate it.
    """
    raise NotImplementedError
