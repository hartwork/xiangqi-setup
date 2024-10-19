# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

ANNOTATION_NAME_BLANK_MOVE = "blank_move"
ANNOTATION_NAME_PIECE_MOVE = "piece_move"

ANNOTATION_NAME_OF_ATOM_CODE = {
    "a+0+1": "arrow_plus_0_plus_1",
    "a+0+2": "arrow_plus_0_plus_2",
    "a+0+3": "arrow_plus_0_plus_3",
    "a+0+4": "arrow_plus_0_plus_4",
    "a+0+5": "arrow_plus_0_plus_5",
    "a+0+6": "arrow_plus_0_plus_6",
    "a+0+7": "arrow_plus_0_plus_7",
    "a+0+8": "arrow_plus_0_plus_8",
    "a+0+9": "arrow_plus_0_plus_9",
    "a+0-1": "arrow_plus_0_minus_1",
    "a+0-2": "arrow_plus_0_minus_2",
    "a+0-3": "arrow_plus_0_minus_3",
    "a+0-4": "arrow_plus_0_minus_4",
    "a+0-5": "arrow_plus_0_minus_5",
    "a+0-6": "arrow_plus_0_minus_6",
    "a+0-7": "arrow_plus_0_minus_7",
    "a+0-8": "arrow_plus_0_minus_8",
    "a+0-9": "arrow_plus_0_minus_9",
    "a+1+0": "arrow_plus_1_plus_0",
    "a+1+1": "arrow_plus_1_plus_1",
    "a+1+2": "arrow_plus_1_plus_2",
    "a+1-1": "arrow_plus_1_minus_1",
    "a+1-2": "arrow_plus_1_minus_2",
    "a+2+0": "arrow_plus_2_plus_0",
    "a+2+1": "arrow_plus_2_plus_1",
    "a+2+2": "arrow_plus_2_plus_2",
    "a+2-1": "arrow_plus_2_minus_1",
    "a+2-2": "arrow_plus_2_minus_2",
    "a+3+0": "arrow_plus_3_plus_0",
    "a+4+0": "arrow_plus_4_plus_0",
    "a+5+0": "arrow_plus_5_plus_0",
    "a+6+0": "arrow_plus_6_plus_0",
    "a+7+0": "arrow_plus_7_plus_0",
    "a+8+0": "arrow_plus_8_plus_0",
    "a-1+0": "arrow_minus_1_plus_0",
    "a-1+1": "arrow_minus_1_plus_1",
    "a-1+2": "arrow_minus_1_plus_2",
    "a-1-1": "arrow_minus_1_minus_1",
    "a-1-2": "arrow_minus_1_minus_2",
    "a-2+0": "arrow_minus_2_plus_0",
    "a-2+1": "arrow_minus_2_plus_1",
    "a-2+2": "arrow_minus_2_plus_2",
    "a-2-1": "arrow_minus_2_minus_1",
    "a-2-2": "arrow_minus_2_minus_2",
    "a-3+0": "arrow_minus_3_plus_0",
    "a-4+0": "arrow_minus_4_plus_0",
    "a-5+0": "arrow_minus_5_plus_0",
    "a-6+0": "arrow_minus_6_plus_0",
    "a-7+0": "arrow_minus_7_plus_0",
    "a-8+0": "arrow_minus_8_plus_0",
    "bb": "blank_bad",
    "bg": "blank_good",
    "bm": ANNOTATION_NAME_BLANK_MOVE,
    "pb": "piece_bad",
    "pg": "piece_good",
    "pm": ANNOTATION_NAME_PIECE_MOVE,
}


class PutAnnotation:
    def __init__(self, annotation_name: str, x: float, y: float):
        self.annotation_name = annotation_name
        self.x = x
        self.y = y


class InvalidAnnotationCode(ValueError):
    def __init__(self, atom_code):
        super().__init__(f"Invalid annotation code {atom_code!r}")
