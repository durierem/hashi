from enum import Enum

from island import Island

class CellType(Enum):
    EMPTY = 0
    BRIDGE = 1
    ISLAND = 2

class Cell():
    def __init__(self, island = None):
        assert(island == None or type(island) == Island)
        self.__type = CellType.ISLAND if island !=  None else CellType.EMPTY
        self.__island = island

    def __str__(self):
        return ("{type=" + str(self.__type)+ ", island="
                + str(self.__island) + "}")

    def getType(self):
        return self.__type

    def getIsland(self):
        assert(self.getType() == CellType.ISLAND)
        return self.__island

    def isEmpty(self):
        return self.__type == CellType.EMPTY

    def setType(self, cellType):
        assert(type(cellType) == CellType)
        self.__type = cellType
