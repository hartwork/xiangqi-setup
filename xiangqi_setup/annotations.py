# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

_ARROW_MINUS_3_PLUS_0 = 'arrow_minus_3_plus_0'
_ARROW_PLUS_1_MINUS_2 = 'arrow_plus_1_minus_2'
_BOTTOM_RIGHT_1 = 'bottom_right_1'
_BOTTOM_RIGHT_2 = 'bottom_right_2'
_SPOTLIGHT_BAD = 'spotlight_bad'
_SPOTLIGHT_GOOD = 'spotlight_good'

ANNOTATION_NAME_OF_ATOM_CODE = {
    'a-3+0': _ARROW_MINUS_3_PLUS_0,
    'a+1-2': _ARROW_PLUS_1_MINUS_2,

    'bb': 'blank_bad',
    'bg': 'blank_good',
    'bm': 'blank_move',

    'cb': 'carpet_bad',
    'cg': 'carpet_good',
    'cm': 'carpet_move',

    'sb': _SPOTLIGHT_BAD,
    'sg': _SPOTLIGHT_GOOD,

    'br1': _BOTTOM_RIGHT_1,
    'br2': _BOTTOM_RIGHT_2,

}

_ANNOTATIONS_NOT_TO_SCALE = {
    _ARROW_MINUS_3_PLUS_0,
    _ARROW_PLUS_1_MINUS_2,
}

_ANNOTATIONS_ABOVE_PIECE_LEVEL = {
    _ARROW_MINUS_3_PLUS_0,
    _ARROW_PLUS_1_MINUS_2,
    _BOTTOM_RIGHT_1,
    _BOTTOM_RIGHT_2,
    _SPOTLIGHT_BAD,
    _SPOTLIGHT_GOOD,
}


class PutAnnotation:
    def __init__(self, annotation_name: str, x: float, y: float):
        self.annotation_name = annotation_name
        self.x = x
        self.y = y
        self.allow_scaling = annotation_name not in _ANNOTATIONS_NOT_TO_SCALE
        self.above_pieces = annotation_name in _ANNOTATIONS_ABOVE_PIECE_LEVEL
