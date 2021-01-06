from lib.cell import CellType
from lib.direction import Direction

class EndOfGridException(Exception):
    pass

# Modélise un curseur associé à une grille.
class Cursor:

    # CONSTRUCTEUR

    # Créé un nouveau curseur sur une grille.
    #
    # grid - La Grid à laquelle associer le curseur.
    # coord - Un Tuple de coordonnées (x, y).
    def __init__(self, grid, coord=(0, 0)):
        self.__grid = grid
        self.__coord = coord

    # REQUÊTES

    # Renvoie une représentation textuelle du curseur.
    def __str__(self):
        return "<Cursor: coord=" + str(self.__coord) + ">"

    # Redéfinit l'opérateur "==" pour les Cursor.
    #
    # Deux curseurs sont égaux si ils sont associés à la même grille et ont les
    # mêmes coordonnées.
    def __eq__(self, obj):
        return (
            type(obj) == Cursor
            and obj.getGrid() == self.getGrid()
            and obj.getCoord() == self.getCoord()
        )

    # Redéfinit l'opérateur "!=" pour les Cursor.
    def __ne__(self, obj):
        return not self == obj

    # Renvoie le Tuple de coordonnées (x, y) indiquant la position du curseur.
    def getCoord(self):
        return self.__coord

    # Renvoie la coordonnée x.
    def getCoordX(self):
        return self.__coord[0]

    # Renvoie la coordonnée y.
    def getCoordY(self):
        return self.__coord[1]

    # Renvoie la Grid associée au curseur.
    def getGrid(self):
        return self.__grid

    # Renvoie la Cell de la grille aux coordonnées pointées par le curseur.
    def getCell(self):
        return self.getGrid().getCell(self)

    # Représente la capacité du curseur à se déplacer dans une direction.
    #
    # Le curseur ne peut pas se déplacer dans une direction donnée lorsqu'il
    # est positionné aux bords de la grille.
    #
    # direction - La Direction a tester.
    def canMove(self, direction):
        x, y = Direction.add(direction, self.__coord) 
        if x < 0 or x >= self.getGrid().getWidth(): return False
        if y < 0 or y >= self.getGrid().getHeight(): return False 
        return True

    # COMMANDES

    # Définit les nouvelles coordonnées du curseur.
    #
    # coord - Le Tuple de coordonnées auxquelles déplacer le curseur.
    def setCoord(self, coord):
        x, y = coord
        assert x <= self.getGrid().getWidth(), "Invalid X coordinate"
        assert y <= self.getGrid().getHeight(), "Invalid Y coordinate"
        self.__coord = (x, y)

    # Déplace le curseur d'une cellule dans une direction.
    #
    # direction - La Direction dans laquelle déplacer le curseur.
    def move(self, direction):
        assert self.canMove(direction), "Invalid direction"
        self.__coord = Direction.add(direction, self.__coord)

    # Déplace le curseur sur la première cellule de la ligne du dessous.
    def nextLine(self):
        self.__coord = (0, self.getCoordY() + 1)

    def goToNextCell(self):
        if self.canMove(Direction.RIGHT):
            self.move(Direction.RIGHT)
        else:
            if self.canMove(Direction.DOWN):
                self.nextLine()
            else:
                raise EndOfGridException

    def goToNextIsland(self):
         while True:
            self.goToNextCell()
            if self.getCell().getType() == CellType.ISLAND:
                break
