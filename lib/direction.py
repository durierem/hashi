from enum import Enum


class Direction(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @staticmethod
    def opposite(direction):
        if direction == Direction.LEFT:
            return Direction.RIGHT
        if direction == Direction.UP:
            return Direction.DOWN
        if direction == Direction.RIGHT:
            return Direction.LEFT
        if direction == Direction.DOWN:
            return Direction.UP
        raise TypeError

    @staticmethod
    def add(direction, coord):
        addX, addY = direction.value
        x = addX + coord[0]
        y = addY + coord[1]
        return (x, y)
