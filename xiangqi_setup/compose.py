# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import configparser
import errno
import os
from collections import defaultdict
from typing import Tuple

import yaml

try:
    from svgutils.compose import Unit
    from svgutils.transform import SVGFigure, fromfile
except ImportError:
    import sys
    print(
        'Please install version 0.3.2 of svgutils'
        ' (https://github.com/btel/svg_utils) first,'
        ' e.g. by running "pip install svgutils==0.3.2".',
        file=sys.stderr)
    sys.exit(1)

from .annotations import PutAnnotation
from .parties import BLACK, RED
from .pieces import ADVISOR, CANNON, CHARIOT, ELEPHANT, HORSE, KING, PAWN, PutPiece

_BOARD_SVG_BASENAME = 'board.svg'
_BOARD_INI_BASENAME = 'board.ini'
_BOARD_CONFIG_SECTION = 'Board'

_DIAMOND_FILE_NAME = os.path.join('..', 'diamond.svg')

_MAX_X = 8
_MAX_Y = 9

_Z_INDEX_PIECE_LEVEL = 0
_Z_INDEX_DEBUG_DIAMOND = 1000  # i.e. way above piece level and assumed sane annotation levels

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


def _anything_to_pixel(unit: str, raw_value: float, resolution_dpi: float) -> float:
    if unit == 'cm':
        return cm_to_pixel(raw_value, resolution_dpi)
    if unit == 'mm':
        return cm_to_pixel(raw_value / 10.0, resolution_dpi)
    if unit == 'px':
        return raw_value
    raise ValueError(f'Unit {unit!r} not yet supported, please open a bug.')


def _length_string_to_pixel(text: str, resolution_dpi: float) -> float:
    try:
        raw_value = float(text)
    except ValueError:
        raw_value, unit = float(text[:-2]), text[-2:]
        return _anything_to_pixel(unit, raw_value, resolution_dpi)

    return raw_value


def _pixel_viewbox_of_figure(figure: SVGFigure, resolution_dpi: float) -> Tuple[float, float]:
    # NOTE: Attribute "viewbox" (with lowercase "b") is ignored by Inkscape 1.0.1
    #       in practice so I'm following Inkscape here and ignore the lowercase
    #       edition, too.
    try:
        view_box = figure.root.attrib['viewBox']
    except KeyError:
        left_str, top_str = '0', '0'
        width_str, height_str = figure.get_size()
    else:
        left_str, top_str, width_str, height_str = view_box.split()

    return (
        _length_string_to_pixel(left_str, resolution_dpi),
        _length_string_to_pixel(top_str, resolution_dpi),
        _length_string_to_pixel(width_str, resolution_dpi),
        _length_string_to_pixel(height_str, resolution_dpi),
    )


def _cm_to_inch(cm):
    return cm * 0.393700787


def cm_to_pixel(cm, resolution_dpi):
    return _cm_to_inch(cm) * resolution_dpi


