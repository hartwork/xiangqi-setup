# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import svgutils.transform as sg


_BOARDER_WIDTH_PIXEL = 2
_BOARDER_GAP_PIXEL = 40
_LINE_WIDTH_PIXEL = 1
_SQUARE_WIDTH_PIXEL = 53
_START_HELPER_LENGTH_PIXEL = 10
_START_HELPER_LINE_WIDTH_PIXEL = 1
_START_HELPER_GAP_PIXEL = 4


class BoardPainter(object):
    def __init__(self):
        self._lines = []
        self._square_width_pixel = _SQUARE_WIDTH_PIXEL

    def _playing_field_offset(self):
        return _BOARDER_WIDTH_PIXEL + _BOARDER_GAP_PIXEL + _LINE_WIDTH_PIXEL / 2.0

    def _cross(self, (column, row)):
        SHIFT = self._playing_field_offset()
        x = SHIFT + column * self._square_width_pixel
        y = SHIFT + row * self._square_width_pixel
        return (x, y)

    def _raw_line(self, start, end, width):
        line = sg.LineElement([start, end], width=width)
        self._lines.append(line)

    def _grid_line(self, start, end):
        self._raw_line(self._cross(start), self._cross(end), _LINE_WIDTH_PIXEL)

    def _outer_board_width_pixel(self):
        return 2 * _BOARDER_WIDTH_PIXEL + 2 * _BOARDER_GAP_PIXEL + _LINE_WIDTH_PIXEL \
                + 8 * self._square_width_pixel

    def _outer_board_height_pixel(self):
        return 2 * _BOARDER_WIDTH_PIXEL + 2 * _BOARDER_GAP_PIXEL + _LINE_WIDTH_PIXEL \
                + 9 * self._square_width_pixel

    def _draw_border(self):
        # Vertical lines
        WIDTH = self._outer_board_width_pixel()
        HEIGHT = self._outer_board_height_pixel()
        X_LEFT_CENTER = _BOARDER_WIDTH_PIXEL / 2.0
        X_RIGHT_CENTER = WIDTH - _BOARDER_WIDTH_PIXEL / 2.0
        Y_TOP_CENTER = _BOARDER_WIDTH_PIXEL / 2.0
        Y_BOTTOM_CENTER = HEIGHT - _BOARDER_WIDTH_PIXEL / 2.0
        for start, end in (
                # Vertical lines
                ((X_LEFT_CENTER, 0), (X_LEFT_CENTER, HEIGHT)),
                ((X_RIGHT_CENTER, 0), (X_RIGHT_CENTER, HEIGHT)),

                # Horizontal lines
                ((0, Y_TOP_CENTER), (WIDTH, Y_TOP_CENTER)),
                ((0, Y_BOTTOM_CENTER), (WIDTH, Y_BOTTOM_CENTER)),
                ):
            line = sg.LineElement([start, end], width=_BOARDER_WIDTH_PIXEL)
            self._lines.append(line)

    def _draw_playing_field(self):
        # Vertical lines, river gap
        for column in range(0, 9):
            if 0 < column < 8:
                self._grid_line((column, 0), (column, 4))
                self._grid_line((column, 5), (column, 9))
            else:
                self._grid_line((column, 0), (column, 9))

        # Horizontal lines
        for row in range(0, 10):
            self._grid_line((0, row), (8, row))

        # Palace crosses
        self._grid_line((3, 0), (5, 2))
        self._grid_line((3, 2), (5, 0))
        self._grid_line((3, 7), (5, 9))
        self._grid_line((3, 9), (5, 7))

    def _add_setup_helper(self, column, row, left, right):
        assert left or right
        center = self._cross((column, row))
        for x_factor, y_factor, wanted in (
                (1, -1, right),  # top right
                (1, 1, right),  # bottom right
                (-1, 1, left),  # bottom left
                (-1, -1, left),  # top left
                ):
            if not wanted:
                continue

            GAP = _LINE_WIDTH_PIXEL / 2.0 + _START_HELPER_GAP_PIXEL + _START_HELPER_LINE_WIDTH_PIXEL / 2.0
            start_x = center[0] + x_factor * GAP
            start_y = center[1] + y_factor * GAP

            # Vertical part
            end_x = start_x
            end_y = start_y + y_factor * _START_HELPER_LENGTH_PIXEL
            SHIFT_Y = y_factor * _START_HELPER_LINE_WIDTH_PIXEL / 2.0
            self._raw_line((start_x, start_y - SHIFT_Y), (end_x, end_y - SHIFT_Y), _START_HELPER_LINE_WIDTH_PIXEL)

            # Horizontal part
            end_x = start_x + x_factor * _START_HELPER_LENGTH_PIXEL
            end_y = start_y
            SHIFT_X = x_factor * _START_HELPER_LINE_WIDTH_PIXEL / 2.0
            self._raw_line((start_x - SHIFT_X, start_y), (end_x - SHIFT_X, end_y), _START_HELPER_LINE_WIDTH_PIXEL)

    def _draw_setup_helpers(self):
        for column, row in (
                # Black cannons
                (1, 2), (7, 2),
                # Black pawns
                (0, 3),  (2, 3), (4, 3), (6, 3), (8, 3),
                # Red pawns
                (0, 6),  (2, 6), (4, 6), (6, 6), (8, 6),
                # Red cannons
                (1, 7), (7, 7),
                ):
            left = (column > 0)
            right = (column < 8)
            self._add_setup_helper(column, row, left, right)

    def draw(self):
        self._draw_playing_field()
        self._draw_setup_helpers()
        self._draw_border()

    def write(self, filename):
        WIDTH = self._outer_board_width_pixel()
        HEIGHT = self._outer_board_height_pixel()
        output_fig = sg.SVGFigure(str(WIDTH), str(HEIGHT))
        output_fig.append(self._lines)
        output_fig.save(filename)
