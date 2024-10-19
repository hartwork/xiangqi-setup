# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

(
    CHARIOT,
    HORSE,
    ELEPHANT,
    ADVISOR,
    KING,
    CANNON,
    PAWN,
) = list(range(7))


class PutPiece:
    def __init__(self, party, piece, x, y):
        self.party = party
        self.piece = piece
        self.x = x
        self.y = y

    def __str__(self):
        return "PutPiece(party=%s, piece=%s, x=%d, y=%d)" % (
            self.party,
            self.piece,
            self.x,
            self.y,
        )

    def __eq__(self, other):
        return (
            isinstance(other, PutPiece)
            and other.party == self.party
            and other.piece == self.piece
            and other.x == self.x
            and other.y == self.y
        )
