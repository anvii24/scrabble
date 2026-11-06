from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from optimise.common import Result

RESULTS_DIR = Path(__file__).resolve().parent / "results"
TECHNIQUES = ("hill_climb", "tabu", "annealing", "genetic")
EVAL_SEEDS = range(1000, 1050)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    raise NotImplementedError


def save_history(result: Result) -> Path:
    raise NotImplementedError


def evaluate_weights(weights: list[float]) -> tuple[float, float]:
    raise NotImplementedError


def append_summary(result: Result, win_rate: float, avg_margin: float) -> None:
    raise NotImplementedError


def main(argv: list[str] | None = None) -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
