from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrabble.lexicon import Lexicon
    from scrabble.types import Player


def choose_opponent(lexicon: Lexicon) -> Player:
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
