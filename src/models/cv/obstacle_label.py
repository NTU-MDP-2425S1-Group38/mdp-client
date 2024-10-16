from enum import Enum
from typing import Dict

import torch


class ObstacleLabel(str, Enum):
    """
    Label of the image on the obstacle.
    """
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    Number_1 = "1"
    Number_2 = "2"
    Number_3 = "3"
    Number_4 = "4"
    Number_5 = "5"
    Number_6 = "6"
    Number_7 = "7"
    Number_8 = "8"
    Number_9 = "9"
    Shape_Bullseye = "BULLSEYE"
    Shape_Circle = "CIRCLE"
    Shape_Up = "UP"
    Shape_Down = "DOWN"
    Shape_Left = "LEFT"
    Shape_Right = "RIGHT"
    Unknown = "UNKNOWN"



_label_map: Dict[ObstacleLabel, int] = {
    ObstacleLabel.A: 20,
    ObstacleLabel.B: 21,
    ObstacleLabel.C: 22,
    ObstacleLabel.D: 23,
    ObstacleLabel.E: 24,
    ObstacleLabel.F: 25,
    ObstacleLabel.G: 26,
    ObstacleLabel.H: 27,
    ObstacleLabel.S: 28,
    ObstacleLabel.T: 29,
    ObstacleLabel.U: 30,
    ObstacleLabel.V: 31,
    ObstacleLabel.W: 32,
    ObstacleLabel.X: 33,
    ObstacleLabel.Y: 34,
    ObstacleLabel.Z: 35,
    ObstacleLabel.Number_1: 11,
    ObstacleLabel.Number_2: 12,
    ObstacleLabel.Number_3: 13,
    ObstacleLabel.Number_4: 14,
    ObstacleLabel.Number_5: 15,
    ObstacleLabel.Number_6: 16,
    ObstacleLabel.Number_7: 17,
    ObstacleLabel.Number_8: 18,
    ObstacleLabel.Number_9: 19,
    ObstacleLabel.Shape_Up: 36,
    ObstacleLabel.Shape_Down: 37,
    ObstacleLabel.Shape_Right: 38,
    ObstacleLabel.Shape_Left: 39,
    ObstacleLabel.Shape_Circle: 40,
    ObstacleLabel.Shape_Bullseye: 100,
    ObstacleLabel.Unknown: 404,
}

_cv_cls_id_map: Dict[int, str] = {
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
    8: '9',
    9: 'A',
    10: 'B',
    11: 'BULLSEYE',
    12: 'C',
    13: 'CIRCLE',
    14: 'D',
    15: 'DOWN',
    16: 'E',
    17: 'F',
    18: 'G',
    19: 'H',
    20: 'LEFT',
    21: 'RIGHT',
    22: 'S',
    23: 'T',
    24: 'U',
    25: 'UP',
    26: 'V',
    27: 'W',
    28: 'X',
    29: 'Y',
    30: 'Z'
}


def ObstacleLabelToId(label: ObstacleLabel) -> int:

    if label in _label_map:
        return _label_map[label]
    else:
        return _label_map[ObstacleLabel.Unknown]


def ModelClsToId(cls: int) -> int:

    assert cls in _cv_cls_id_map.keys(), "Image label class not found!"

    return ObstacleLabelToId(
        ObstacleLabel(
            _cv_cls_id_map[cls]
        )
    )
