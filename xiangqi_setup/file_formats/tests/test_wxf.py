# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from unittest import TestCase

from parameterized import parameterized

from ...parties import BLACK, RED
from ...pieces import ADVISOR, CANNON, CHARIOT, ELEPHANT, HORSE, KING, PAWN, PutPiece
from ..fen import PIECE_OF_UPPER_LETTER
from ..wxf import _Board, _PlayerRelativeView


class PlayerRelativeViewTest(TestCase):
    @parameterized.expand(
        [
            (RED, 1, 8),
            (RED, 9, 0),
            (BLACK, 1, 0),
            (BLACK, 9, 8),
        ]
    )
    def test_x_index_from(self, party, player_relative_x_pos, expected_internal_x_index):
        actual_internal_x_index = _PlayerRelativeView(party).x_index_from(player_relative_x_pos)
        self.assertEqual(expected_internal_x_index, actual_internal_x_index)

    @parameterized.expand(
        [
            (RED, +2, +2),
            (RED, -2, -2),
            (BLACK, +2, -2),
            (BLACK, -2, +2),
        ]
    )
    def test_y_diff_from(self, party, player_relative_y_diff, expected_internal_y_diff):
        actual_internal_y_diff = _PlayerRelativeView(party).y_diff_from(player_relative_y_diff)
        self.assertEqual(expected_internal_y_diff, actual_internal_y_diff)

    @parameterized.expand(
        [
            (RED, (2, 4)),
            (BLACK, (2, 1)),
        ]
    )
    def test_further_up_the_board_sort_key(self, party, expected_furthest_up_the_board_x_y):
        piece = ELEPHANT  # arbitrary
        view = _PlayerRelativeView(party)
        x_y_pairs = [
            (2, 2),
            (2, 4),
            (2, 1),
            (2, 3),
        ]  # min and max are not at the so they move during sorting
        x_y_put_pieces = [PutPiece(party, piece, x, y) for x, y in x_y_pairs]
        expected_piece_furthest_up_the_board = PutPiece(
            party, piece, *expected_furthest_up_the_board_x_y
        )
        actual_piece_furthest_up_the_board = sorted(
            x_y_put_pieces, key=view.further_up_the_board_sort_key
        )[-1]
        self.assertEqual(actual_piece_furthest_up_the_board, expected_piece_furthest_up_the_board)


