from enum import Enum


class ActionType(Enum):  # pierwszy znak - kierunek, drugi - rodzaj ruchu
    Up = '-11'
    Right = '+10'
    Down = '+11'
    Left = '-10'
