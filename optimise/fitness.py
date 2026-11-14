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
    global CALLS
    CALLS = 0


def _get_lexicon() -> Lexicon:
    global _lexicon_cache

    if _lexicon_cache is None:
        lexicon = Lexicon()
        lexicon.load(str(LEXICON_PATH))
        _lexicon_cache = lexicon

    return _lexicon_cache


def fitness(weights: list[float], n_games: int = 4, seed: int = 0) -> float:
    global CALLS

    if n_games < 1:
        raise ValueError("n_games must be at least 1")

    lexicon = _get_lexicon()
    tuned = WeightedPlayer(list(weights), lexicon)
    greedy = GreedyPlayer(lexicon)

    total_margin = 0.0

    for i in range(n_games):
        game_seed = seed + i // 2
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