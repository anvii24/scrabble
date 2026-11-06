from __future__ import annotations

import random
import time

from optimise.common import BOUNDS, N_WEIGHTS, Result, random_weights


def clamp(value):
    return max(BOUNDS[0], min(BOUNDS[1], value))


class Evaluator:
    def __init__(self, fitness_fn, budget):
        self.fitness_fn = fitness_fn
        self.budget = budget
        self.calls = 0
        self.best_weights = None
        self.best_fitness = float("-inf")
        self.history = []

    def done(self):
        return self.calls >= self.budget

    def score(self, weights):
        value = self.fitness_fn(weights)
        self.calls += 1
        if value > self.best_fitness:
            self.best_fitness = value
            self.best_weights = list(weights)
        self.history.append(self.best_fitness)
        return value


def tournament(population, scores, k, rng):
    picks = rng.sample(range(len(population)), k)
    best = max(picks, key=lambda i: scores[i])
    return population[best]


def crossover(parent_a, parent_b, p_cross, rng):
    if rng.random() > p_cross:
        return list(parent_a), list(parent_b)
    point = rng.randint(1, N_WEIGHTS - 1)
    child_a = parent_a[:point] + parent_b[point:]
    child_b = parent_b[:point] + parent_a[point:]
    return child_a, child_b


def mutate(weights, p_mut, rng, sd=0.5):
    child = list(weights)
    for i in range(1, N_WEIGHTS):
        if rng.random() < p_mut:
            child[i] = clamp(child[i] + rng.gauss(0, sd))
    child[0] = 1.0
    return child


def run(budget=100, seed=0, pop_size=10, tour_k=3, p_cross=0.8, p_mut=0.1, elite=2, fitness_fn=None):
    if fitness_fn is None:
        from optimise.fitness import fitness
        fitness_fn = lambda w: fitness(w, seed=seed)
    rng = random.Random(seed)
    start = time.time()
    evaluator = Evaluator(fitness_fn, budget)
    population = [random_weights(rng) for _ in range(pop_size)]
    best_per_gen = []
    avg_per_gen = []
    while not evaluator.done():
        scores = []
        for weights in population:
            if evaluator.done():
                break
            scores.append(evaluator.score(weights))
        if len(scores) < len(population):
            break
        best_per_gen.append(max(scores))
        avg_per_gen.append(sum(scores) / len(scores))
        ranked = sorted(range(len(population)), key=lambda i: scores[i], reverse=True)
        next_population = [list(population[i]) for i in ranked[:elite]]
        while len(next_population) < pop_size:
            parent_a = tournament(population, scores, tour_k, rng)
            parent_b = tournament(population, scores, tour_k, rng)
            child_a, child_b = crossover(parent_a, parent_b, p_cross, rng)
            next_population.append(mutate(child_a, p_mut, rng))
            if len(next_population) < pop_size:
                next_population.append(mutate(child_b, p_mut, rng))
        population = next_population
    return Result(
        technique="genetic",
        best_weights=evaluator.best_weights,
        best_fitness=evaluator.best_fitness,
        history=evaluator.history,
        runtime_s=time.time() - start,
        seed=seed,
        extra={"best_per_gen": best_per_gen, "avg_per_gen": avg_per_gen},
    )