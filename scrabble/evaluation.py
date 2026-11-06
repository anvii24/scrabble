"""Step 5 (players and evaluation): the weighted move evaluation being tuned."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def features(state: GameState, move: Move, rack: Rack) -> list[float]:
    """Return the 6 features of a candidate move, in fixed order.

    Inputs:
        state: the position BEFORE the move (not mutated).
        move: the candidate 'play' move, with its score already set.
        rack: the mover's rack before the move (not mutated).
    Outputs:
        [score, leave, vowel_balance, tw_opened, dw_opened, bag_frac]. Weight
        index i multiplies feature i, so weight 0 (fixed at 1.0) scales score.
    Rules:
        The "kept" tiles are the rack minus the tiles placed.
        score: move.score.
        leave: +1 per S or blank kept; -1 per duplicate, i.e. each kept tile
            beyond the first of its letter (two blanks are not duplicates);
            -2 if Q is kept with no U kept. A kept blank does not count as a U.
        vowel_balance: -abs(vowels_kept - 3), using constants.VOWELS. Blanks
            and Y are not vowels here.
        tw_opened: number of TW squares newly reachable by the opponent, i.e.
            empty squares that are anchors after the move but were not before.
        dw_opened: the same count for DW squares.
        bag_frac: state.bag.remaining() / 100.
    Edge cases:
        Compute the after-move anchors on a board.copy(), never on the real
        board. Squares the move itself covers cannot count as opened.
    """
    raise NotImplementedError


def evaluate(weights: list[float], feats: list[float]) -> float:
    """Return the dot product of `weights` and `feats`.

    Edge cases:
        Raises ValueError if the lengths differ; zip() alone would silently
        truncate.
    """
    raise NotImplementedError


class WeightedPlayer(Player):
    """Chooses the play that maximises evaluate(weights, features(...))."""

    def __init__(
        self, weights: list[float], lexicon: Lexicon, name: str = "Weighted"
    ) -> None:
        """Store the weights, lexicon and name.

        Inputs:
            weights: a weight vector of length 6, index 0 fixed at 1.0.
            lexicon: the word list, needed by generate_moves.
            name: display name.
        """
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        """Return the legal play with the highest evaluation.

        Inputs:
            state: the current position.
            rack: this player's rack.
        Outputs:
            The generate_moves entry that maximises evaluate.
        Rules:
            Ties go to the first move in generate_moves order. With all of
            weights[1:] at 0 this reduces to GreedyPlayer.
        Edge cases:
            With no play, uses the same exchange-or-pass fallback as
            GreedyPlayer.
        """
        raise NotImplementedError
