# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import re
import sys

from ..annotations import ANNOTATION_NAME_BLANK_MOVE, ANNOTATION_NAME_PIECE_MOVE, PutAnnotation
from ..default_setup import iterate_default_setup
from ..file_formats.fen import PIECE_OF_UPPER_LETTER, iterate_fen_tokens
from ..parties import BLACK, RED
from ..pieces import ADVISOR, CANNON, CHARIOT, ELEPHANT, HORSE, KING, PAWN, PutPiece

ALL_MOVES = "all"

START_PARTY_RED = "RED"
START_PARTY_BLACK = "BLACK"

_SETUP_EXTRACTOR = re.compile("SETUP\\{([^}]+)\\}", re.MULTILINE)
_MOVES_EXTRACTOR = re.compile("START\\{([^}]+)\\}END", re.MULTILINE)
_SINGLE_MOVE_EXTRACTOR = re.compile(
    "(?P<piece_code>[A-Za-z])(?P<former_column>[1-9+=-])(?P<operator>[.+-])(?P<argument>[1-9])"
)
_ITEM_ITERATOR = re.compile(
    "(?P<put_piece>[RHEAKCPrheakcp][a-i][0-9])|(?P<move_offset>MOVE [1-9][0-9]*)|(?P<start_party>RED|BLACK)"
)
_FEN_ELEMENT_PATERN = "[RHEAKCPNBrheakcpnb1-9]+"
_FEN_EXTRACTOR = re.compile(
    f"^FEN[ \\t]+(?P<field_state>{_FEN_ELEMENT_PATERN}(?:/{_FEN_ELEMENT_PATERN}){{9}})( (?P<starting_party>[rb]))?",
    re.MULTILINE,
)

_UPPER_PIECE, _MIDDLE_PIECE, _LOWER_PIECE, _SINGLE_PIECE = range(4)


class _PlayerRelativeView:
    """
    This class translates from Chinese human coordinates
    as used in WXF notation into internal array coordinates.
    Positions are 1-based and a relative to the point of view
    of the moving player.
    Also note that the Chinese notation does not define
    whether the lowest row is 1 or 0 — it can do without
    it because only distances of rows travelled are used,
    not absolute row locations.

    For a more visual description of the three involved
    systems:

    Target system:
    Internal array coordinates
    (0, 9) . . . . . . . (8, 9)  # black player home base
       .   . . . . . . .   .
       .   . . . . . . .   .
       .   . . . . . . .   .
       .   . . . . . . .   .
    ---------------------------  # river
       .   . . . . . . .   .
       .   . . . . . . .   .
       .   . . . . . . .   .
       .   . . . . . . .   .
    (0, 0) . . . . . . . (8, 0)  # red player home base

    Source system for red player:
    (9, ?+9) . . . . . . . (1, ?+9)  # black player home base
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
    -------------------------------  # river
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
    (9, ?+0) . . . . . . . (1, ?+0)  # red player home base

    Source system for black player:
    (1, ?+0) . . . . . . . (9, ?+0)  # black player home base
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
    -------------------------------  # river
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
       .     . . . . . . .     .
    (1, ?+9) . . . . . . . (9, ?+9)  # red player home base
    """

    def __init__(self, party):
        self._party = party

    def x_index_from(self, x: int) -> int:
        if self._party == RED:
            return 9 - x
        else:
            return x - 1

    def y_diff_from(self, y: int) -> int:
        return y if self._party == RED else -y

    def further_up_the_board_sort_key(self, put_piece: PutPiece):
        return self.y_diff_from(put_piece.y)


