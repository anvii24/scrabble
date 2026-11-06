from __future__ import annotations

import argparse
import csv
import importlib
from pathlib import Path
from typing import TYPE_CHECKING

from optimise import fitness as fitness_module
from scrabble.evaluation import WeightedPlayer
from scrabble.game import play_game
from scrabble.lexicon import Lexicon
from scrabble.players import GreedyPlayer

if TYPE_CHECKING:
    from optimise.common import Result

RESULTS_DIR = Path(__file__).resolve().parent / "results"
TECHNIQUES = ("hill_climb", "tabu", "annealing", "genetic")
EVAL_SEEDS = range(1000, 1050)
SUMMARY_COLUMNS = [
    "technique", "seed", "best_fitness", "win_rate", "avg_margin",
    "runtime_s", "weights",
]

_LEXICON: Lexicon | None = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the optimisation experiments.")
    parser.add_argument(
        "--tech", default="all", choices=("all", *TECHNIQUES),
        help="technique to run (default: all four)",
    )
    parser.add_argument(
        "--seeds", type=int, default=3,
        help="number of seeds; runs seeds 0..N-1 (default: 3)",
    )
    parser.add_argument(
        "--budget", type=int, default=100,
        help="fitness calls per run (default: 100)",
    )
    args = parser.parse_args(argv)
    if args.seeds < 1:
        parser.error("--seeds must be at least 1")
    if args.budget < 1:
        parser.error("--budget must be at least 1")
    return args


def save_history(result: Result) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"history_{result.technique}_{result.seed}.csv"
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["call", "best_so_far"])
        for i, value in enumerate(result.history, start=1):
            writer.writerow([i, value])
    return path


def _get_lexicon() -> Lexicon:
    global _LEXICON
    if _LEXICON is None:
        _LEXICON = Lexicon()
        _LEXICON.load(str(fitness_module.LEXICON_PATH))
    return _LEXICON


def evaluate_weights(
    weights: list[float], lexicon: Lexicon | None = None
) -> tuple[float, float]:
    lexicon = lexicon or _get_lexicon()
    tuned = WeightedPlayer(list(weights), lexicon)
    greedy = GreedyPlayer(lexicon)
    wins = 0.0
    margins: list[float] = []
    for i, seed in enumerate(EVAL_SEEDS):
        tuned_first = i % 2 == 0
        if tuned_first:
            out = play_game(tuned, greedy, seed, lexicon)
            mine, theirs = out["scores"][0], out["scores"][1]
        else:
            out = play_game(greedy, tuned, seed, lexicon)
            mine, theirs = out["scores"][1], out["scores"][0]
        margin = mine - theirs
        margins.append(margin)
        wins += 1.0 if margin > 0 else 0.5 if margin == 0 else 0.0
    n = len(margins)
    return wins / n, sum(margins) / n


def append_summary(result: Result, win_rate: float, avg_margin: float) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / "summary.csv"
    rows: list[dict] = []
    if path.exists():
        with path.open(newline="") as f:
            rows = [
                r for r in csv.DictReader(f)
                if not (
                    r["technique"] == result.technique
                    and r["seed"] == str(result.seed)
                )
            ]
    rows.append({
        "technique": result.technique,
        "seed": result.seed,
        "best_fitness": result.best_fitness,
        "win_rate": win_rate,
        "avg_margin": avg_margin,
        "runtime_s": result.runtime_s,
        "weights": str([round(w, 4) for w in result.best_weights]),
    })
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _run_technique(tech: str, seed: int, budget: int) -> Result:
    module = importlib.import_module(f"optimise.{tech}")
    fitness_module.reset_calls()
    return module.run(budget=budget, seed=seed)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    techniques = TECHNIQUES if args.tech == "all" else (args.tech,)
    for tech in techniques:
        for seed in range(args.seeds):
            print(f"[{tech}] seed {seed}: optimising (budget {args.budget})...", flush=True)
            result = _run_technique(tech, seed, args.budget)
            save_history(result)
            win_rate, avg_margin = evaluate_weights(result.best_weights)
            append_summary(result, win_rate, avg_margin)
            print(
                f"[{tech}] seed {seed}: fitness {result.best_fitness:.2f}, "
                f"win rate {win_rate:.0%}, avg margin {avg_margin:+.1f}",
                flush=True,
            )


if __name__ == "__main__":
    main()
