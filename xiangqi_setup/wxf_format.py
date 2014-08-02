# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import re
import sys


CHARIOT, \
HORSE, \
ELEPHANT, \
ADVISOR, \
KING, \
CANNON, \
PAWN, \
= range(7)

RED, \
BLACK, \
= range(2)

START_PARTY_RED = 'RED'
START_PARTY_BLACK = 'BLACK'


_SETUP_EXTRACTOR = re.compile('SETUP\\{([^}]+)}', re.MULTILINE)
_ITEM_ITERATOR = re.compile('(?P<put_piece>[RHEAKCPrheakcp][a-i][0-9])|(?P<move_offset>MOVE [1-9][0-9]*)|(?P<start_party>RED|BLACK)')
_FEN_ELEMENT_PATERN = '[RHEAKCPrheakcp1-9]+'
_FEN_EXTRACTOR = re.compile('^FEN[ \\t]+(?P<field_state>%s(?:/%s){9})( [rb])?' % (_FEN_ELEMENT_PATERN, _FEN_ELEMENT_PATERN), re.MULTILINE)


_PIECE_OF_UPPER_LETTER = {
    'R': CHARIOT,
    'H': HORSE,
    'E': ELEPHANT,
    'A': ADVISOR,
    'K': KING,
    'C': CANNON,
    'P': PAWN,
}


class PutPiece(object):
    def __init__(self, party, piece, x, y):
        self.party = party
        self.piece = piece
        self.x = x
        self.y = y

    def __str__(self):
        return 'PutPiece(party=%s, piece=%s, x=%d, y=%d)' \
                % (self.party, self.piece, self.x, self.y)


def _iterate_default_setup():
    for party, piece, x, y in (
            (RED, CHARIOT, 0, 0),
            (RED, HORSE, 1, 0),
            (RED, ELEPHANT, 2, 0),
            (RED, ADVISOR, 3, 0),
            (RED, KING, 4, 0),
            (RED, ADVISOR, 5, 0),
            (RED, ELEPHANT, 6, 0),
            (RED, HORSE, 7, 0),
            (RED, CHARIOT, 8, 0),

            (RED, CANNON, 1, 2),
            (RED, CANNON, 7, 2),

            (RED, PAWN, 0, 3),
            (RED, PAWN, 2, 3),
            (RED, PAWN, 4, 3),
            (RED, PAWN, 6, 3),
            (RED, PAWN, 8, 3),

            (BLACK, CHARIOT, 0, 9),
            (BLACK, HORSE, 1, 9),
            (BLACK, ELEPHANT, 2, 9),
            (BLACK, ADVISOR, 3, 9),
            (BLACK, KING, 4, 9),
            (BLACK, ADVISOR, 5, 9),
            (BLACK, ELEPHANT, 6, 9),
            (BLACK, HORSE, 7, 9),
            (BLACK, CHARIOT, 8, 9),

            (BLACK, CANNON, 1, 7),
            (BLACK, CANNON, 7, 7),

            (BLACK, PAWN, 0, 6),
            (BLACK, PAWN, 2, 6),
            (BLACK, PAWN, 4, 6),
            (BLACK, PAWN, 6, 6),
            (BLACK, PAWN, 8, 6),
            ):
        yield PutPiece(party, piece, x, y)


def iterate_wxf_tokens(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()

    fen_match = _FEN_EXTRACTOR.search(content)
    if fen_match:
        field_state_raw = fen_match.groupdict()['field_state']
        for i, line in enumerate(field_state_raw.split('/')):
            x = 0
            for char in line:
                try:
                    x += int(char)
                except ValueError:
                    party = BLACK if char.islower() else RED
                    piece = _PIECE_OF_UPPER_LETTER[char.upper()]
                    y = 9 - i
                    p = PutPiece(party, piece, x, y)
                    yield p
                    x += 1
        return

    setup_match = _SETUP_EXTRACTOR.search(content)
    if not setup_match:
        print('No custom setup found, assuming default setup.', file=sys.stderr)
        for put_piece in _iterate_default_setup():
            yield put_piece
        return

    setup_body = setup_match.group(1)
    for item_match in re.finditer(_ITEM_ITERATOR, setup_body):
        gd = item_match.groupdict()
        if gd['put_piece']:
            piece_letter, x_lower_alpha, y_0_9 = gd['put_piece']

            party = BLACK if piece_letter.islower() else RED
            piece = _PIECE_OF_UPPER_LETTER[piece_letter.upper()]
            x = ord(x_lower_alpha) - ord('a')
            y = int(y_0_9)

            yield PutPiece(party, piece, x, y)
