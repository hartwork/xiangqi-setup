# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from ..parties import BLACK, RED
from ..pieces import ADVISOR, CANNON, CHARIOT, ELEPHANT, HORSE, KING, PAWN, PutPiece

PIECE_OF_UPPER_LETTER = {
    # Official letters from http://wxf.ca/xq/computer/fen.pdf
    'R': CHARIOT,  # "r" is for "rook"
    'H': HORSE,
    'E': ELEPHANT,
    'A': ADVISOR,
    'K': KING,
    'C': CANNON,
    'P': PAWN,

    # As seen at https://www.chessdb.cn/query_en/
    'N': HORSE,  # "n" is for "k[n]ight"; "k" is taken by "king"
    'B': ELEPHANT,  # "b" for "bishop"

    # As seen at http://wxf.ca/xq/computer/wxf_format.pdf
    'G': ADVISOR,  # "g" for "guard"
    'M': ELEPHANT,  # "m" for "minister"
}


def iterate_fen_tokens(field_state_raw):
    # Make sure we're only operating on the first part the FEN,
    # the piece setup matrix (empty board: "9/9/9/9/9/9/9/9/9/9 w - - 0 1")
    field_state_raw = field_state_raw.split()[0]

    for i, line in enumerate(field_state_raw.split('/')):
        x = 0
        for char in line:
            try:
                x += int(char)
            except ValueError:
                party = BLACK if char.islower() else RED
                piece = PIECE_OF_UPPER_LETTER[char.upper()]
                y = 9 - i
                p = PutPiece(party, piece, x, y)
                yield p
                x += 1
