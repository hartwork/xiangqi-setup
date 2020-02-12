# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

from six.moves import configparser

import svgutils.transform as sg


class BoardPainter(object):
    def __init__(self,
            line_thickness_pixel,
            field_width_px,
            field_height_px,
            border_thickness_pixel,
            border_gap_width_pixel,
            border_gap_height_pixel,
            cross_length_pixel,
            cross_thickness_pixel,
            cross_gap_pixel,
            ):
        self._lines = []

        self._line_thickness_pixel = line_thickness_pixel
        self._field_width_px = field_width_px
        self._field_height_px = field_height_px
        self._border_thickness_pixel = border_thickness_pixel
        self._border_gap_width_pixel = border_gap_width_pixel
        self._border_gap_height_pixel = border_gap_height_pixel
        self._cross_width_pixel = cross_length_pixel
        self._cross_thickness_pixel = cross_thickness_pixel
        self._cross_gap_pixel = cross_gap_pixel

    def _playing_field_offset_left(self):
        return self._border_thickness_pixel + self._border_gap_width_pixel + self._line_thickness_pixel / 2.0

    def _playing_field_offset_top(self):
        return self._border_thickness_pixel + self._border_gap_height_pixel + self._line_thickness_pixel / 2.0

    def _cross(self, location):
        column, row = location
        x = self._playing_field_offset_left() + column * self._field_width_px
        y = self._playing_field_offset_top() + row * self._field_height_px
        return (x, y)

    def _raw_line(self, start, end, width):
        line = sg.LineElement([start, end], width=width)
        self._lines.append(line)

    def _grid_line(self, start, end):
        self._raw_line(self._cross(start), self._cross(end), self._line_thickness_pixel)

    def _outer_board_width_pixel(self):
        return 2 * self._border_thickness_pixel + 2 * self._border_gap_width_pixel + self._line_thickness_pixel \
                + 8 * self._field_width_px

    def _outer_board_height_pixel(self):
        return 2 * self._border_thickness_pixel + 2 * self._border_gap_height_pixel + self._line_thickness_pixel \
                + 9 * self._field_height_px

    def _draw_border(self):
        # Vertical lines
        WIDTH = self._outer_board_width_pixel()
        HEIGHT = self._outer_board_height_pixel()
        X_LEFT_CENTER = self._border_thickness_pixel / 2.0
        X_RIGHT_CENTER = WIDTH - self._border_thickness_pixel / 2.0
        Y_TOP_CENTER = self._border_thickness_pixel / 2.0
        Y_BOTTOM_CENTER = HEIGHT - self._border_thickness_pixel / 2.0
        for start, end in (
                # Vertical lines
                ((X_LEFT_CENTER, 0), (X_LEFT_CENTER, HEIGHT)),
                ((X_RIGHT_CENTER, 0), (X_RIGHT_CENTER, HEIGHT)),

                # Horizontal lines
                ((0, Y_TOP_CENTER), (WIDTH, Y_TOP_CENTER)),
                ((0, Y_BOTTOM_CENTER), (WIDTH, Y_BOTTOM_CENTER)),
                ):
            line = sg.LineElement([start, end], width=self._border_thickness_pixel)
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

            GAP = self._line_thickness_pixel / 2.0 + self._cross_gap_pixel + self._cross_thickness_pixel / 2.0
            start_x = center[0] + x_factor * GAP
            start_y = center[1] + y_factor * GAP

            # Vertical part
            end_x = start_x
            end_y = start_y + y_factor * self._cross_width_pixel
            SHIFT_Y = y_factor * self._cross_thickness_pixel / 2.0
            self._raw_line((start_x, start_y - SHIFT_Y), (end_x, end_y - SHIFT_Y), self._cross_thickness_pixel)

            # Horizontal part
            end_x = start_x + x_factor * self._cross_width_pixel
            end_y = start_y
            SHIFT_X = x_factor * self._cross_thickness_pixel / 2.0
            self._raw_line((start_x - SHIFT_X, start_y), (end_x - SHIFT_X, end_y), self._cross_thickness_pixel)

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
        if self._cross_thickness_pixel != 0:
            self._draw_setup_helpers()
        if self._border_thickness_pixel != 0:
            self._draw_border()

    def write_svg(self, filename):
        WIDTH = self._outer_board_width_pixel()
        HEIGHT = self._outer_board_height_pixel()
        output_fig = sg.SVGFigure(str(WIDTH), str(HEIGHT))
        output_fig.append(self._lines)
        output_fig.save(filename)

    def write_board_ini(self, filename):
        f = open(filename, 'w')
        config = configparser.RawConfigParser()
        config.add_section('Board')
        config.set('Board', 'left', str(self._playing_field_offset_left()))
        config.set('Board', 'top', str(self._playing_field_offset_top()))
        config.set('Board', 'width', str(self._field_width_px * 8))
        config.set('Board', 'height', str(self._field_height_px * 9))
        config.write(f)
        f.close()
