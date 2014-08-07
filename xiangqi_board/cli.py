# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import argparse

from .painter import BoardPainter


def run(options):
    board = BoardPainter()
    board.draw()
    board.write(options.output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file', metavar='OUTPUT_FILE')
    options = parser.parse_args()
    run(options)
