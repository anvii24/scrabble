"""Step 4 (lexicon and move generation): the word list stored as a dict trie."""

from __future__ import annotations


class Lexicon:
    """A trie of uppercase words.

    Attributes:
        root: nested dicts keyed by letter. A node containing the key "$" ends a
            valid word, e.g. {"A": {"T": {"$": True}}} holds just "AT".
    """

    def __init__(self) -> None:
        """Create an empty lexicon with root = {}."""
        raise NotImplementedError

    def load(self, path: str) -> None:
        """Add every word in a text file to the trie.

        Inputs:
            path: a UTF-8 file with one word per line.
        Rules:
            Words are stripped and uppercased. Blank lines are skipped, as are
            lines that are not purely A-Z (headers, comments).
        Edge cases:
            Raises FileNotFoundError if `path` is missing. Calling load twice
            merges the files.
        """
        raise NotImplementedError

    def is_word(self, s: str) -> bool:
        """Return True if `s` is a complete word, ignoring case.

        Edge cases:
            The empty string is not a word. A prefix such as "CA" of "CAT" is
            False unless "CA" is itself a word.
        """
        raise NotImplementedError

    def has_prefix(self, s: str) -> bool:
        """Return True if some word starts with `s`, ignoring case.

        Edge cases:
            A complete word counts as its own prefix. The empty string is True
            for a non-empty lexicon.
        """
        raise NotImplementedError

    def child(self, node: dict, letter: str) -> dict | None:
        """Return `node`'s child for `letter`, or None if there is none.

        Inputs:
            node: a trie node, starting from `root`.
            letter: a single uppercase letter.
        Rules:
            This is the hot path for movegen, so it does a plain lookup with no
            case normalisation.
        Edge cases:
            Passing "$" must return None: it is the end marker, not a letter.
        """
        raise NotImplementedError
