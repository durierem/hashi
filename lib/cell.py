from enum import Enum

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


# Modélise une cellule.
#
# @inv:
#       getType() == CellType.ISLAND <=> getIsland() != None
#       getType() != CellType.ISLAND <=> getIsland() == None
class Cell:

    # CONSTRUCTEUR

    # Créé une nouvelle cellule.
    #
    # @post
    #       island == None => getType() == CellType.EMPTY
    #       island != None => getType() == CellType.ISLAND
    def __init__(self, island=None):
        self.__type = CellType.ISLAND if island != None else CellType.EMPTY
        self.__island = island

    # REQUÊTES

    # Renvoie une chaîne de caractère décrivant la cellule.
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

    # Renvoie le type de la cellule.
    def getType(self):
        return self.__type

    # Renvoie l'île associée à la cellule.
    def getIsland(self):
        return self.__island

    # COMMANDES

    # Modifie le type de la cellule.
    #
    # @pre
    #       cellType == CellType.ISLAND <=> island != None
    # @post
    #       getType() == cellType
    #       getIsland() == island
    def setType(self, cellType, island=None):
        if cellType == CellType.ISLAND:
            assert island != None
        else:
            assert island == None

        self.__type = cellType
        self.__island = island

    # Modifie l'île associée à la cellule.
    #
    # @pre
    #       getType() == CellType.ISLAND
    # @post
    #       getType() == old getType()
    #       getIsland() == island
    def setIsland(self, island):
        assert self.getType() == CellType.ISLAND
        self.__island = island
