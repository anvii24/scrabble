# Scrabble AI

A two-player Scrabble game in Python. The AI picks its move with a weighted
evaluation function over six features (move score, rack leave, vowel balance,
triple-word squares opened, double-word squares opened, tiles left in the bag).
The six weights are tuned with four search techniques and compared against a
greedy player that always takes the highest-scoring move:

- Hill climbing
- Tabu search
- Simulated annealing
- Genetic algorithm

Moves are generated with anchors, cross-checks and a depth-first search over a
trie of the ENABLE word list (`data/enable1.txt`).

## Setup

Requires Python 3.10 or newer.

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (macOS/Linux)
pip install -r requirements.txt
```

## Running

Run everything from the project root.

Play against the AI:

```
python main.py
```

Run the experiments and build the charts:

```
python -m experiments.run_all --seeds 2 --budget 60
python -m experiments.plots
```

`--tech` can be `hill_climb`, `tabu`, `annealing`, `genetic` or `all` (default).
Results go to `experiments/results/`.

Run the tests:

```
python -m pytest
```

## Results

Each technique had 60 fitness evaluations (4 games against greedy each) and
started from the greedy weights. The best weights were then tested on 50 new
games against greedy (mean over 2 seeds).

| Technique | Win rate vs greedy | Avg margin |
| --- | --- | --- |
| Hill climbing | 51% | +1.2 |
| Tabu search | 54% | +8.5 |
| Simulated annealing | 53% | +7.6 |
| Genetic algorithm | 39% | -40.8 |

Charts: `experiments/results/convergence.png` and `experiments/results/winrate.png`.

## Project structure

| Folder | Contents |
| --- | --- |
| `scrabble/` | Board, tiles, rules, scoring, word list, move generator, players, game loop, terminal UI |
| `optimise/` | Fitness function and the four search techniques |
| `experiments/` | Experiment runner, plots and results |
| `tests/` | Tests |
