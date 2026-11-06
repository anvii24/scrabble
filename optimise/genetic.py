from __future__ import annotations

from optimise.common import Result


def run(
    budget: int = 100,
    seed: int = 0,
    pop_size: int = 10,
    tour_k: int = 3,
    p_cross: float = 0.8,
    p_mut: float = 0.1,
    elite: int = 2,
) -> Result:
    raise NotImplementedError
