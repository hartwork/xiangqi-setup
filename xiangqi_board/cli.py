# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import argparse

from .painter import BoardPainter


def run(options):
    board = BoardPainter()
    board.draw()
    board.write_svg(options.svg_output_file)
    board.write_board_ini(options.ini_output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('svg_output_file', metavar='SVG_FILE')
    parser.add_argument('ini_output_file', metavar='INI_FILE')
    options = parser.parse_args()
    run(options)
