from enum import Enum


class Color(Enum):
    BLACK: tuple[int, int, int] = (0, 0, 0)
    GRAY: tuple[int, int, int] = (127, 127, 127)
    WHITE: tuple[int, int, int] = (255, 255, 255)
    RED: tuple[int, int, int] = (255, 0, 0)
    GREEN: tuple[int, int, int] = (0, 255, 0)
    BLUE: tuple[int, int, int] = (0, 0, 255)
    YELLOW: tuple[int, int, int] = (255, 255, 0)
    CYAN: tuple[int, int, int] = (0, 255, 255)
    MAGENTA: tuple[int, int, int] = (255, 0, 255)


class MoveDirection(Enum):
    UP: tuple[int, int] = (0, -1)
    DOWN: tuple[int, int] = (0, 1)
    LEFT: tuple[int, int] = (-1, 0)
    RIGHT: tuple[int, int] = (1, 0)


class SwitchMoveDirection(Enum):
    NO: str = 'no'
    BACK: str = 'back'
    RANDOM: str = 'random'
