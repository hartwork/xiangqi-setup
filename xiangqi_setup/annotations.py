# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

ANNOTATION_NAME_OF_ATOM_CODE = {
    'bb': 'blank_bad',
    'bg': 'blank_good',
    'bm': 'blank_move',

    'pb': 'piece_bad',
    'pg': 'piece_good',
    'pm': 'piece_move',
}


class PutAnnotation:
    def __init__(self, annotation_name: str, x: float, y: float):
        self.annotation_name = annotation_name
        self.x = x
        self.y = y
