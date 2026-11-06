from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon


def new_game(seed: int, n_players: int = 2) -> GameState:
    raise NotImplementedError


def apply_move(state: GameState, move: Move) -> None:
    raise NotImplementedError


def is_over(state: GameState) -> bool:
    raise NotImplementedError


def play_game(p1: Player, p2: Player, seed: int, lexicon: Lexicon) -> dict:
    raise NotImplementedError
