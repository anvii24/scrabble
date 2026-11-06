"""Step 6 (game loop and UI): play Scrabble against an AI from the terminal."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.types import Player


def choose_opponent(lexicon: Lexicon) -> Player:
    """Ask the user which AI to play and return it.

    Inputs:
        lexicon: passed to the player's constructor.
    Outputs:
        A GreedyPlayer, or a WeightedPlayer using weights read from a file.
    Rules:
        A weights file is a JSON list of 6 numbers, the same format as the
        `weights` column in experiments/results/summary.csv.
    Edge cases:
        On an unknown choice, a missing file or the wrong number of weights,
        print the problem and ask again.
    """
    raise NotImplementedError


def main() -> None:
    """Load the lexicon, choose an opponent, and play one game.

    Rules:
        Load optimise.fitness.LEXICON_PATH, call choose_opponent, then run
        play_game with a HumanPlayer as p1 and a seed from the current time.
        Print the final scores and the winner.
    Edge cases:
        If the word list is missing, print where to put it and exit.
        Ctrl-C ends the game cleanly.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
