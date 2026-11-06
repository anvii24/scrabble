import os
import time

from scrabble.constants import LETTER_POINTS, SIZE
from scrabble.movegen import brute_force_moves, generate_moves
from scrabble.types import Tile

WORDS = ["AT", "TA", "CAT", "ACT", "TAC", "AS", "SAT", "CATS", "ACTS", "SCAT", "TO", "OAT",
         "COAT", "COATS", "TACO", "TACOS", "OF", "FA", "OX", "AX", "TAX", "DOG", "GOD",
         "GO", "DO", "OD", "AD", "ADS"]


class FakeBoard:
    def __init__(self):
        self.grid = [[None] * SIZE for _ in range(SIZE)]

    def get(self, row, col):
        return self.grid[row][col]

    def put(self, row, col, word, across=True):
        for letter in word:
            self.grid[row][col] = Tile(letter, LETTER_POINTS[letter])
            if across:
                col += 1
            else:
                row += 1


class FakeLexicon:
    def __init__(self, words):
        self.root = {}
        for word in words:
            node = self.root
            for letter in word:
                node = node.setdefault(letter, {})
            node["$"] = True


def make_rack(letters):
    return [Tile("?", 0, True) if l == "?" else Tile(l, LETTER_POINTS[l]) for l in letters]


def keys(moves):
    return {tuple(sorted((p.row, p.col, p.tile.letter, p.tile.is_blank) for p in m.placements)) for m in moves}


def check_same(board, letters):
    lexicon = FakeLexicon(WORDS)
    rack = make_rack(letters)
    fast = keys(generate_moves(board, rack, lexicon))
    slow = keys(brute_force_moves(board, rack, lexicon))
    assert fast == slow
    return fast


def test_empty_board():
    moves = check_same(FakeBoard(), "CATS")
    assert len(moves) > 0


def test_one_word_on_board():
    board = FakeBoard()
    board.put(7, 6, "CAT")
    check_same(board, "OSD")


def test_word_going_down():
    board = FakeBoard()
    board.put(5, 7, "DOG", across=False)
    check_same(board, "ATS")


def test_two_words():
    board = FakeBoard()
    board.put(7, 5, "COAT")
    board.put(5, 8, "TAX", across=False)
    check_same(board, "ASO")


def test_blank():
    board = FakeBoard()
    board.put(7, 7, "AT")
    check_same(board, "?S")


def test_speed_with_real_words():
    path = os.path.join("data", "enable1.txt")
    if not os.path.exists(path):
        return
    with open(path) as f:
        words = [w.strip().upper() for w in f if 2 <= len(w.strip()) <= 15]
    lexicon = FakeLexicon(words)
    board = FakeBoard()
    board.put(7, 5, "SCRABBLE")
    start = time.time()
    generate_moves(board, make_rack("AEINRST"), lexicon)
    assert time.time() - start < 1