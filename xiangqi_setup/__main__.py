# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import argparse
import glob
import inspect
import os
import sys
from pkg_resources import resource_filename

if sys.version_info[:2] < (3, 5):
    from scandir import walk
else:
    from os import walk

from .wxf_format import iterate_wxf_tokens, iterate_fen_tokens
from .compose import compose_svg, cm_to_pixel
from .license import get_license_choices_of_theme, inform_license
from .version import VERSION_STR


_DEFAULT_WIDTH_CM = 7.0

_PIECE_SCALE_MIN = 0.0
_PIECE_SCALE_MAX = 1.2


def _get_self_dir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def _get_themes_home_dir():
    self_dir = _get_self_dir()
    if os.path.exists(os.path.join(self_dir, '..', '.git')):
        return os.path.join(self_dir, 'themes')
    else:
        return resource_filename('xiangqi_setup', 'themes')


def check(options):
    if _PIECE_SCALE_MIN < options.piece_scale <= _PIECE_SCALE_MAX:
        pass
    else:
        print('ERROR: Piece scale must be larger than %.1f and greater or equal %.1f .' \
                % (_PIECE_SCALE_MIN, _PIECE_SCALE_MAX), file=sys.stderr)
        sys.exit(1)

    if options.width_centimeter is not None:
        options.width_pixel = cm_to_pixel(options.width_centimeter, options.resolution_dpi)
    delattr(options, 'width_centimeter')
    if options.width_pixel is None:
        options.width_pixel = cm_to_pixel(_DEFAULT_WIDTH_CM, options.resolution_dpi)


def run(options):
    with open(options.input_file, 'r') as f:
        content = f.read()
        if 'WXF' in content:
            pieces_to_put = list(iterate_wxf_tokens(content))
        else:
            pieces_to_put = list(iterate_fen_tokens(content))
    compose_svg(pieces_to_put, options)
    inform_license(options.board_theme_dir, options.pieces_theme_dir)


def _theme_name(text):
    if '/' in text:
        raise ValueError('Theme name cannot contain slashes')
    return text

_theme_name.__name__ = 'theme name'  # used by arparse error message


def _discover_themes_in(directory):
    for _root, dirs, _files in walk(directory, topdown=True):
        return [d for d in dirs if d != '__pycache__']


def main():
    themes_home_dir = _get_themes_home_dir()
    board_themes_home_dir = os.path.join(themes_home_dir, 'board')
    pieces_themes_home_dir = os.path.join(themes_home_dir, 'pieces')

    epilog_chunks = []

    # Are we in --help mode (or can we save wasting time collecting all that data)
    if '--help' in sys.argv[1:] or '-h' in sys.argv[1:]:
        board_theme_choices = []
        pieces_theme_choices = []
        for directory, target_list in (
                (board_themes_home_dir, board_theme_choices),
                (pieces_themes_home_dir, pieces_theme_choices),
                ):
            target_list += _discover_themes_in(directory)

        for category, category_home_dir, source_list, blank_line_after in (
                ('board themes', board_themes_home_dir, board_theme_choices, True),
                ('pieces themes', pieces_themes_home_dir, pieces_theme_choices, False),
                ):
            epilog_chunks.append('%s (%d available, in alphabetic order):' % (category, len(source_list)))
            for name in sorted(source_list, key=lambda x: x.lower()):
                license_choices = get_license_choices_of_theme(os.path.join(category_home_dir, name))
                epilog_chunks.append('  %-42s (license: %s)' % (name, ' / '.join(license_choices)))
            if blank_line_after:
                epilog_chunks.append('')

    parser = argparse.ArgumentParser(
            epilog='\n'.join(epilog_chunks),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    theme_options = parser.add_argument_group('theme selection')
    theme_options.add_argument('--board', dest='board_theme_dir', metavar='THEME',
            type=_theme_name, default='clean_alpha',
            help='name of board theme to use (default: "%(default)s"; please check the list of available themes below')
    theme_options.add_argument('--pieces', dest='pieces_theme_dir', metavar='THEME',
            type=_theme_name, default='retro_simple',
            help='name of pieces theme to use (default: "%(default)s"; please check the list of available themes below')

    scaling_options = parser.add_argument_group('scaling')
    width_options = scaling_options.add_mutually_exclusive_group()
    width_options.add_argument('--width-px', dest='width_pixel', metavar='PIXEL', type=float,
            help='width of the output in pixels')
    width_options.add_argument('--width-cm', dest='width_centimeter', metavar='CENTIMETER', type=float,
            help='width of the output in centimeters')
    scaling_options.add_argument('--dpi', dest='resolution_dpi', metavar='FLOAT', type=float, default=90.0,
            help='resolution of the output in dots per inch')
    scaling_options.add_argument('--scale-pieces', dest='piece_scale', metavar='FACTOR', type=float, default=0.9,
            help='factor to scale pieces by (%.1f to %.1f, default: %%(default)s)' % (_PIECE_SCALE_MIN, _PIECE_SCALE_MAX))

    parser.add_argument('--debug', action='store_true',
            help='enable debugging (e.g. mark corners of the board)')

    parser.add_argument('input_file', metavar='INPUT_FILE',
            help='location of WXF or FEN file to render')
    parser.add_argument('output_file', metavar='OUTPUT_FILE',
            help='location of SVG output file to write')

    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION_STR)

    options = parser.parse_args()

    # Turn theme names into paths
    options.board_theme_dir = os.path.join(board_themes_home_dir, options.board_theme_dir)
    options.pieces_theme_dir = os.path.join(pieces_themes_home_dir, options.pieces_theme_dir)

    check(options)
    run(options)


if __name__ == '__main__':
     main()
