# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import re

from ..annotations import ANNOTATION_NAME_OF_ATOM_CODE, PutAnnotation
from ..parties import BLACK, RED
from ..pieces import PutPiece
from .fen import PIECE_OF_UPPER_LETTER

_piece_letters = list(
    PIECE_OF_UPPER_LETTER.keys()) + [letter.lower() for letter in PIECE_OF_UPPER_LETTER.keys()]
_escaped_annotation_names = [
    re.escape(atom_code) for atom_code in ANNOTATION_NAME_OF_ATOM_CODE.keys()
]

_single_piece_pattern = '[' + ''.join(_piece_letters) + ']'
_single_annotation_pattern = '<(?:' + '|'.join(_escaped_annotation_names) + ')>'
_single_annotation_plus_capture_pattern = _single_annotation_pattern.replace(
    '(?:', '(?P<atom_code>')
_atom_pattern = f'(?:{_single_piece_pattern}|{_single_annotation_pattern})'
_stacked_atoms_pattern = '\\[(?P<atoms>(?:' + _atom_pattern + ')+)\\]'

_annofen_tokens_pattern = '(?:' + '|'.join(f'(?P<{name}>{pattern})' for name, pattern in (
    ('end_of_row', '/'),
    ('empty_fields', '[0-9]'),
    ('single_piece', _single_piece_pattern),
    ('single_annotation', _single_annotation_plus_capture_pattern),
    ('stacked_atoms', _stacked_atoms_pattern),
    ('malformed', '.'),
)) + ')'
_atoms_tokens_pattern = '(?:' + '|'.join(f'(?P<{name}>{pattern})' for name, pattern in (
    ('single_piece', _single_piece_pattern),
    ('single_annotation', _single_annotation_plus_capture_pattern),
    ('malformed', '.'),
)) + ')'


def is_annofen_content(content: str) -> bool:
    return any(line.startswith('v1 ') for line in content.split('\n'))


def iterate_annofen_tokens(content: str):
    def _create_piece(x: int, y: int, letter: str) -> PutPiece:
        party = BLACK if letter.islower() else RED
        piece = PIECE_OF_UPPER_LETTER[letter.upper()]
        return PutPiece(party, piece, x, y)

    def _create_annotation(x: int, y: int, atom_code: str) -> PutAnnotation:
        annotation_name = ANNOTATION_NAME_OF_ATOM_CODE[atom_code]
        return PutAnnotation(annotation_name=annotation_name, x=x, y=y)

    seen_fen_before = False
    for i, line in enumerate(content.split('\n')):
        line = line.strip()

        if line.startswith('#') or not line:
            continue

        if not line.startswith('v1 '):
            raise ValueError(f'Malformed annoFEN: {line!r}')

        if seen_fen_before:
            raise ValueError(f'Garbage after annoFEN document: {line!r}')

        x = 0
        y = 9
        fen_part = line.split()[1]

        for match in re.finditer(_annofen_tokens_pattern, fen_part):
            if match.group('stacked_atoms') is not None:
                without_square_braces = match.group('atoms')
                for inner_match in re.finditer(_atoms_tokens_pattern, without_square_braces):
                    if inner_match.group('single_piece') is not None:
                        yield _create_piece(x, y, inner_match.group('single_piece'))
                    else:
                        yield _create_annotation(x, y, inner_match.group('atom_code'))
            elif match.group('end_of_row') is not None:
                x = 0
                y -= 1
                continue
            elif match.group('empty_fields') is not None:
                x += int(match.group('empty_fields'))
                continue
            elif match.group('single_piece') is not None:
                yield _create_piece(x, y, match.group('single_piece'))
            elif match.group('single_annotation') is not None:
                yield _create_annotation(x, y, match.group('atom_code'))
            elif match.group('malformed') is not None:
                character = match.group('malformed')
                raise ValueError(f'Malformed annoFEN token: {character!r}')
            x += 1

        seen_fen_before = True