class _Board:
    def __init__(self):
        self._board = [[None for _column in range(9)] for _row in range(10)]
        self._move_locations = set()

    def put(self, piece: PutPiece):
        self._board[piece.y][piece.x] = piece

    @staticmethod
    def _calculate_destination_of_move(put_piece: PutPiece, operator: str, argument: str):
        argument = int(argument)
        view = _PlayerRelativeView(put_piece.party)

        if put_piece.piece in (CHARIOT, KING, CANNON, PAWN):
            if operator == "+":
                new_x, new_y = put_piece.x, put_piece.y + view.y_diff_from(argument)
            elif operator == "-":
                new_x, new_y = put_piece.x, put_piece.y - view.y_diff_from(argument)
            else:
                assert operator == "."
                new_x, new_y = view.x_index_from(argument), put_piece.y
        elif put_piece.piece in (ADVISOR, ELEPHANT):
            diff_y = {
                ADVISOR: 1,
                ELEPHANT: 2,
            }[put_piece.piece]

            new_x = view.x_index_from(argument)
            if operator == "+":
                new_y = put_piece.y + view.y_diff_from(diff_y)
            elif operator == "-":
                new_y = put_piece.y - view.y_diff_from(diff_y)
            else:
                raise ValueError(f"Bad operator: {operator!r}")
        else:
            assert put_piece.piece == HORSE
            new_x = view.x_index_from(argument)
            diff_x = abs(put_piece.x - new_x)
            diff_y = 1 if diff_x == 2 else 2
            if operator == "+":
                new_y = put_piece.y + view.y_diff_from(diff_y)
            elif operator == "-":
                new_y = put_piece.y - view.y_diff_from(diff_y)
            else:
                raise ValueError(f"Bad operator: {operator!r}")

        return new_x, new_y

    def _locate_piece(self, party: int, piece_code: str, former_column: str):
        piece_type = PIECE_OF_UPPER_LETTER[piece_code.upper()]
        view = _PlayerRelativeView(party)

        if former_column in ("+", "=", "-"):  # with two pieces on same column/file
            if former_column == "+":
                look_for = _UPPER_PIECE
            elif former_column == "=":
                look_for = _MIDDLE_PIECE
            else:
                assert former_column == "-"
                look_for = _LOWER_PIECE
                piece_x = None
        else:
            assert former_column in (str(i) for i in range(1, 9 + 1))
            look_for = _SINGLE_PIECE
            piece_x = view.x_index_from(int(former_column))

        candidates = []
        for y, row in enumerate(self._board):
            for x, field in enumerate(row):
                if (
                    field is None
                    or (look_for == _SINGLE_PIECE and x != piece_x)
                    or field.piece != piece_type
                    or field.party != party
                ):
                    continue
                candidates.append(field)

        if look_for == _UPPER_PIECE:
            assert len(candidates) in (2, 3)
            put_piece = sorted(candidates, key=view.further_up_the_board_sort_key)[-1]
        elif look_for == _MIDDLE_PIECE:
            assert len(candidates) == 3
            put_piece = sorted(candidates, key=view.further_up_the_board_sort_key)[1]
        elif look_for == _LOWER_PIECE:
            assert len(candidates) in (2, 3)
            put_piece = sorted(candidates, key=view.further_up_the_board_sort_key)[0]
        else:
            assert look_for == _SINGLE_PIECE
            assert len(candidates) == 1
            put_piece = candidates[0]

        return put_piece

    def move(
        self,
        party: int,
        piece_code: str,
        former_column: str,
        operator: str,
        argument: str,
        annotate: bool,
    ):
        put_piece = self._locate_piece(party, piece_code, former_column)

        new_x, new_y = self._calculate_destination_of_move(put_piece, operator, argument)

        self._board[put_piece.y][put_piece.x] = None
        self._board[new_y][new_x] = put_piece

        if annotate:
            self._move_locations.add((put_piece.x, put_piece.y))
            self._move_locations.add((new_x, new_y))

        put_piece.x = new_x
        put_piece.y = new_y

    def iterate_tokens(self):
        for row in self._board:
            for piece in row:
                if piece is None:
                    continue
                yield piece

        for move_location in self._move_locations:
            x, y = move_location
            location_blank = self._board[y][x] is None
            annotation_name = (
                ANNOTATION_NAME_BLANK_MOVE if location_blank else ANNOTATION_NAME_PIECE_MOVE
            )
            yield PutAnnotation(annotation_name, x, y)


def iterate_wxf_tokens(content: str, moves_to_play: str, annotate_last_move: bool):
    board = _Board()

    fen_match = _FEN_EXTRACTOR.search(content)
    if fen_match:
        field_state_raw = fen_match.groupdict()["field_state"]
        starting_party = RED if fen_match.groupdict()["starting_party"] != "b" else BLACK
        for put_piece in iterate_fen_tokens(field_state_raw):
            board.put(put_piece)
    else:
        starting_party = RED  # TODO
        setup_match = _SETUP_EXTRACTOR.search(content)
        if setup_match:
            setup_body = setup_match.group(1)
            for item_match in re.finditer(_ITEM_ITERATOR, setup_body):
                gd = item_match.groupdict()
                if gd["put_piece"]:
                    piece_letter, x_lower_alpha, y_0_9 = gd["put_piece"]

                    party = BLACK if piece_letter.islower() else RED
                    piece = PIECE_OF_UPPER_LETTER[piece_letter.upper()]
                    x = ord(x_lower_alpha) - ord("a")
                    y = int(y_0_9)

                    board.put(PutPiece(party, piece, x, y))
        else:
            print("No custom setup found, assuming default setup.", file=sys.stderr)
            for put_piece in iterate_default_setup():
                board.put(put_piece)

    moves_match = _MOVES_EXTRACTOR.search(content)
    if moves_match:
        moves_body = moves_match.group(1)
        available_moves = list(re.finditer(_SINGLE_MOVE_EXTRACTOR, moves_body))

        if moves_to_play == ALL_MOVES:
            included_moves = available_moves
        else:
            slice_stop = int(moves_to_play)
            if slice_stop > len(available_moves) or slice_stop < -len(available_moves):
                raise ValueError(
                    f"Requested number of moves {slice_stop!r} outside of range of {-len(available_moves)} to {len(available_moves)}"
                )
            included_moves = available_moves[:slice_stop]

        # NOTE: We flip the party after every move rather than relying on
        #       the case of the piece letter (upper- or lowercase) because
        #       software XieXie seems to use uppercase letters all the time,
        #       even when it is Black's turn.
        party = starting_party
        for i, single_move in enumerate(included_moves):
            party_human = "Red" if party == RED else "Black"
            move_human = single_move.group(0)
            if party == BLACK:
                move_human = move_human.lower()  # again because of XieXie's all-uppercase
            print(
                f"Applying move {i + 1:>2}: Move {i // 2 + 1:>2} of {party_human:<5}: {move_human}"
            )
            annotate = annotate_last_move and (i == len(included_moves) - 1)

            board.move(party=party, annotate=annotate, **single_move.groupdict())

            party = {
                RED: BLACK,
                BLACK: RED,
            }[party]

    yield from board.iterate_tokens()
