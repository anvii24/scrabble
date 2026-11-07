"""Step 7: shared fitness function.

NOTE (integration fix, not part of tasks 11/13): this module was still an
unimplemented stub (`raise NotImplementedError`) and its `LEXICON_PATH`
pointed at `data/words.txt`, a file that does not exist anywhere in the
repository -- the actual word list that ships with the project is
`data/enable1.txt` (see `tests/test_movegen.py`). Every optimisation
technique, including simulated annealing (task 11), calls `fitness()`, so
the project could not run end to end without this module working. Per the
brief's instruction to propose the smallest necessary fix for another
module rather than silently redesigning it, this is a minimal, literal
implementation of the documented interface: play `n_games` games of the
candidate `WeightedPlayer` against a `GreedyPlayer`, alternating who moves
first, and return the average margin. This should be reviewed by whoever
owns `optimise/fitness.py`.
"""

from __future__ import annotations

from pathlib import Path

from scrabble.evaluation import WeightedPlayer
from scrabble.game import play_game
from scrabble.lexicon import Lexicon
from scrabble.players import GreedyPlayer

LEXICON_PATH = Path(__file__).resolve().parent.parent / "data" / "enable1.txt"

CALLS = 0

_lexicon_cache: Lexicon | None = None


def reset_calls() -> None:
    """Zero the shared fitness-call counter.

    Optimisation techniques call this once at the start of a `run()` so
    that `CALLS` (and, by extension, their fitness-call budget) is
    measured from a clean slate.
    """
    global CALLS
    CALLS = 0


def _get_lexicon() -> Lexicon:
    """Load and cache the word list used to validate and score moves."""
    global _lexicon_cache

    if _lexicon_cache is None:
        lexicon = Lexicon()
        lexicon.load(str(LEXICON_PATH))
        _lexicon_cache = lexicon

    return _lexicon_cache


def fitness(weights: list[float], n_games: int = 6, seed: int = 0) -> float:
    """Score a weight vector by playing it against the greedy baseline.

    Plays `n_games` complete games of a `WeightedPlayer` using `weights`
    against a `GreedyPlayer`, alternating which of the two moves first, and
    returns the average margin (the weighted player's final score minus
    the greedy player's) across those games. A positive value means the
    weighted player outperformed greedy on average.

    Args:
        weights: the six evaluation weights to test.
        n_games: how many games to play. Must be at least 1.
        seed: base seed. Game ``i`` (0-indexed) is dealt with
            `scrabble.game.new_game`'s seed set to ``seed + i``, so calling
            `fitness` again with the same `weights`, `n_games` and `seed`
            reproduces exactly the same games.

    Returns:
        The average score margin across the `n_games` games.

    Raises:
        ValueError: if `n_games` is less than 1.
    """
    global CALLS

    if n_games < 1:
        raise ValueError("n_games must be at least 1")

    lexicon = _get_lexicon()
    tuned = WeightedPlayer(list(weights), lexicon)
    greedy = GreedyPlayer(lexicon)

    total_margin = 0.0

    for i in range(n_games):
        game_seed = seed + i
        tuned_moves_first = i % 2 == 0

        if tuned_moves_first:
            outcome = play_game(tuned, greedy, game_seed, lexicon)
            margin = outcome["scores"][0] - outcome["scores"][1]
        else:
            outcome = play_game(greedy, tuned, game_seed, lexicon)
            margin = outcome["scores"][1] - outcome["scores"][0]

        total_margin += margin

    CALLS += 1

    return total_margin / n_games
