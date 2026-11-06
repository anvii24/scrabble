"""Step 5 (players and evaluation): the greedy baseline and a random player.

choose_move receives only (state, rack), so each player is given the lexicon
when it is constructed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


class GreedyPlayer(Player):
    """The baseline: always takes the highest-scoring play."""

    def __init__(self, lexicon: Lexicon, name: str = "Greedy") -> None:
        """Store the lexicon and name."""
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        """Return the move with the highest score.

        Inputs:
            state: the current position.
            rack: this player's rack.
        Outputs:
            The generate_moves entry with the highest move.score.
        Rules:
            Ties go to the first move in generate_moves order, which is
            deterministic. If there is no play: exchange the whole rack when
            the bag holds at least RACK_SIZE tiles, otherwise pass.
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """Picks uniformly among legal plays; a weak sanity-check opponent."""

    def __init__(self, lexicon: Lexicon, seed: int = 0, name: str = "Random") -> None:
        """Store the lexicon and name and create a private random.Random(seed)."""
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        """Return a uniformly random legal play.

        Inputs:
            state: the current position.
            rack: this player's rack.
        Outputs:
            A random entry of generate_moves, chosen with the private Random.
        Edge cases:
            With no play, uses the same exchange-or-pass fallback as
            GreedyPlayer.
        """
        raise NotImplementedError
