from __future__ import annotations

from pathlib import Path

LEXICON_PATH = Path(__file__).resolve().parent.parent / "data" / "words.txt"

CALLS = 0


def reset_calls() -> None:
    raise NotImplementedError


def fitness(weights: list[float], n_games: int = 6, seed: int = 0) -> float:
    raise NotImplementedError
