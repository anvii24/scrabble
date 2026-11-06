from __future__ import annotations

from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def plot_convergence(results_dir: Path = RESULTS_DIR) -> Path:
    raise NotImplementedError


def plot_winrate(results_dir: Path = RESULTS_DIR) -> Path:
    raise NotImplementedError


def write_results_table(results_dir: Path = RESULTS_DIR) -> Path:
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
