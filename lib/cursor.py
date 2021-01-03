from lib.direction import Direction

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
        x, y = self.__coord
        width = self.getGrid().getWidth()
        height = self.getGrid().getHeight()
        return (
            not (direction == Direction.LEFT and x == 0)
            and not (direction == Direction.UP and y == 0)
            and not (direction == Direction.RIGHT and x == width - 1)
            and not (direction == Direction.DOWN and y == height - 1)
        )

    # COMMANDES

    # Définit les nouvelles coordonnées du curseur.
    #
    # coord - Le Tuple de coordonnées auxquelles déplacer le curseur.
    def setCoord(self, coord):
        x, y = coord
        assert x <= self.getGrid().getWidth(), "Coordonnée X incorrecte"
        assert y <= self.getGrid().getHeight(), "Coordonnée Y incorrecte"
        self.__coord = (x, y)

    # Déplace le curseur d'une cellule dans une direction.
    #
    # direction - La Direction dans laquelle déplacer le curseur.
    def move(self, direction):
        assert self.canMove(direction), "Impossible de déplacer le curseur"
        self.__coord = Direction.add(direction, self.__coord)

    # Déplace le curseur sur la première cellule de la ligne du dessous.
    def nextLine(self):
        self.__coord = (0, self.getCoordY + 1)
