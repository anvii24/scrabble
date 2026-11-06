from __future__ import annotations


class Lexicon:
    def __init__(self) -> None:
        raise NotImplementedError

    def load(self, path: str) -> None:
        raise NotImplementedError

    def is_word(self, s: str) -> bool:
        raise NotImplementedError

    def has_prefix(self, s: str) -> bool:
        raise NotImplementedError

    def child(self, node: dict, letter: str) -> dict | None:
        raise NotImplementedError
