# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import yaml

from ..annotations import ANNOTATION_NAME_OF_ATOM_CODE, PutAnnotation
from ..parties import BLACK, RED
from ..pieces import PutPiece
from .fen import PIECE_OF_UPPER_LETTER


def is_xay_content(content: str) -> bool:
    try:
        document = yaml.safe_load(content)
        return isinstance(document, dict) and 'setup' in document
    except yaml.error.MarkedYAMLError:
        return False


def iterate_xay_tokens(content: str):
    document = yaml.safe_load(content)
    xay_format_version = document['version']
    if xay_format_version != '1':
        raise ValueError(f'Unsupported XAY file format version {xay_format_version!r}')

    annotation_matrix = document['setup']
    for row_index, annotations_of_column in enumerate(annotation_matrix):
        for column_index, atom_codes in enumerate(annotations_of_column):
            x = column_index
            y = 9 - row_index
            for atom_code in atom_codes:
                if atom_code.upper() in PIECE_OF_UPPER_LETTER:
                    party = BLACK if atom_code.islower() else RED
                    piece = PIECE_OF_UPPER_LETTER[atom_code.upper()]
                    yield PutPiece(party, piece, x, y)
                elif atom_code in ANNOTATION_NAME_OF_ATOM_CODE:
                    annotation_name = ANNOTATION_NAME_OF_ATOM_CODE[atom_code]
                    yield PutAnnotation(annotation_name=annotation_name, x=x, y=y)
                else:
                    raise ValueError(f'Unsupported atom code {atom_code!r}')
