# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

from six.moves import configparser
import errno
import os

try:
    import svgutils.transform as sg
except ImportError:
    import sys
    print('Please install svg_utils first: https://github.com/btel/svg_utils', file=sys.stderr)
    sys.exit(1)

from .wxf_format import \
        CHARIOT, HORSE, ELEPHANT, ADVISOR, KING, CANNON, PAWN, \
        RED, BLACK 


_BOARD_SVG_BASENAME = 'board.svg'
_BOARD_INI_BASENAME = 'board.ini'
_BOARD_CONFIG_SECTION = 'Board'

_DIAMOND_FILE_NAME = os.path.join('..', 'diamond.svg')

_MAX_X = 8
_MAX_Y = 9


_FILENAME_OF_PARTY_PIECE = {
    RED: {
        CHARIOT: 'red_chariot.svg',
        HORSE: 'red_horse.svg',
        ELEPHANT: 'red_elephant.svg',
        ADVISOR: 'red_advisor.svg',
        KING: 'red_king.svg',
        CANNON: 'red_cannon.svg',
        PAWN: 'red_pawn.svg',
    },
    BLACK: {
        CHARIOT: 'black_chariot.svg',
        HORSE: 'black_horse.svg',
        ELEPHANT: 'black_elephant.svg',
        ADVISOR: 'black_advisor.svg',
        KING: 'black_king.svg',
        CANNON: 'black_cannon.svg',
        PAWN: 'black_pawn.svg',
    }
}


def _length_string_to_pixel(text, resolution_dpi):
    if text.endswith('cm'):
        return cm_to_pixel(float(text[:-2]), resolution_dpi)
    return float(text)

def _cm_to_inch(cm):
    return cm * 0.393700787

def cm_to_pixel(cm, resolution_dpi):
    return _cm_to_inch(cm) * resolution_dpi


def compose_svg(pieces_to_put, options):
    board_svg_filename = os.path.join(options.board_theme_dir, _BOARD_SVG_BASENAME)
    board_ini_filename = os.path.join(options.board_theme_dir, _BOARD_INI_BASENAME)

    # Check for existance ourselves since configparser would throw NoSectionError
    # at us for a missing file.
    if not os.path.exists(board_ini_filename):
        raise IOError(errno.ENOENT, "No such file or directory: '%s'" % board_ini_filename)

    config = configparser.RawConfigParser(defaults={'river': 0.0})
    config.read(board_ini_filename)

    output_board_offset_left_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'left')
    output_board_offset_top_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'top')
    output_board_width_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'width')
    output_board_height_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'height')
    output_board_river_height_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'river')

    jobs = []
    for put_piece in pieces_to_put:
        x_rel = float(put_piece.x) / _MAX_X
        y_rel = float(_MAX_Y - put_piece.y) / _MAX_Y
        basename = _FILENAME_OF_PARTY_PIECE[put_piece.party][put_piece.piece]
        filename = os.path.join(options.pieces_theme_dir, basename)
        jobs.append((x_rel, y_rel, filename))

    if options.debug:
        for x_rel in (0.0, 1.0):
            for y_rel in (0.0, 1.0):
                jobs.append((x_rel, y_rel, os.path.join(options.pieces_theme_dir, _DIAMOND_FILE_NAME)))

    # Read board
    board_fig = sg.fromfile(board_svg_filename)
    board_root = board_fig.getroot()

    # Scale board to output
    board_width_pixel, board_height_pixel = [_length_string_to_pixel(e, options.resolution_dpi) for e in board_fig.get_size()]
    height_factor = board_height_pixel / float(board_width_pixel)
    board_scale = options.width_pixel / board_width_pixel
    board_root.moveto(0, 0, scale=board_scale)

    output_board_offset_left_pixel *= board_scale
    output_board_offset_top_pixel *= board_scale
    output_board_width_pixel *= board_scale
    output_board_height_pixel *= board_scale
    output_board_river_height_pixel *= board_scale

    # Initialize output figure
    output_fig = sg.SVGFigure(
            str(options.width_pixel),
            str(options.width_pixel * height_factor))
    output_fig.append([board_root, ])

    for (x_rel, y_rel, filename) in jobs:
        piece_fig = sg.fromfile(filename)
        piece_root = piece_fig.getroot()
        original_piece_width_pixel, original_piece_height_pixel = [
                _length_string_to_pixel(s, options.resolution_dpi)
                for s in piece_fig.get_size()
                ]

        # Scale and put piece onto board
        center_x_pixel = output_board_offset_left_pixel + output_board_width_pixel * x_rel
        center_y_pixel = output_board_offset_top_pixel + (output_board_height_pixel - output_board_river_height_pixel) * y_rel \
                + (output_board_river_height_pixel if (y_rel >= 0.5) else 0.0)

        maximum_future_piece_width_pixel = output_board_width_pixel / _MAX_X * options.piece_scale
        maximum_future_piece_height_pixel = output_board_height_pixel / _MAX_Y * options.piece_scale

        scale = min(maximum_future_piece_width_pixel / original_piece_width_pixel, maximum_future_piece_height_pixel / original_piece_height_pixel)

        future_piece_width_pixel = original_piece_width_pixel * scale
        future_piece_height_pixel = original_piece_height_pixel * scale

        x_pixel = center_x_pixel - future_piece_width_pixel / 2.0
        y_pixel = center_y_pixel - future_piece_height_pixel / 2.0
        piece_root.moveto(x_pixel, y_pixel, scale=scale)
        output_fig.append([piece_root, ])

    output_fig.save(options.output_file)
