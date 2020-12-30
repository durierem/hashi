from direction import Direction

class Island():

    MAX_BRIDGES_BY_DIRECTION = 2

    # CONSTRUCTEUR

    def __init__(self, maxBridges):
        assert(maxBridges > 0)

        self.__maxBridges = maxBridges
        self.__totalBridges = 0
        self.__bridges = {
            Direction.LEFT: 0,
            Direction.UP: 0,
            Direction.RIGHT: 0,
            Direction.DOWN: 0
        }

    # REQUÊTES

    def __str__(self):
        return ("{maxBridges=" + str(self.__maxBridges) + ", bridges="
                + str(self.__bridges) + "}")

    def getBridges(self, direction):
        return self.__bridges[direction]

    def getTotalBridges(self):
        return self.__totalBridges

    def getMaxBridges(self):
        return self.__maxBridges

    # COMMANDES

    def addBridge(self, direction):
        assert(self.__canAddBridge(direction))
        self.__bridges[direction] += 1
        self.__totalBridges += 1

    # OUTILS

    def __canAddBridge(self, direction):
        isLegal = self.getNbBridges(direction) <= MAX_BRIDGES_BY_DIRECTION
        isNotFull = self.__totalBridges < self.__maxBridges
        return isLegal and isNotFull
