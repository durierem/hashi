from enum import Enum

class Direction(Enum):
    LEFT = (0, -1)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)

    @staticmethod
    def opposite(direction):
        if direction ==  Direction.LEFT:
            return Direction.RIGHT
        if direction == Direction.UP:
            return Direction.DOWN
        if direction == Direction.RIGHT:
            return Direction.LEFT
        if direction == Direction.DOWN:
            return Direction.UP
        raise TypeError
