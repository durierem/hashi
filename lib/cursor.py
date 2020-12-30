from lib.direction import Direction


class Cursor:

    # CONSTRUCTEUR

    def __init__(self, grid, coord=(0, 0)):
        self.__grid = grid
        self.__coord = coord

    # REQUÊTES

    def __str__(self):
        return "<Cursor: coord=" + str(self.__coord) + ">"

    def getCoord(self):
        return self.__coord

    def getGrid(self):
        return self.__grid

    def getCell(self):
        return self.getGrid().getCell(self)

    def canMove(self, direction):
        x, y = self.__coord
        width = self.getGrid().getWidth()
        height = self.getGrid().getHeight()
        return (
            not (direction == Direction.LEFT and x == 0)
            and not (direction == Direction.UP and y == 0)
            and not (direction == Direction.RIGHT and x == width - 1)
            and not (direction == Direction.DOWN and y == height - 1)
        )

    # COMMANDES

    def setCoord(self, x, y):
        assert x <= self.getGrid().getWidth()
        assert y <= self.getGrid().getHeight()
        self.__coord = (x, y)

    def move(self, direction):
        assert self.canMove(direction)
        self.__coord = Direction.add(direction, self.__coord)
