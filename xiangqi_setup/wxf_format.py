# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import re


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


def iterate_wxf_tokens(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()

    setup_match = _SETUP_EXTRACTOR.search(content)
    if not setup_match:
        raise ValueError('Setup section ("SETUP{..}") missing')

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
