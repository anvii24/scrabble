from __future__ import annotations

import csv

import pytest

from experiments import run_all
from optimise.common import Result


def make_result(tech="hill_climb", seed=0, history=(1.0, 2.0, 3.0)):
    return Result(
        technique=tech, best_weights=[1.0, 0.5, -1.25, 0.0, 2.0, 3.5],
        best_fitness=history[-1], history=list(history),
        runtime_s=1.5, seed=seed, extra={},
    )


@pytest.fixture
def results_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(run_all, "RESULTS_DIR", tmp_path)
    return tmp_path


def test_parse_args_defaults():
    args = run_all.parse_args([])
    assert (args.tech, args.seeds, args.budget) == ("all", 3, 100)


def test_parse_args_rejects_unknown_technique():
    with pytest.raises(SystemExit):
        run_all.parse_args(["--tech", "nope"])


def test_save_history_format(results_dir):
    path = run_all.save_history(make_result("hill_climb", 2))
    assert path.name == "history_hill_climb_2.csv"
    rows = list(csv.reader(path.open()))
    assert rows[0] == ["call", "best_so_far"]
    assert rows[1:] == [["1", "1.0"], ["2", "2.0"], ["3", "3.0"]]


def test_append_summary_writes_header_once(results_dir):
    run_all.append_summary(make_result(seed=0), 0.6, 10.0)
    run_all.append_summary(make_result(seed=1), 0.4, -5.0)
    lines = (results_dir / "summary.csv").read_text().splitlines()
    assert sum(l.startswith("technique,") for l in lines) == 1
    assert len(lines) == 3


def test_append_summary_replaces_rerun(results_dir):
    run_all.append_summary(make_result(seed=0), 0.6, 10.0)
    run_all.append_summary(make_result(seed=0), 0.7, 12.0)
    rows = list(csv.DictReader((results_dir / "summary.csv").open()))
    assert len(rows) == 1 and rows[0]["win_rate"] == "0.7"


def test_append_summary_quotes_weights(results_dir):
    run_all.append_summary(make_result(), 0.5, 0.0)
    rows = list(csv.DictReader((results_dir / "summary.csv").open()))
    assert list(rows[0]) == run_all.SUMMARY_COLUMNS
    assert rows[0]["weights"] == "[1.0, 0.5, -1.25, 0.0, 2.0, 3.5]"


def test_evaluate_weights_plays_held_out_seeds(monkeypatch):
    seen = []

    class FakeWeighted:
        def __init__(self, weights, lexicon):
            self.weights = weights

    class FakeGreedy:
        def __init__(self, lexicon):
            pass

    def fake_play(p1, p2, seed, lexicon):
        seen.append((seed, isinstance(p1, FakeWeighted)))

        return {"scores": [110, 100] if isinstance(p1, FakeWeighted) else [100, 110]}

    monkeypatch.setattr(run_all, "WeightedPlayer", FakeWeighted)
    monkeypatch.setattr(run_all, "GreedyPlayer", FakeGreedy)
    monkeypatch.setattr(run_all, "play_game", fake_play)
    win_rate, margin = run_all.evaluate_weights([1.0] * 6, lexicon=object())
    assert [s for s, _ in seen] == list(range(1000, 1050))
    assert [first for _, first in seen[:4]] == [True, False, True, False]
    assert win_rate == 1.0 and margin == 10.0


def test_main_runs_each_technique_and_seed(results_dir, monkeypatch):
    calls = []

    def fake_run(tech, seed, budget):
        calls.append((tech, seed, budget))
        return make_result(tech, seed)

    monkeypatch.setattr(run_all, "_run_technique", fake_run)
    monkeypatch.setattr(run_all, "evaluate_weights", lambda w: (0.5, 1.0))
    run_all.main(["--seeds", "3"])
    assert calls == [(t, s, 100) for t in run_all.TECHNIQUES for s in range(3)]
    assert len(list(results_dir.glob("history_*.csv"))) == 12
    assert len(list(csv.DictReader((results_dir / "summary.csv").open()))) == 12


def test_main_single_technique(results_dir, monkeypatch):
    calls = []
    monkeypatch.setattr(
        run_all, "_run_technique",
        lambda t, s, b: calls.append(t) or make_result(t, s),
    )
    monkeypatch.setattr(run_all, "evaluate_weights", lambda w: (0.5, 1.0))
    run_all.main(["--tech", "genetic"])
    assert set(calls) == {"genetic"} and len(calls) == 3
