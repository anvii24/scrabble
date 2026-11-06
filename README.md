# Scrabble

A two-player Scrabble game whose AI picks moves
with a weighted evaluation function. The weights are tuned by four techniques
(hill climbing, tabu search, simulated annealing and a genetic algorithm), and
the tuned players are compared against a greedy baseline that always takes the
highest-scoring move.

## Status

This is a project skeleton. `scrabble/types.py`, `scrabble/constants.py` and
`optimise/common.py` are implemented. Everything else is a documented stub that
raises `NotImplementedError`, and the planned tests are marked as skipped.

## Setup

Requires Python 3.10 or newer.

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (macOS/Linux)
pip install -r requirements.txt
```

Put a word list at `data/words.txt`, with one word per line. It is not included.

## Running

Run everything from the project root. Do not run files inside `scrabble/`
directly: that puts `scrabble/` on the import path, where `scrabble/types.py`
hides Python's own `types` module.

Play the game:

```
python main.py
```

Run the experiments, then build the plots and the results table:

```
python -m experiments.run_all --tech all --seeds 5 --budget 100
python -m experiments.plots
```

`--tech` is `hill_climb`, `tabu`, `annealing`, `genetic` or `all`. Output goes to
`experiments/results/`.

Run the tests:

```
pytest
```

## Build order

Each module's docstring names the step it belongs to.

| Step | Topic | Files |
| --- | --- | --- |
| 1 | Foundations | `scrabble/types.py`, `scrabble/constants.py` |
| 2 | Board and tiles | `scrabble/board.py`, `bag.py`, `rack.py` |
| 3 | Rules and scoring | `scrabble/rules.py`, `scoring.py` |
| 4 | Lexicon and move generation | `scrabble/lexicon.py`, `movegen.py` |
| 5 | Players and evaluation | `scrabble/players.py`, `evaluation.py` |
| 6 | Game loop and UI | `scrabble/game.py`, `ui.py`, `main.py` |
| 7 | Optimisation | `optimise/common.py`, `fitness.py`, `hill_climb.py`, `tabu.py`, `annealing.py`, `genetic.py` |
| 8 | Experiments | `experiments/run_all.py`, `plots.py` |
