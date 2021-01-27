# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from unittest import TestCase

from parameterized import parameterized

from xiangqi_setup.file_formats.wxf import _PlayerRelativeView
from xiangqi_setup.parties import RED, BLACK
from xiangqi_setup.pieces import PutPiece, ELEPHANT


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
