from lib.cell import *

class Grid:
    def __init__(self, cellMatrix):
        self.__matrix = cellMatrix

    def __iter__(self):
        self.__current = Cell(CellType.EMPTY)
        self.__line = 0
        self.__col = 0
        return self

    def __next__(self):
        if (self.__line == self.getHeight()):
            raise StopIteration

        self.__current = self.__matrix[self.__line][self.__col]
        self.__col = 0 if self.__col + 1 == self.getWidth() else self.__col + 1
        self.__line += 1 if self.__col == 0 else 0

        return self.__current

    def getMatrix(self):
        self.__matrix

    def getWidth(self):
        return len(self.__matrix[0])

    def getHeight(self):
        return len(self.__matrix)

    def getCell(self, x, y):
        return self.__matrix[x][y]

