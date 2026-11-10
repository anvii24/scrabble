"""Step 6: command-line entry point.

Lets a human play a complete game against either the greedy baseline AI or
a weighted AI, right in the terminal. Run it from the project root with:

    python main.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from scrabble.evaluation import WeightedPlayer
from scrabble.game import apply_move, is_over, new_game
from scrabble.lexicon import Lexicon
from scrabble.players import GreedyPlayer
from scrabble.rules import validate
from scrabble.scoring import end_game_adjust
from scrabble.types import Move
from scrabble.ui import HumanPlayer, show

if TYPE_CHECKING:
    from scrabble.types import Player

WORD_LIST_PATH = Path(__file__).resolve().parent / "data" / "enable1.txt"

# A reasonable, generic starting point if the player does not supply their
# own tuned weights: value raw score, penalise a heavy rack leave, prefer a
# balanced rack, and avoid opening premium squares for the opponent.
DEFAULT_WEIGHTS = [1.0, -1.0, 1.0, -1.0, -1.0, 0.0]


def _load_weights(path_text: str) -> list[float]:
    """Load six whitespace- or comma-separated weights from a text file."""
    text = Path(path_text).read_text(encoding="utf-8")
    parts = text.replace(",", " ").split()
    weights = [float(p) for p in parts]

    if len(weights) != 6:
        raise ValueError("a weights file must contain exactly six numbers")

    return weights


def choose_opponent(lexicon: Lexicon) -> Player:
    """Ask the player which AI to play against, and build it.

    Re-prompts on anything other than "1" or "2". Choosing the weighted AI
    ("2") asks for an optional path to a weights file; a blank answer, a
    missing file, or a file that doesn't contain exactly six numbers all
    fall back to `DEFAULT_WEIGHTS` rather than crashing the program.
    """
    while True:
        print("Choose your opponent:")
        print("  1. Greedy AI")
        print("  2. Weighted AI")
        choice = input("> ").strip()

        if choice == "1":
            return GreedyPlayer(lexicon, "Greedy")

        if choice == "2":
            path_text = input(
                "Path to a weights file (leave blank for default weights): "
            ).strip()

            weights = DEFAULT_WEIGHTS

            if path_text:
                try:
                    weights = _load_weights(path_text)
                except (OSError, ValueError) as exc:
                    print(f"Could not load weights ({exc}); using default weights.")
                    weights = DEFAULT_WEIGHTS

            return WeightedPlayer(weights, lexicon, "Weighted")

        print("Please enter 1 or 2.")


def _play(human: Player, ai: Player, lexicon: Lexicon) -> None:
    """Run one complete human-vs-AI game, printing progress as it goes."""
    seed = random.randint(0, 2**31 - 1)
    state = new_game(seed, n_players=2)
    players = [human, ai]
    human_idx = 0

    while not is_over(state):
        current = players[state.turn]
        rack = state.racks[state.turn]
        move = current.choose_move(state, rack)

        ok, reason = validate(state.board, move, lexicon)

        if not ok:
            # Every Player implementation in this project only offers
            # validated moves (HumanPlayer re-prompts until one passes
            # validate(); the AI players only ever propose moves straight
            # out of the move generator). This is a last-resort guard so a
            # misbehaving Player cannot crash someone else's terminal game.
            print(f"{current.name} offered an illegal move ({reason}); passing instead.")
            move = Move(kind="pass")

        apply_move(state, move)

        if move.kind == "play":
            print(f"{current.name} played {' '.join(move.words)} for {move.score} points.")
        elif move.kind == "exchange":
            print(f"{current.name} exchanged {len(move.exchanged)} tile(s).")
        else:
            print(f"{current.name} passed.")

    show(state, human_idx)

    who_went_out = next(
        (i for i, rack in enumerate(state.racks) if len(rack.tiles) == 0), None
    )
    final_scores = end_game_adjust(state.scores, state.racks, who_went_out)

    print()
    print("Game over!")
    for player, score in zip(players, final_scores):
        print(f"  {player.name}: {score}")

    if final_scores[0] > final_scores[1]:
        print(f"{human.name} wins!")
    elif final_scores[1] > final_scores[0]:
        print(f"{ai.name} wins!")
    else:
        print("It's a tie!")


def main() -> None:
    """Entry point: load the word list, pick an opponent, and play."""
    if not WORD_LIST_PATH.exists():
        print(f"Word list not found at {WORD_LIST_PATH}. Cannot start a game.")
        sys.exit(1)

    lexicon = Lexicon()
    lexicon.load(str(WORD_LIST_PATH))

    human = HumanPlayer(lexicon, "You")
    ai = choose_opponent(lexicon)

    _play(human, ai, lexicon)


if __name__ == "__main__":
    main()
