"""Step 6 (game loop and UI): the text interface for a human player."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scrabble.types import GameState, Move, Player

if TYPE_CHECKING:
    from scrabble.board import Board
    from scrabble.lexicon import Lexicon
    from scrabble.rack import Rack


def show(state: GameState, player_idx: int) -> None:
    """Print the game from one player's point of view.

    Inputs:
        state: the current game.
        player_idx: whose rack to show.
    Outputs:
        Prints the board, all scores, tiles left in the bag and this player's
        rack. Returns None.
    Rules:
        Never print the other player's rack.
    """
    raise NotImplementedError


def parse_move(text: str, board: Board, rack: Rack) -> Move:
    """Turn a typed command into a Move.

    Inputs:
        text: one of "H8 across WORD", "H8 down WORD", "exchange AEI", "pass".
        board: the current position, needed to skip tiles already on it.
        rack: the player's rack, used to resolve tiles.
    Outputs:
        A Move with kind 'play', 'exchange' or 'pass'. Its score and words are
        left unset, because legality has not been checked yet.
    Rules:
        H8 means column H (A-O) and row 8 (1-15), so H8 is (row 7, col 7) and
        A1 is (0, 0). Keywords and coordinates ignore case, but WORD does not:
        a lowercase letter is played with a blank, so "QuIZ" uses a blank as U,
        giving Tile("U", 0, True). Letters of WORD over squares that already
        hold that letter produce no placement. In exchange, "?" names a blank.
    Edge cases:
        Raises ValueError with a readable message for malformed text, a bad
        coordinate, a word running off the board, a letter that conflicts with
        a tile on the board, or tiles the rack does not hold (counting
        duplicates). Dictionary and connection checks are left to rules.validate.
    """
    raise NotImplementedError


class HumanPlayer(Player):
    """A player who types moves at the terminal."""

    def __init__(self, lexicon: Lexicon, name: str = "Human") -> None:
        """Store the lexicon and name.

        Inputs:
            lexicon: used to validate typed moves before they are played.
            name: display name.
        """
        raise NotImplementedError

    def choose_move(self, state: GameState, rack: Rack) -> Move:
        """Prompt until a legal move is entered and return it.

        Inputs:
            state: the current position.
            rack: this player's rack.
        Outputs:
            A legal Move with score and words filled in.
        Rules:
            Loop: show the game, read a line, parse_move, rules.validate, and
            for a play set move.score with scoring.score_move and move.words
            from rules.words_formed.
        Edge cases:
            On ValueError or an invalid move, print the reason and prompt again
            rather than ending the game. EOF or Ctrl-C propagates to the caller.
        """
        raise NotImplementedError
