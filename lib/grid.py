from lib.cell import *
from lib.cursor import Cursor
from lib.direction import Direction


class Grid:

    # CONSTRUCTEUR

    def __init__(self, matrix):
        self.__matrix = matrix
        self.__cursor = Cursor(self)

    # ÉNUMÉRATEUR

    def __iter__(self):
        self.__current = Cursor(self)
        self.__x = 0
        self.__y = 0
        return self

    def __next__(self):
        if self.__y == self.getHeight():
            raise StopIteration

        self.__current.setCoord(self.__x, self.__y)
        self.__x = 0 if self.__x + 1 == self.getWidth() else self.__x + 1 
        self.__y += 1 if self.__x == 0 else 0

        return self.__current

    # REQUÊTES

    def getMatrix(self):
        self.__matrix

    def getWidth(self):
        return len(self.__matrix[0])

    def getHeight(self):
        return len(self.__matrix)

    def getCursor(self):
        return self.__cursor

    def getCell(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        x, y = c.getCoord()
        return self.__matrix[y][x]

    def getIsland(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        return self.getCell(c).getIsland()

    # OUTILS

    def __createPossibleBridges(self):
        l = []
        for i0 in range(3):
            buf = [0, 0, 0, 0]
            buf[0] = i0
            for i1 in range(3):
                buf[1] = i1
                for i2 in range(3):
                    buf[2] = i2
                    for i3 in range(3):
                        buf[3] = i3
                        l.append(buf[:])
        return l;

    def __createBridges(self):
        possibleBridges = self.__createPossibleBridges() # [:] ?

        leftBridges = self.__findPossibleBridges(Direction.LEFT)
        upBridges = self.__findPossibleBridges(Direction.UP)
        rightBridges = self.__findPossibleBridges(Direction.RIGHT)
        downBridges = self.__findPossibleBridges(Direction.DOWN)

        possibleBridges = [i for i in possibleBridges if i[0] <= leftBridges]
        possibleBridges = [i for i in possibleBridges if i[1] <= upBridges]
        possibleBridges = [i for i in possibleBridges if i[2] <= rightBridges]
        possibleBridges = [i for i in possibleBridges if i[3] <= downBridges]
        possibleBridges = [
            i
            for i in possibleBridges
            if sum(i)
            == self.getIsland().getMaxBridges() - self.getIsland().getTotalBridges()
        ]
        return possibleBridges

    def __findPossibleBridges(self, direction):
        c = Cursor(self, self.getCursor().getCoord())
        c.move(direction)

        while (
            self.getCell(c).getType() != CellType.ISLAND
            and (
                self.getCell(c).getType() != CellType.BRIDGE
                or self.getIsland().getBridges(direction) == 1
            )
            and c.canMove(direction)
        ):
            c.move(direction)

        if (
            # TODO: Redéfinir l'égalité de 2 curseurs comme en Java ?
            self.getCursor().getCoord() == c.getCoord()
            or self.getCell(c).getType() == CellType.BRIDGE
            or self.getCell(c).getType() == CellType.EMPTY
        ):
            return 0

        op = Direction.opposite(direction)
        return self.getIsland(c).getPossibleBridges(op)
