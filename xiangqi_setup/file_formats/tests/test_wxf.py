# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from unittest import TestCase

from parameterized import parameterized

from xiangqi_setup.file_formats.wxf import _PlayerRelativeView, _Board
from xiangqi_setup.parties import RED, BLACK
from xiangqi_setup.pieces import PutPiece, ELEPHANT, CHARIOT, CANNON, HORSE, ADVISOR, KING, PAWN


class PlayerRelativeViewTest(TestCase):
    @parameterized.expand([
        (RED, 1, 8),
        (RED, 9, 0),
        (BLACK, 1, 0),
        (BLACK, 9, 8),
    ])
    def test_x_index_from(self, party, player_relative_x_pos, expected_internal_x_index):
        actual_internal_x_index = _PlayerRelativeView(party).x_index_from(player_relative_x_pos)
        self.assertEqual(expected_internal_x_index, actual_internal_x_index)

    @parameterized.expand([
        (RED, +2, +2),
        (RED, -2, -2),
        (BLACK, +2, -2),
        (BLACK, -2, +2),
    ])
    def test_y_diff_from(self, party, player_relative_y_diff, expected_internal_y_diff):
        actual_internal_y_diff = _PlayerRelativeView(party).y_diff_from(player_relative_y_diff)
        self.assertEqual(expected_internal_y_diff, actual_internal_y_diff)

    @parameterized.expand([
        (RED, (2, 4)),
        (BLACK, (2, 1)),
    ])
    def test_further_up_the_board_sort_key(self, party, expected_furthest_up_the_board_x_y):
        piece = ELEPHANT  # arbitrary
        view = _PlayerRelativeView(party)
        x_y_pairs = [(2, 2), (2, 4), (2, 1), (2, 3)]  # min and max are not at the so they move during sorting
        x_y_put_pieces = [PutPiece(party, piece, x, y) for x, y in x_y_pairs]
        expected_piece_furthest_up_the_board = PutPiece(party, piece, *expected_furthest_up_the_board_x_y)
        actual_piece_furthest_up_the_board = sorted(x_y_put_pieces, key=view.further_up_the_board_sort_key)[-1]
        self.assertEqual(actual_piece_furthest_up_the_board, expected_piece_furthest_up_the_board)


class BoardTest(TestCase):
    @parameterized.expand([
        (CHARIOT, RED, (3, 5), '+', '3', (3, 8)),
        (CHARIOT, BLACK, (3, 5), '+', '3', (3, 2)),
        (CHARIOT, RED, (3, 5), '-', '3', (3, 2)),
        (CHARIOT, BLACK, (3, 5), '-', '3', (3, 8)),
        (CHARIOT, RED, (3, 5), '.', '1', (8, 5)),
        (CHARIOT, RED, (3, 5), '.', '9', (0, 5)),
        (CHARIOT, BLACK, (3, 5), '.', '1', (0, 5)),
        (CHARIOT, BLACK, (3, 5), '.', '9', (8, 5)),

        (HORSE, RED, (2, 4), '+', '9', (0, 5)),
        (HORSE, RED, (2, 4), '+', '8', (1, 6)),
        (HORSE, RED, (2, 4), '+', '6', (3, 6)),
        (HORSE, RED, (2, 4), '+', '5', (4, 5)),
        (HORSE, BLACK, (2, 4), '+', '1', (0, 3)),
        (HORSE, BLACK, (2, 4), '+', '2', (1, 2)),
        (HORSE, BLACK, (2, 4), '+', '4', (3, 2)),
        (HORSE, BLACK, (2, 4), '+', '5', (4, 3)),
        (HORSE, RED, (2, 4), '-', '9', (0, 3)),
        (HORSE, RED, (2, 4), '-', '8', (1, 2)),
        (HORSE, RED, (2, 4), '-', '6', (3, 2)),
        (HORSE, RED, (2, 4), '-', '5', (4, 3)),
        (HORSE, BLACK, (2, 4), '-', '1', (0, 5)),
        (HORSE, BLACK, (2, 4), '-', '2', (1, 6)),
        (HORSE, BLACK, (2, 4), '-', '4', (3, 6)),
        (HORSE, BLACK, (2, 4), '-', '5', (4, 5)),

        (ELEPHANT, RED, (2, 0), '+', '9', (0, 2)),
        (ELEPHANT, RED, (2, 0), '+', '5', (4, 2)),
        (ELEPHANT, BLACK, (2, 9), '+', '1', (0, 7)),
        (ELEPHANT, BLACK, (2, 9), '+', '5', (4, 7)),
        (ELEPHANT, RED, (2, 4), '-', '9', (0, 2)),
        (ELEPHANT, RED, (2, 4), '-', '5', (4, 2)),
        (ELEPHANT, BLACK, (2, 5), '-', '1', (0, 7)),
        (ELEPHANT, BLACK, (2, 5), '-', '5', (4, 7)),

        (ADVISOR, RED, (4, 1), '+', '6', (3, 2)),
        (ADVISOR, RED, (4, 1), '+', '4', (5, 2)),
        (ADVISOR, BLACK, (4, 8), '+', '4', (3, 7)),
        (ADVISOR, BLACK, (4, 8), '+', '6', (5, 7)),
        (ADVISOR, RED, (4, 1), '-', '6', (3, 0)),
        (ADVISOR, RED, (4, 1), '-', '4', (5, 0)),
        (ADVISOR, BLACK, (4, 8), '-', '4', (3, 9)),
        (ADVISOR, BLACK, (4, 8), '-', '6', (5, 9)),

        (KING, RED, (4, 1), '+', '1', (4, 2)),
        (KING, BLACK, (4, 8), '+', '1', (4, 7)),
        (KING, RED, (4, 1), '-', '1', (4, 0)),
        (KING, BLACK, (4, 8), '-', '1', (4, 9)),
        (KING, RED, (4, 1), '.', '4', (5, 1)),
        (KING, RED, (4, 1), '.', '6', (3, 1)),
        (KING, BLACK, (4, 8), '.', '4', (3, 8)),
        (KING, BLACK, (4, 8), '.', '6', (5, 8)),

        (PAWN, RED, (2, 5), '+', '1', (2, 6)),
        (PAWN, BLACK, (2, 4), '+', '1', (2, 3)),
        (PAWN, RED, (2, 5), '.', '8', (1, 5)),
        (PAWN, RED, (2, 5), '.', '6', (3, 5)),
        (PAWN, BLACK, (2, 4), '.', '2', (1, 4)),
        (PAWN, BLACK, (2, 4), '.', '4', (3, 4)),

        (CANNON, RED, (3, 5), '+', '3', (3, 8)),
        (CANNON, BLACK, (3, 5), '+', '3', (3, 2)),
        (CANNON, RED, (3, 5), '-', '3', (3, 2)),
        (CANNON, BLACK, (3, 5), '-', '3', (3, 8)),
        (CANNON, RED, (3, 5), '.', '1', (8, 5)),
        (CANNON, RED, (3, 5), '.', '9', (0, 5)),
        (CANNON, BLACK, (3, 5), '.', '1', (0, 5)),
        (CANNON, BLACK, (3, 5), '.', '9', (8, 5)),
    ])
    def test_calculate_destination_of_move(self, piece, party, cur_x_y, operator, argument, expected_new_x_y):
        put_piece = PutPiece(party, piece, *cur_x_y)
        actual_new_x_y = _Board._calculate_destination_of_move(put_piece, operator, argument)
        self.assertEqual(actual_new_x_y, expected_new_x_y)