class BoardTest(TestCase):
    @parameterized.expand(
        [
            (CHARIOT, RED, (3, 5), "+", "3", (3, 8)),
            (CHARIOT, BLACK, (3, 5), "+", "3", (3, 2)),
            (CHARIOT, RED, (3, 5), "-", "3", (3, 2)),
            (CHARIOT, BLACK, (3, 5), "-", "3", (3, 8)),
            (CHARIOT, RED, (3, 5), ".", "1", (8, 5)),
            (CHARIOT, RED, (3, 5), ".", "9", (0, 5)),
            (CHARIOT, BLACK, (3, 5), ".", "1", (0, 5)),
            (CHARIOT, BLACK, (3, 5), ".", "9", (8, 5)),
            (HORSE, RED, (2, 4), "+", "9", (0, 5)),
            (HORSE, RED, (2, 4), "+", "8", (1, 6)),
            (HORSE, RED, (2, 4), "+", "6", (3, 6)),
            (HORSE, RED, (2, 4), "+", "5", (4, 5)),
            (HORSE, BLACK, (2, 4), "+", "1", (0, 3)),
            (HORSE, BLACK, (2, 4), "+", "2", (1, 2)),
            (HORSE, BLACK, (2, 4), "+", "4", (3, 2)),
            (HORSE, BLACK, (2, 4), "+", "5", (4, 3)),
            (HORSE, RED, (2, 4), "-", "9", (0, 3)),
            (HORSE, RED, (2, 4), "-", "8", (1, 2)),
            (HORSE, RED, (2, 4), "-", "6", (3, 2)),
            (HORSE, RED, (2, 4), "-", "5", (4, 3)),
            (HORSE, BLACK, (2, 4), "-", "1", (0, 5)),
            (HORSE, BLACK, (2, 4), "-", "2", (1, 6)),
            (HORSE, BLACK, (2, 4), "-", "4", (3, 6)),
            (HORSE, BLACK, (2, 4), "-", "5", (4, 5)),
            (ELEPHANT, RED, (2, 0), "+", "9", (0, 2)),
            (ELEPHANT, RED, (2, 0), "+", "5", (4, 2)),
            (ELEPHANT, BLACK, (2, 9), "+", "1", (0, 7)),
            (ELEPHANT, BLACK, (2, 9), "+", "5", (4, 7)),
            (ELEPHANT, RED, (2, 4), "-", "9", (0, 2)),
            (ELEPHANT, RED, (2, 4), "-", "5", (4, 2)),
            (ELEPHANT, BLACK, (2, 5), "-", "1", (0, 7)),
            (ELEPHANT, BLACK, (2, 5), "-", "5", (4, 7)),
            (ADVISOR, RED, (4, 1), "+", "6", (3, 2)),
            (ADVISOR, RED, (4, 1), "+", "4", (5, 2)),
            (ADVISOR, BLACK, (4, 8), "+", "4", (3, 7)),
            (ADVISOR, BLACK, (4, 8), "+", "6", (5, 7)),
            (ADVISOR, RED, (4, 1), "-", "6", (3, 0)),
            (ADVISOR, RED, (4, 1), "-", "4", (5, 0)),
            (ADVISOR, BLACK, (4, 8), "-", "4", (3, 9)),
            (ADVISOR, BLACK, (4, 8), "-", "6", (5, 9)),
            (KING, RED, (4, 1), "+", "1", (4, 2)),
            (KING, BLACK, (4, 8), "+", "1", (4, 7)),
            (KING, RED, (4, 1), "-", "1", (4, 0)),
            (KING, BLACK, (4, 8), "-", "1", (4, 9)),
            (KING, RED, (4, 1), ".", "4", (5, 1)),
            (KING, RED, (4, 1), ".", "6", (3, 1)),
            (KING, BLACK, (4, 8), ".", "4", (3, 8)),
            (KING, BLACK, (4, 8), ".", "6", (5, 8)),
            (PAWN, RED, (2, 5), "+", "1", (2, 6)),
            (PAWN, BLACK, (2, 4), "+", "1", (2, 3)),
            (PAWN, RED, (2, 5), ".", "8", (1, 5)),
            (PAWN, RED, (2, 5), ".", "6", (3, 5)),
            (PAWN, BLACK, (2, 4), ".", "2", (1, 4)),
            (PAWN, BLACK, (2, 4), ".", "4", (3, 4)),
            (CANNON, RED, (3, 5), "+", "3", (3, 8)),
            (CANNON, BLACK, (3, 5), "+", "3", (3, 2)),
            (CANNON, RED, (3, 5), "-", "3", (3, 2)),
            (CANNON, BLACK, (3, 5), "-", "3", (3, 8)),
            (CANNON, RED, (3, 5), ".", "1", (8, 5)),
            (CANNON, RED, (3, 5), ".", "9", (0, 5)),
            (CANNON, BLACK, (3, 5), ".", "1", (0, 5)),
            (CANNON, BLACK, (3, 5), ".", "9", (8, 5)),
        ]
    )
    def test_calculate_destination_of_move(
        self, piece, party, cur_x_y, operator, argument, expected_new_x_y
    ):
        put_piece = PutPiece(party, piece, *cur_x_y)
        actual_new_x_y = _Board._calculate_destination_of_move(put_piece, operator, argument)
        self.assertEqual(actual_new_x_y, expected_new_x_y)

    @parameterized.expand(
        list(PIECE_OF_UPPER_LETTER.keys())
        + [upper.lower() for upper in PIECE_OF_UPPER_LETTER.keys()]
    )
    def test_locate_piece__by_column(self, wanted_piece_code):
        party = BLACK if wanted_piece_code.islower() else RED
        other_party = BLACK if party == RED else RED

        piece = PIECE_OF_UPPER_LETTER[wanted_piece_code.upper()]
        other_piece = next(
            (
                other_piece_type
                for other_piece_code, other_piece_type in PIECE_OF_UPPER_LETTER.items()
                if other_piece_code != wanted_piece_code.upper()
            )
        )

        # We're putting other pieces on the board so we know that
        # the location algorithm is picky enough with regard to all of
        # - piece type
        # - party
        # - column on the board
        board = _Board()
        x = 3  # arbitrary, with some room left and right
        expected_y = 5  # arbitrary, with some room above and below
        for diff_y in (-1, 0, +1):
            board.put(PutPiece(other_party, piece, x + diff_y, expected_y - 2))
            board.put(PutPiece(party, other_piece, x + diff_y, expected_y - 1))
            board.put(PutPiece(party, piece, x + diff_y, expected_y))
            board.put(PutPiece(party, other_piece, x + diff_y, expected_y + 1))
            board.put(PutPiece(other_party, piece, x + diff_y, expected_y + 2))
        former_column = "6" if party == RED else "4"

        put_piece = board._locate_piece(party, wanted_piece_code, former_column)

        self.assertEqual(x, put_piece.x)
        self.assertEqual(expected_y, put_piece.y)
        self.assertEqual(piece, put_piece.piece)
        self.assertEqual(party, put_piece.party)

    @parameterized.expand(
        [
            (RED, "+", 7),
            (RED, "=", 6),
            (RED, "-", 5),
            (BLACK, "+", 5),
            (BLACK, "=", 6),
            (BLACK, "-", 7),
        ]
    )
    def test_locate_piece__same_column(self, party, former_column, expected_y):
        other_party = BLACK if party == RED else RED
        piece = CHARIOT  # arbitrary
        upper_piece_code = [
            upper_piece_code for upper_piece_code, piece_type in PIECE_OF_UPPER_LETTER.items()
        ][0]
        piece_code = upper_piece_code.lower() if party == BLACK else upper_piece_code

        other_piece = CANNON  # arbitrary
        assert other_piece != piece
        x = 3  # arbitary

        # We're putting other pieces on the board so we know that
        # the location algorithm is picky enough with regard to all of
        # - piece type
        # - party
        # - row on the board
        board = _Board()
        board.put(PutPiece(party, other_piece, x, y=8))
        board.put(PutPiece(party, piece, x, y=7))
        board.put(PutPiece(party, piece, x, y=6))
        board.put(PutPiece(party, piece, x, y=5))
        board.put(PutPiece(other_party, piece, x, y=4))
        board.put(PutPiece(other_party, piece, x, y=3))
        board.put(PutPiece(other_party, piece, x, y=2))
        board.put(PutPiece(party, other_piece, x, y=1))

        put_piece = board._locate_piece(party, piece_code, former_column)

        self.assertEqual(x, put_piece.x)
        self.assertEqual(expected_y, put_piece.y)
        self.assertEqual(piece, put_piece.piece)
        self.assertEqual(party, put_piece.party)