def compose_svg(atoms_to_put, options):
    board_svg_filename = os.path.join(options.board_theme_dir, _BOARD_SVG_BASENAME)
    board_ini_filename = os.path.join(options.board_theme_dir, _BOARD_INI_BASENAME)

    # Check for existance ourselves since configparser would throw NoSectionError
    # at us for a missing file.
    if not os.path.exists(board_ini_filename):
        raise OSError(errno.ENOENT, "No such file or directory: '%s'" % board_ini_filename)

    config = configparser.RawConfigParser(defaults={'river': 0.0})
    config.read(board_ini_filename)

    output_board_offset_left_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'left')
    output_board_offset_top_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'top')
    output_board_width_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'width')
    output_board_height_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'height')
    output_board_river_height_pixel = config.getfloat(_BOARD_CONFIG_SECTION, 'river')

    # Regular pieces are at level 0; level 1 and above is drawn on top of (i.e. after)
    # the pieces while -1 and below is drawn below (i.e. before) the pieces.
    jobs_at_z_index = defaultdict(list)

    annotation_theme_config_filename = os.path.join(options.annotation_theme_dir, 'config.yml')
    with open(annotation_theme_config_filename) as f:
        annotation_theme_config = yaml.safe_load(f)

    for put_atom in atoms_to_put:
        if isinstance(put_atom, PutAnnotation):
            put_annotation: PutAnnotation = put_atom
            x_rel = float(put_annotation.x) / _MAX_X
            y_rel = float(_MAX_Y - put_annotation.y) / _MAX_Y
            filename = os.path.join(options.annotation_theme_dir,
                                    f'{put_annotation.annotation_name}.svg')
            annotation_scale = options.annotation_scale if annotation_theme_config[
                'allow_scaling'][put_annotation.annotation_name] else 1.0
            atom_z_index = int(annotation_theme_config['z_index'][put_annotation.annotation_name])
            jobs_at_z_index[atom_z_index].append((x_rel, y_rel, filename, annotation_scale))
        else:
            assert isinstance(put_atom, PutPiece)
            put_piece: PutPiece = put_atom
            x_rel = float(put_piece.x) / _MAX_X
            y_rel = float(_MAX_Y - put_piece.y) / _MAX_Y
            basename = _FILENAME_OF_PARTY_PIECE[put_piece.party][put_piece.piece]
            filename = os.path.join(options.piece_theme_dir, basename)
            jobs_at_z_index[_Z_INDEX_PIECE_LEVEL].append(
                (x_rel, y_rel, filename, options.piece_scale))

    if options.debug:
        for x_rel in (0.0, 1.0):
            for y_rel in (0.0, 1.0):
                jobs_at_z_index[_Z_INDEX_DEBUG_DIAMOND].append(
                    (x_rel, y_rel, os.path.join(options.piece_theme_dir,
                                                _DIAMOND_FILE_NAME), options.piece_scale))

    # Read board
    board_fig = fromfile(board_svg_filename)
    board_root = board_fig.getroot()

    # Scale board to output
    board_width_pixel, board_height_pixel = _pixel_viewbox_of_figure(board_fig,
                                                                     options.resolution_dpi)[2:]
    height_factor = board_height_pixel / float(board_width_pixel)
    board_scale = options.width_pixel / board_width_pixel
    board_root.moveto(0, 0, scale_x=board_scale, scale_y=board_scale)

    output_board_offset_left_pixel *= board_scale
    output_board_offset_top_pixel *= board_scale
    output_board_width_pixel *= board_scale
    output_board_height_pixel *= board_scale
    output_board_river_height_pixel *= board_scale

    # Initialize output figure
    output_fig = SVGFigure(Unit(f'{options.width_pixel}px'),
                           Unit(f'{options.width_pixel * height_factor}px'))
    output_fig.append([
        board_root,
    ])

    for _z_index, jobs in sorted(jobs_at_z_index.items()):
        for (x_rel, y_rel, filename, element_scale) in jobs:
            piece_fig = fromfile(filename)
            piece_root = piece_fig.getroot()
            original_piece_width_pixel, original_piece_height_pixel = \
                _pixel_viewbox_of_figure(piece_fig, options.resolution_dpi)[2:]

            # Scale and put piece onto board
            center_x_pixel = output_board_offset_left_pixel + output_board_width_pixel * x_rel
            center_y_pixel = output_board_offset_top_pixel + (output_board_height_pixel - output_board_river_height_pixel) * y_rel \
                    + (output_board_river_height_pixel if (y_rel >= 0.5) else 0.0)

            maximum_future_piece_width_pixel = output_board_width_pixel / _MAX_X * element_scale
            maximum_future_piece_height_pixel = output_board_height_pixel / _MAX_Y * element_scale

            scale = min(maximum_future_piece_width_pixel / original_piece_width_pixel,
                        maximum_future_piece_height_pixel / original_piece_height_pixel)

            future_piece_width_pixel = original_piece_width_pixel * scale
            future_piece_height_pixel = original_piece_height_pixel * scale

            x_pixel = center_x_pixel - future_piece_width_pixel / 2.0
            y_pixel = center_y_pixel - future_piece_height_pixel / 2.0
            piece_root.moveto(x_pixel, y_pixel, scale_x=scale, scale_y=scale)
            output_fig.append([
                piece_root,
            ])

    output_fig.save(options.output_file)
