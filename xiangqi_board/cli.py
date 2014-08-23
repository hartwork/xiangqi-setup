# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import argparse

from .painter import BoardPainter


def run(options):
    board = BoardPainter(
            options.line_thickness_px,
            options.field_width_px,
            options.field_height_px,
            options.border_thickness_px,
            options.border_gap_width_px,
            options.border_gap_height_px,
            options.cross_width_px,
            options.cross_thickness_px,
            options.cross_gap_px,
            )
    board.draw()
    board.write_svg(options.svg_output_file)
    board.write_board_ini(options.ini_output_file)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--line-thickness-px', metavar='FLOAT', default=1.0, type=float,
            help='Line thickness of square fields in pixel (default: %(default)d)')
    parser.add_argument('--field-width-px', metavar='FLOAT', default=53.0, type=float,
            help='Width of fields in pixel (default: %(default)d)')
    parser.add_argument('--field-height-px', metavar='FLOAT', default=53.0, type=float,
            help='Height of fields in pixel (default: %(default)d)')

    parser.add_argument('--border-thickness-px', metavar='FLOAT', default=2.0, type=float,
            help='Line thickness of border in pixel (default: %(default)d)')
    parser.add_argument('--border-gap-width-px', metavar='FLOAT', default=40.0, type=float,
            help='Widtn of gap to border in pixel (default: %(default)d)')
    parser.add_argument('--border-gap-height-px', metavar='FLOAT', default=40.0, type=float,
            help='Height of gap to border in pixel (default: %(default)d)')

    parser.add_argument('--cross-width-px', metavar='FLOAT', default=10.0, type=float,
            help='Width of starting position cross segments in pixel (default: %(default)d)')
    parser.add_argument('--cross-thickness-px', metavar='FLOAT', default=1.0, type=float,
            help='Line thickness of starting position cross in pixel (default: %(default)d)')
    parser.add_argument('--cross-gap-px', metavar='FLOAT', default=4.0, type=float,
            help='Gap to starting position cross in pixel (default: %(default)d)')

    parser.add_argument('svg_output_file', metavar='SVG_FILE')
    parser.add_argument('ini_output_file', metavar='INI_FILE')
    options = parser.parse_args()
    run(options)
