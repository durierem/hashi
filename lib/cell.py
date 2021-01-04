from enum import Enum

from lib.direction import Direction
from lib.island import Island

# Modélise les 3 types de cellules possibles.
#
# EMPTY     La cellule ne contient rien
# BRIDGE    La cellule contient une portion d'un ou plusieurs pont(s)
# ISLAND    La cellule contient une île
class CellType(Enum):
    EMPTY = 0
    BRIDGE = 1
    ISLAND = 2


# Modélise une cellule de Hashiwokakero.
class Cell:

    # CONSTRUCTEUR

    # Créé une nouvelle cellule.
    #
    # Si une île est précisée en paramètre, le type de la nouvelle cellule est
    # CellType.ISLAND. Sinon le type est CellType.EMPTY.
    #
    # island - L'Island à associer à la cellule (défaut : None)
    def __init__(self, island=None):
        # Type
        self.__type = CellType.ISLAND if island != None else CellType.EMPTY

        # Île
        self.__island = island

        # Pont
        self.__dual = False
        self.__direction = None

    # REQUÊTES

    # Renvoie une chaîne de caractère décrivant la cellule.
    def __str__(self):
        return (
            "<Cell: id="
            + str(id(self))
            + ", type="
            + str(self.__type)
            + ", island="
            + str(self.__island)
            + ">"
        )

    # Renvoie le type de la cellule.
    def getType(self):
        return self.__type

    # Renvoie l'île associée à la cellule.
    def getIsland(self):
        return self.__island

    # COMMANDES

    def display(self):
        if self.__type == CellType.ISLAND:
            print(" " + str(self.__island.getMaxBridges()) + " ", end="")
        elif self.__type == CellType.BRIDGE:
            if self.__direction in [Direction.RIGHT, Direction.LEFT]:
                print("═══" if self.__dual else "───", end="")
            elif self.__direction in [Direction.UP, Direction.DOWN]:
                print(" ║ " if self.__dual else " │ ", end="")
        elif self.__type == CellType.EMPTY:
            print("   ", end="")

    # Modifie le type de la cellule.
    #
    # cellType - Le nouveau CellType de la cellule.
    # island - L'Island à associer à la cellule si son nouveau type est
    #          CellType.ISLAND (défaut : None).
    def setType(self, cellType, island=None):
        if cellType == CellType.ISLAND:
            assert island != None, "None argument: 'island'"
        else:
            assert island == None, "Not None argument: 'island'"

        self.__type = cellType
        self.__island = island

    # Modifie l'île associée à la cellule.
    #
    # island - L'Island à associer à la cellule.
    def setIsland(self, island):
        assert self.getType() == CellType.ISLAND, "cell type is not 'CellType.ISLAND'"
        self.__island = island

    def setDual(self):
        assert self.getType() == CellType.BRIDGE, "cell type is not 'CellType.BRIDGE'"
        self.__dual = True

    def setDirection(self, direction):
        assert self.getType() == CellType.BRIDGE, "cell type is not 'CellType.BRIDGE'"
        self.__direction = direction
