"""Step 8 (experiments): run every technique and record results as CSV files.

Run from the project root with `python -m experiments.run_all`.
"""

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
    """Parse the command line.

    Inputs:
        argv: arguments, or None for sys.argv.
    Outputs:
        A namespace with:
            tech: list of technique names. --tech takes one name from
                TECHNIQUES or "all", the default.
            seeds: list of ints. --seeds N means seeds 0..N-1, default 5.
            budget: int fitness calls per run. --budget defaults to 100.
    Edge cases:
        An unknown technique or a non-positive --seeds or --budget exits with
        an argparse error.
    """
    raise NotImplementedError


def save_history(result: Result) -> Path:
    """Write history_<tech>_<seed>.csv to RESULTS_DIR and return its path.

    Inputs:
        result: a finished run.
    Outputs:
        A CSV with header `call,best_fitness` and one row per history entry,
        call numbers starting from 1. An existing file is overwritten.
    """
    raise NotImplementedError


def evaluate_weights(weights: list[float]) -> tuple[float, float]:
    """Return (win_rate, avg_margin) for `weights` against GreedyPlayer.

    Inputs:
        weights: the tuned weights.
    Outputs:
        win_rate: wins / 50, with ties counting as non-wins.
        avg_margin: mean (my score - greedy score).
    Rules:
        Play one game per seed in EVAL_SEEDS, alternating who starts as in
        optimise.fitness. These seeds are disjoint from the fitness seeds, so
        this is a held-out estimate.
    """
    raise NotImplementedError


def append_summary(result: Result, win_rate: float, avg_margin: float) -> None:
    """Append one row to RESULTS_DIR / "summary.csv".

    Rules:
        Columns: technique, seed, best_fitness, win_rate, avg_margin, runtime_s,
        weights. `weights` is a JSON list in one cell, so the csv module must do
        the quoting. Write the header only when creating the file.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> None:
    """Run the experiment.

    Rules:
        For each technique and seed, in that order: import the technique's
        module, call run(seed=seed, budget=budget), save_history,
        evaluate_weights on best_weights, then append_summary. Writing after
        each run means an interrupted experiment keeps its finished results.
    Edge cases:
        Creates RESULTS_DIR if missing. Re-running appends to summary.csv, so
        delete it first to start clean.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
