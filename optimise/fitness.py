"""Step 7 (optimisation): the fitness function all four techniques share."""

from __future__ import annotations

from pathlib import Path

LEXICON_PATH = Path(__file__).resolve().parent.parent / "data" / "words.txt"

# Read this as `fitness_module.CALLS`. `from optimise.fitness import CALLS`
# copies the int and will never see it change.
CALLS = 0


def reset_calls() -> None:
    """Set CALLS back to 0. Each technique calls this at the start of run()."""
    raise NotImplementedError


def fitness(weights: list[float], n_games: int = 6, seed: int = 0) -> float:
    """Return how far WeightedPlayer(weights) beats GreedyPlayer on average.

    Inputs:
        weights: a weight vector of length 6, index 0 fixed at 1.0.
        n_games: number of games to play.
        seed: game seeds used are seed .. seed + n_games - 1.
    Outputs:
        The mean of (my score - opponent score) over the games. Positive means
        the weights beat greedy.
    Rules:
        Alternate who starts: even-offset games have WeightedPlayer as p1, odd
        ones have it as p2, and the score difference must be taken from the
        correct side of play_game's "scores". Adds 1 to CALLS per call, however
        many games n_games is. CALLS is the budget unit for every technique.
        Deterministic: the same arguments always give the same value.
    Edge cases:
        The lexicon is loaded once from LEXICON_PATH on first use and cached at
        module level, since loading it per call would dominate the runtime.
        Raises ValueError if n_games < 1.
    """
    raise NotImplementedError
