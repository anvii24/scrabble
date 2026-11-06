from __future__ import annotations

from itertools import permutations

from scrabble.constants import CENTER, LETTER_POINTS, SIZE
from scrabble.types import Move, Placement, Tile

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ACROSS = (0, 1)
DOWN = (1, 0)
END = "$"


def in_bounds(row, col):
    return 0 <= row < SIZE and 0 <= col < SIZE


def is_filled(board, row, col):
    return in_bounds(row, col) and board.get(row, col) is not None


def board_is_empty(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board.get(row, col) is not None:
                return False
    return True


def is_word(lexicon, word):
    node = lexicon.root
    for letter in word:
        if letter not in node:
            return False
        node = node[letter]
    return END in node


def anchors(board):
    if board_is_empty(board):
        return [CENTER]
    result = []
    for row in range(SIZE):
        for col in range(SIZE):
            if board.get(row, col) is not None:
                continue
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if is_filled(board, row + dr, col + dc):
                    result.append((row, col))
                    break
    return result


def read_tiles(board, row, col, dr, dc):
    letters = ""
    row += dr
    col += dc
    while is_filled(board, row, col):
        letters += board.get(row, col).letter
        row += dr
        col += dc
    return letters


def cross_checks(board, lexicon, direction=ACROSS):
    dr, dc = direction[1], direction[0]
    checks = {}
    for row in range(SIZE):
        for col in range(SIZE):
            if board.get(row, col) is not None:
                continue
            before = read_tiles(board, row, col, -dr, -dc)[::-1]
            after = read_tiles(board, row, col, dr, dc)
            if before == "" and after == "":
                checks[(row, col)] = set(ALPHABET)
                continue
            allowed = set()
            for letter in ALPHABET:
                if is_word(lexicon, before + letter + after):
                    allowed.add(letter)
            checks[(row, col)] = allowed
    return checks


def make_tile(letter, is_blank):
    if is_blank:
        return Tile(letter, 0, True)
    return Tile(letter, LETTER_POINTS[letter], False)


def add_move(board, placements, word, found):
    key = tuple(sorted((p.row, p.col, p.tile.letter, p.tile.is_blank) for p in placements))
    if key in found:
        return
    move = Move("play", list(placements), [], 0, [word])
    move.score = safe_score(board, move)
    found[key] = move


def safe_score(board, move):
    try:
        from scrabble.scoring import score_move
        return score_move(board, move)
    except NotImplementedError:
        return 0


def extend(board, row, col, direction, node, word, rack, placements, checks, anchor, covered, found):
    dr, dc = direction
    if not in_bounds(row, col):
        if END in node and placements and covered:
            add_move(board, placements, word, found)
        return
    tile = board.get(row, col)
    if tile is not None:
        if tile.letter in node:
            extend(board, row + dr, col + dc, direction, node[tile.letter], word + tile.letter,
                   rack, placements, checks, anchor, covered, found)
        return
    if END in node and placements and covered:
        add_move(board, placements, word, found)
    if (row, col) == anchor:
        covered = True
    allowed = checks[(row, col)]
    tried = set()
    for i in range(len(rack)):
        letter = rack[i]
        if letter in tried:
            continue
        tried.add(letter)
        rest = rack[:i] + rack[i + 1:]
        if letter == "?":
            options = ALPHABET
        else:
            options = letter
        for choice in options:
            if choice not in node or choice not in allowed:
                continue
            placement = Placement(row, col, make_tile(choice, letter == "?"))
            extend(board, row + dr, col + dc, direction, node[choice], word + choice,
                   rest, placements + [placement], checks, anchor, covered, found)


def start_squares(board, anchor, direction, anchor_set):
    dr, dc = direction
    row, col = anchor
    if is_filled(board, row - dr, col - dc):
        while is_filled(board, row - dr, col - dc):
            row -= dr
            col -= dc
        return [(row, col)]
    starts = [(row, col)]
    while True:
        row -= dr
        col -= dc
        if not in_bounds(row, col) or (row, col) in anchor_set:
            break
        if is_filled(board, row - dr, col - dc):
            break
        starts.append((row, col))
        if len(starts) > 7:
            break
    return starts


def generate_moves(board, rack, lexicon):
    letters = "".join(tile.letter if not tile.is_blank else "?" for tile in rack_tiles(rack))
    found = {}
    anchor_list = anchors(board)
    anchor_set = set(anchor_list)
    for direction in [ACROSS, DOWN]:
        checks = cross_checks(board, lexicon, direction)
        for anchor in anchor_list:
            for row, col in start_squares(board, anchor, direction, anchor_set):
                extend(board, row, col, direction, lexicon.root, "", letters, [],
                       checks, anchor, False, found)
    return list(found.values())


def rack_tiles(rack):
    if hasattr(rack, "tiles"):
        return rack.tiles
    return rack


def word_through(board, new, row, col, dr, dc):
    while (row - dr, col - dc) in new or is_filled(board, row - dr, col - dc):
        row -= dr
        col -= dc
    word = ""
    while (row, col) in new or is_filled(board, row, col):
        if (row, col) in new:
            word += new[(row, col)]
        else:
            word += board.get(row, col).letter
        row += dr
        col += dc
    return word


def is_legal(board, placements, lexicon, direction):
    new = {(p.row, p.col): p.tile.letter for p in placements}
    dr, dc = direction
    first = placements[0]
    main = word_through(board, new, first.row, first.col, dr, dc)
    if len(main) < 2 or not is_word(lexicon, main):
        return None
    touches = len(main) > len(placements)
    for p in placements:
        cross = word_through(board, new, p.row, p.col, dc, dr)
        if len(cross) >= 2:
            touches = True
            if not is_word(lexicon, cross):
                return None
    if board_is_empty(board):
        if CENTER not in new:
            return None
    elif not touches:
        return None
    return main


def brute_force_moves(board, rack, lexicon):
    letters = "".join(tile.letter if not tile.is_blank else "?" for tile in rack_tiles(rack))
    found = {}
    for size in range(1, len(letters) + 1):
        for combo in set(permutations(letters, size)):
            for choice in expand_blanks(combo):
                for direction in [ACROSS, DOWN]:
                    for row in range(SIZE):
                        for col in range(SIZE):
                            placements = lay_out(board, row, col, direction, choice, combo)
                            if placements is None:
                                continue
                            word = is_legal(board, placements, lexicon, direction)
                            if word:
                                add_move(board, placements, word, found)
    return list(found.values())


def expand_blanks(combo):
    results = [""]
    for letter in combo:
        if letter == "?":
            results = [r + c for r in results for c in ALPHABET]
        else:
            results = [r + letter for r in results]
    return results


def lay_out(board, row, col, direction, word, original):
    dr, dc = direction
    if not in_bounds(row, col) or is_filled(board, row, col):
        return None
    placements = []
    for i in range(len(word)):
        while is_filled(board, row, col):
            row += dr
            col += dc
        if not in_bounds(row, col):
            return None
        placements.append(Placement(row, col, make_tile(word[i], original[i] == "?")))
        row += dr
        col += dc
    return placements