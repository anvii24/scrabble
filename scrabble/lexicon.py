from __future__ import annotations


class Lexicon:
    def __init__(self) -> None:
        self.root = {}

    def load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip().upper()

                if not word or not word.isalpha() or not word.isascii():
                    continue

                node = self.root

                for letter in word:
                    if letter not in node:
                        node[letter] = {}

                    node = node[letter]

                node["$"] = True

    def is_word(self, s: str) -> bool:
        if not s:
            return False

        node = self.root

        for letter in s.upper():
            node = self.child(node, letter)

            if node is None:
                return False

        return "$" in node

    def child(self, node: dict, letter: str) -> dict | None:
        if letter == "$":
            return None

        return node.get(letter)
