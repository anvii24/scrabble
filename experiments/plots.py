from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent / "results"
ORDER = ("hill_climb", "tabu", "annealing", "genetic")
LABELS = {
    "hill_climb": "Hill climbing",
    "tabu": "Tabu search",
    "annealing": "Simulated annealing",
    "genetic": "Genetic algorithm",
}


def _sorted_techniques(names) -> list[str]:
    names = set(names)
    return [t for t in ORDER if t in names] + sorted(names - set(ORDER))


def _load_histories(results_dir: Path) -> dict[str, list[list[float]]]:
    histories: dict[str, list[list[float]]] = defaultdict(list)
    for path in sorted(Path(results_dir).glob("history_*.csv")):
        stem = path.stem[len("history_"):]
        tech, _, seed = stem.rpartition("_")
        if not tech or not seed.isdigit():
            continue
        with path.open(newline="") as f:
            values = [float(r["best_so_far"]) for r in csv.DictReader(f)]
        if values:
            histories[tech].append(values)
    if not histories:
        raise FileNotFoundError(f"no history_*.csv files in {results_dir}")
    return histories


def _load_summary(results_dir: Path) -> dict[str, list[dict]]:
    path = Path(results_dir) / "summary.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing {path}")
    rows: dict[str, list[dict]] = defaultdict(list)
    with path.open(newline="") as f:
        for r in csv.DictReader(f):
            rows[r["technique"]].append(r)
    if not rows:
        raise FileNotFoundError(f"{path} has no rows")
    return rows


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return (sum((v - m) ** 2 for v in values) / (len(values) - 1)) ** 0.5


def _average_curve(histories: list[list[float]]) -> list[float]:
    length = max(len(h) for h in histories)
    padded = [h + [h[-1]] * (length - len(h)) for h in histories]
    return [_mean([h[i] for h in padded]) for i in range(length)]


def plot_convergence(results_dir: Path = RESULTS_DIR) -> Path:
    histories = _load_histories(results_dir)
    fig, ax = plt.subplots(figsize=(8, 5))
    for tech in _sorted_techniques(histories):
        curve = _average_curve(histories[tech])
        ax.plot(
            range(1, len(curve) + 1), curve,
            label=f"{LABELS.get(tech, tech)} (n={len(histories[tech])})",
        )
    ax.set_xlabel("Fitness calls")
    ax.set_ylabel("Best fitness so far (avg margin vs greedy)")
    ax.set_title("Convergence (averaged over seeds)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    out = Path(results_dir) / "convergence.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def plot_winrate(results_dir: Path = RESULTS_DIR) -> Path:
    rows = _load_summary(results_dir)
    techs = _sorted_techniques(rows)
    rates = {t: [float(r["win_rate"]) * 100 for r in rows[t]] for t in techs}
    means = [_mean(rates[t]) for t in techs]
    errs = [_std(rates[t]) for t in techs]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        [LABELS.get(t, t) for t in techs], means, yerr=errs, capsize=5,
    )
    ax.axhline(50, color="grey", linestyle="--", linewidth=1, label="Even with greedy")
    for bar, m in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, m + 1, f"{m:.0f}%",
                ha="center", va="bottom")
    ax.set_ylim(0, 105)
    ax.set_ylabel("Win rate vs greedy (%)")
    ax.set_title("Tuned player vs greedy (50 games per run; bars = mean, whiskers = std over seeds)")
    ax.title.set_fontsize(10)
    ax.legend()
    fig.tight_layout()
    out = Path(results_dir) / "winrate.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def write_results_table(results_dir: Path = RESULTS_DIR) -> Path:
    rows = _load_summary(results_dir)
    lines = [
        "| Technique | Seeds | Best fitness | Win rate vs greedy | Avg margin | Runtime (s) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for tech in _sorted_techniques(rows):
        rs = rows[tech]
        fit = [float(r["best_fitness"]) for r in rs]
        win = [float(r["win_rate"]) * 100 for r in rs]
        mar = [float(r["avg_margin"]) for r in rs]
        run = [float(r["runtime_s"]) for r in rs]
        lines.append(
            f"| {LABELS.get(tech, tech)} | {len(rs)} "
            f"| {_mean(fit):.2f} ± {_std(fit):.2f} "
            f"| {_mean(win):.1f}% ± {_std(win):.1f} "
            f"| {_mean(mar):+.2f} ± {_std(mar):.2f} "
            f"| {_mean(run):.1f} |"
        )
    lines.append("")
    lines.append("Values are mean ± std over seeds.")
    out = Path(results_dir) / "results_table.md"
    out.write_text("\n".join(lines) + "\n")
    return out


def main() -> None:
    for fn in (plot_convergence, plot_winrate, write_results_table):
        print("wrote", fn())


if __name__ == "__main__":
    main()
