from enum import Enum
from lib.island import Island


class CellType(Enum):
    EMPTY = 0
    BRIDGE = 1
    ISLAND = 2


class Cell:
    def __init__(self, island=None):
        self.__type = CellType.ISLAND if island != None else CellType.EMPTY
        self.__island = island

    def __str__(self):
        return (
            "<Cell: id="
            + str(id(self))
            + ", type="
            + str(self.getType())
            + ", island="
            + str(self.getIsland())
            + ">"
        )

    def getType(self):
        return self.__type

    def getIsland(self):
        return self.__island

    def setType(self, cellType):
        self.__type = cellType
        if (cellType != CellType.ISLAND):
            self.__island = None

    def setIsland(self, island):
        assert self.getType() == CellType.ISLAND
        self.__island = island
