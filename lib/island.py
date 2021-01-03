from lib.direction import Direction

# Représente une île de Hashiwokakero.
class Island:

    # CONSTANTES

    # Le nombre maximum de ponts entre deux îles.
    MAX_BRIDGES_BY_DIRECTION = 2

    # CONSTRUCTEUR

    # Créé une nouvelle île.
    #
    # maxBridges - Le nombre maximum de ponts reliés à l'île.
    def __init__(self, maxBridges):
        assert maxBridges > 0

        self.__maxBridges = maxBridges
        self.__totalBridges = 0
        self.__bridges = {
            Direction.LEFT: 0,
            Direction.UP: 0,
            Direction.RIGHT: 0,
            Direction.DOWN: 0,
        }

    # REQUÊTES

    # Renvoie une représentation textuelle de l'île.
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

    # Renvoie le nombre de ponts reliés à l'île dans une direction.
    #
    # direction - La Direction donnée.
    def getBridges(self, direction):
        return self.__bridges[direction]

    # Renvoie le nombre total de ponts reliés à l'île.
    def getTotalBridges(self):
        return self.__totalBridges

    # Renvoie le nombre maximum de ponts reliés à l'île.
    def getMaxBridges(self):
        return self.__maxBridges

    # Renvoie le nombre de ponts reliables à l'île dans une direction.
    #
    # direction - La Direction donnée.
    def getPossibleBridges(self, direction):
        return min(
            self.getMaxBridges() - self.getTotalBridges(),
            self.MAX_BRIDGES_BY_DIRECTION - self.getBridges(direction),
        )

    # Détermine si un île est pleine.
    def isFull(self):
        return self.getTotalBridges() == self.getMaxBridges()

    # COMMANDES

    # Ajoute un pont à l'île dans une direction.
    #
    # direction - La Direction donnée.
    def addBridge(self, direction):
        assert self.__canAddBridge(direction)
        self.__bridges[direction] += 1
        self.__totalBridges += 1

    # OUTILS

    def __canAddBridge(self, direction):
        isLegal = self.getBridges(direction) <= self.MAX_BRIDGES_BY_DIRECTION
        isNotFull = self.getTotalBridges() < self.getMaxBridges()
        return isLegal and isNotFull
