"""Step 8 (experiments): turn the CSV results into figures and a table.

Run from the project root with `python -m experiments.plots`. matplotlib is
imported inside the functions that need it.
"""

from __future__ import annotations

from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def plot_convergence(results_dir: Path = RESULTS_DIR) -> Path:
    """Write convergence.png and return its path.

    Inputs:
        results_dir: folder holding the history_<tech>_<seed>.csv files.
    Outputs:
        A line chart of best-so-far fitness against fitness calls, with one
        line per technique, averaged over its seeds.
    Edge cases:
        Runs may have different lengths, so average only up to the shortest
        history of that technique. Technique names contain underscores, so
        parse filenames by splitting off the seed from the right. Raises
        FileNotFoundError if there are no history files.
    """
    raise NotImplementedError


def plot_winrate(results_dir: Path = RESULTS_DIR) -> Path:
    """Write winrate.png and return its path.

    Inputs:
        results_dir: folder holding summary.csv.
    Outputs:
        A bar chart of mean win rate against greedy per technique, with error
        bars for the standard deviation across seeds and a reference line at
        0.5.
    Edge cases:
        A technique with a single seed has no standard deviation; draw it with
        no error bar. Raises FileNotFoundError if summary.csv is missing.
    """
    raise NotImplementedError


def write_results_table(results_dir: Path = RESULTS_DIR) -> Path:
    """Write results_table.md and return its path.

    Inputs:
        results_dir: folder holding summary.csv.
    Outputs:
        A Markdown table with one row per technique: seeds run, mean and best
        best_fitness, mean win_rate, mean avg_margin and mean runtime_s.
    """
    raise NotImplementedError


def main() -> None:
    """Produce all three outputs."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
