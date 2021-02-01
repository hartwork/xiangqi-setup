# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from .parties import BLACK, RED
from .pieces import ADVISOR, CANNON, CHARIOT, ELEPHANT, HORSE, KING, PAWN, PutPiece


def iterate_default_setup():
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
