from lib.direction import Direction


# Représente une île de Hashiwokakero.
#
# @inv
#       0 <= totalBridges() <= maxBridges()
#       for d in Direction:
#           0 <= getBridges(d) <= MAX_BRIDGES_BY_DIRECTION
class Island:

    # CONSTANTES

    MAX_BRIDGES_BY_DIRECTION = 2

    # CONSTRUCTEUR

    def __init__(self, maxBridges):
        assert maxBridges > 0

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
        return (
            "<Island: id="
            + str(id(self))
            + ", maxBridges="
            + str(self.getMaxBridges())
            + ", totalBridges="
            + str(self.getTotalBridges())
            + ">"
        )

    def getBridges(self, direction):
        return self.__bridges[direction]

    def getTotalBridges(self):
        return self.__totalBridges

    def getMaxBridges(self):
        return self.__maxBridges

    def getPossibleBridges(self, direction):
        return min(
            self.getMaxBridges() - self.getTotalBridges(),
            MAX_BRIDGES_BY_DIRECTION - self.getBridges(direction)
        )

    # COMMANDES

    def addBridge(self, direction):
        assert self.__canAddBridge(direction)
        self.__bridges[direction] += 1
        self.__totalBridges += 1

    # OUTILS

    def __canAddBridge(self, direction):
        isLegal = self.getNbBridges(direction) <= MAX_BRIDGES_BY_DIRECTION
        isNotFull = self.getTotalBridges() < self.getMaxBridges()
        return isLegal and isNotFull
