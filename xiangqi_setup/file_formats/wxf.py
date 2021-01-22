# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import re
import sys

from ..default_setup import iterate_default_setup
from ..file_formats.fen import iterate_fen_tokens, PIECE_OF_UPPER_LETTER
from ..parties import RED, BLACK
from ..pieces import PutPiece

START_PARTY_RED = 'RED'
START_PARTY_BLACK = 'BLACK'


_SETUP_EXTRACTOR = re.compile('SETUP\\{([^}]+)}', re.MULTILINE)
_ITEM_ITERATOR = re.compile('(?P<put_piece>[RHEAKCPrheakcp][a-i][0-9])|(?P<move_offset>MOVE [1-9][0-9]*)|(?P<start_party>RED|BLACK)')
_FEN_ELEMENT_PATERN = '[RHEAKCPNBrheakcpnb1-9]+'
_FEN_EXTRACTOR = re.compile('^FEN[ \\t]+(?P<field_state>%s(?:/%s){9})( [rb])?' % (_FEN_ELEMENT_PATERN, _FEN_ELEMENT_PATERN), re.MULTILINE)


def iterate_wxf_tokens(content):
    fen_match = _FEN_EXTRACTOR.search(content)
    if fen_match:
        field_state_raw = fen_match.groupdict()['field_state']
        yield from iterate_fen_tokens(field_state_raw)
        return

    setup_match = _SETUP_EXTRACTOR.search(content)
    if not setup_match:
        print('No custom setup found, assuming default setup.', file=sys.stderr)
        for put_piece in iterate_default_setup():
            yield put_piece
        return

    setup_body = setup_match.group(1)
    for item_match in re.finditer(_ITEM_ITERATOR, setup_body):
        gd = item_match.groupdict()
        if gd['put_piece']:
            piece_letter, x_lower_alpha, y_0_9 = gd['put_piece']

            party = BLACK if piece_letter.islower() else RED
            piece = PIECE_OF_UPPER_LETTER[piece_letter.upper()]
            x = ord(x_lower_alpha) - ord('a')
            y = int(y_0_9)

            yield PutPiece(party, piece, x, y)
