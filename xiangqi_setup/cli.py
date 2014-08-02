# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import argparse
import sys

from .wxf_format import iterate_wxf_tokens
from .compose import compose_svg, cm_to_pixel


def check(options):
    if 0 < options.piece_scale <= 1.0:
        pass
    else:
        print('ERROR: Piece scale must be larger than zero and greater or equal one.', file=sys.stderr)
        sys.exit(1)

def run(options):
    pieces_to_put = list(iterate_wxf_tokens(options.input_file))
    compose_svg(pieces_to_put, options)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board', dest='board_theme_dir', metavar='DIRECTORY', default='XXXXXXXXX')
    parser.add_argument('--pieces', dest='pieces_theme_dir', metavar='DIRECTORY', default='XXXXXXXXX')
    parser.add_argument('--width', dest='width_pixel', metavar='PIXEL', type=float, default=cm_to_pixel(7.0))
    parser.add_argument('--scale-pieces', dest='piece_scale', metavar='FACTOR', type=float, default=0.9)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('input_file', metavar='INPUT_FILE')
    parser.add_argument('output_file', metavar='OUTPUT_FILE')
    options = parser.parse_args()
    check(options)
    run(options)
