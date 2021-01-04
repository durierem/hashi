import copy

from lib.cell import *
from lib.cursor import Cursor
from lib.direction import Direction
from lib.island import Island

# Modélise une grille de Hashiwokakero.
class Grid:

    allBridgeCombinations = None

    # CONSTRUCTEUR

    # Créé un nouvelle grille à partir de la liste donnée.
    #
    # matrix - La réprésentation d'une grille de hashi par une liste à deux
    #          dimensions dans laquelle, un 0 représente une case vide et un
    #          chiffre strictement positif et le nombre de ponts associés.
    def __init__(self, matrix):
        self.__matrix = matrix
        self.__cursor = Cursor(self)
        self.allBridgeCombinations = self.__createAllBridgeCombinations()

    # ÉNUMÉRATEUR

    # Une grille peut être énuméré au moyen d'un curseur qui la parcours de
    # bas en haut et de gauche à droite.
    #
    # Exemple :
    #       for cursor in grid:
    #           print(cursor.getCell())
    def __iter__(self):
        self.__current = Cursor(self)
        self.__x = 0
        self.__y = 0
        return self

    def __next__(self):
        if self.__y == self.getHeight():
            raise StopIteration

        self.__current.setCoord((self.__x, self.__y))
        self.__x = 0 if self.__x + 1 == self.getWidth() else self.__x + 1
        self.__y += 1 if self.__x == 0 else 0

        return self.__current

    # REQUÊTES

    def __str__(self):
        return (
            "<Grid: id="
            + str(id(self))
            + ", cursor="
            + str(self.__cursor)
            + ", matrix="
            + str(self.__matrix)
            + ">"
        )

    # Renvoie la matrice associée à la grille.
    def getMatrix(self):
        self.__matrix

    # Renvoie la largeur de la grille.
    def getWidth(self):
        return len(self.__matrix[0])

    # Renvoie la hauteur de la grille.
    def getHeight(self):
        return len(self.__matrix)

    # Renvoie le curseur principal associé à la grille.
    def getCursor(self):
        return self.__cursor

    # Renvoie la cellule pointée par un curseur.
    #
    # cursor - Le Cursor à utiliser. Si aucune curseur n'est précisé, le
    #          curseur utilisé est celui renvoyé par getCursor() (défaut: None)
    def getCell(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        x, y = c.getCoord()
        return self.__matrix[y][x]

    # Renvoie l'île située sur la cellule pointée par un curseur.
    #
    # cursor - Le Cursor à utiliser. Si aucune curseur n'est précisé, le
    #          curseur utilisé est celui renvoyé par getCursor() (défaut: None)
    def getIsland(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        return self.getCell(c).getIsland()

    # Affiche la grille.
    def display(self):
        for c in self:
            c.getCell().display()
            if not c.canMove(Direction.RIGHT):
                print("")

    # Renvoie la grille résolue ou None s'il n'existe pas de solution.
    def solve(self):
        if self.getCell().getType() != CellType.ISLAND:
            if self.__hasNextIsland():
                self.__goToNextIsland()
            else:
                return self
        grid = self.__createGrids()
        for i in grid:
            if not i.__hasNextIsland():
                return i
            i.__goToNextIsland()
        while grid:
            g = grid[0]
            del grid[0]
            buf = g.__createGrids()
            for i in buf:
                if not i.__hasNextIsland():
                    return i
                i.__goToNextIsland()
                grid.append(i)
        return None

    # OUTILS

    def __createAllBridgeCombinations(self):
        l = []
        for i0 in range(3):
            buf = {
                Direction.LEFT: 0,
                Direction.UP: 0,
                Direction.RIGHT: 0,
                Direction.DOWN: 0,
            }
            buf[Direction.LEFT] = i0
            for i1 in range(3):
                buf[Direction.UP] = i1
                for i2 in range(3):
                    buf[Direction.RIGHT] = i2
                    for i3 in range(3):
                        buf[Direction.DOWN] = i3
                        l.append(buf.copy())
        return l

    # Renvoie une liste composée de nouvelles grilles construites à partir de
    # la grille actuelle en ajoutant les ponts posibles à l'île pointée par
    # le curseur de la grille actuelle.
    def __createGrids(self):
        combinations = self.allBridgeCombinations.copy()

        # Les curseurs vers les îles voisines de l'île courante.
        neighborCursors = {
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None,
        }

        # ...
        for d in Direction:
            neighborCursors[d] = self.__findNeighbor(d)
            op = Direction.opposite(d)
            if neighborCursors[d] != None:
                combinations = [
                    i
                    for i in combinations
                    if i[d] <= self.getIsland(neighborCursors[d]).getPossibleBridges(op)
                ]
            else:
                combinations = [i for i in combinations if i[d] <= 0]

        # ...
        combinations = [
            i
            for i in combinations
            if sum(i.values())
            == self.getIsland().getMaxBridges() - self.getIsland().getTotalBridges()
        ]

        # ...
        newGrids = []
        for i in combinations:
            g = copy.deepcopy(self)
            for d in Direction:
                op = Direction.opposite(d)
                if i[d] != 0:
                    for k in range(i[d]):
                        g.getIsland().addBridge(d)
                        g.getIsland(neighborCursors[d]).addBridge(op)
                    c = Cursor(g, self.getCursor().getCoord())
                    isDual = (
                        True
                        if c.getCell().getIsland().getBridges(d)
                        == Island.MAX_BRIDGES_BY_DIRECTION
                        else False
                    )
                    c.move(d)
                    while g.getCell(c).getType() != CellType.ISLAND:
                        g.getCell(c).setType(CellType.BRIDGE)
                        g.getCell(c).setDirection(d)
                        if isDual:
                            g.getCell(c).setDual()
                        c.move(d)
            newGrids.append(g)
        return newGrids

    # S'il existe une île pouvant être reliée à celle pointée par le curseur
    # actuel dans la direction donnée, renvoie un curseur pointant sur ses
    # cooronnées. Sinon renvoie None.
    def __findNeighbor(self, direction):
        c = Cursor(self, self.getCursor().getCoord())
        if c.canMove(direction):
            c.move(direction)

        while (
            self.getCell(c).getType() != CellType.ISLAND
            and (
                self.getCell(c).getType() != CellType.BRIDGE
                or self.getIsland().getBridges(direction) == 1
            )
            and c.canMove(direction)
        ):
            c.move(direction)

        if (
            self.getCursor() == c
            or self.getCell(c).getType() == CellType.BRIDGE
            or self.getCell(c).getType() == CellType.EMPTY
        ):
            return None

        return c

    def __hasNextIsland(self, cursor=None):
        c = (
            Cursor(self, cursor.getCoord())
            if cursor != None
            else Cursor(self, self.getCursor().getCoord())
        )
        if c.canMove(Direction.RIGHT):
            c.move(Direction.RIGHT)
        else:
            if c.canMove(Direction.DOWN):
                c.setCoord((0, c.getCoordY() + 1))
            else:
                return False
        while c.getCell().getType() != CellType.ISLAND:
            if c.canMove(Direction.RIGHT):
                c.move(Direction.RIGHT)
            else:
                if c.canMove(Direction.DOWN):
                    c.setCoord((0, c.getCoordY() + 1))
                else:
                    return False
        if (
            c.getCell().getIsland().getMaxBridges()
            - c.getCell().getIsland().getTotalBridges()
            == 0
        ):
            return self.__hasNextIsland(c)
        return True

    def __goToNextIsland(self):
        c = self.getCursor()

        # while (c.canMove(Direction.RIGHT)):
        #     c.move(Direction.RIGHT)
        #     if (c.getCell().getType() == CellType.ISLAND):
        #         if (c.getCell().getIsland().isFull()):
        #             self.__goToNextIsland(c)
        #         else:
        #             return
        # if (c.canMove(Direction.DOWN)):
        #     c.nextLine()
        #     self.__goToNextIsland()

        if c.canMove(Direction.RIGHT):
            c.move(Direction.RIGHT)
        else:
            if c.canMove(Direction.DOWN):
                c.nextLine()

        while c.getCell().getType() != CellType.ISLAND:
            if c.canMove(Direction.RIGHT):
                c.move(Direction.RIGHT)
            else:
                if c.canMove(Direction.DOWN):
                    c.nextLine()

        if c.getCell().getIsland().isFull():
            return self.__goToNextIsland()
