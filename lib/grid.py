import copy

from lib.cell import *
from lib.cursor import Cursor
from lib.direction import Direction

# Modélise une grille de Hashiwokakero.
class Grid:

    # CONSTRUCTEUR

    # Créé un nouvelle grille à partir de la liste donnée.
    #
    # matrix - La réprésentation d'une grille de hashi par une liste à deux
    #          dimensions dans laquelle, un 0 représente une case vide et un
    #          chiffre strictement positif et le nombre de ponts associés.
    def __init__(self, matrix):
        self.__matrix = matrix
        self.__cursor = Cursor(self)

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

    # OUTILS

    def __createPossibleBridges(self):
        l = []
        for i0 in range(3):
            buf = [0, 0, 0, 0]
            buf[0] = i0
            for i1 in range(3):
                buf[1] = i1
                for i2 in range(3):
                    buf[2] = i2
                    for i3 in range(3):
                        buf[3] = i3
                        l.append(buf[:])
        return l

    # Renvoie une liste composée de nouvelles grilles construites à partir de
    # la grille actuelle en ajoutant les ponts posibles à l'île pointée par
    # le curseur de la grille actuelle.
    def __createGrids(self):
        possibleBridges = self.__createPossibleBridges()  # [:]
        cNeighbord = []
        j = 0
        for d in Direction:
            cNeighbord.append(self.__findPossibleNeighbor(d))
            op = Direction.opposite(d)
            if cNeighbord[j] != 0:
                possibleBridges = [
                    i
                    for i in possibleBridges
                    if i[j] <= self.getIsland(cNeighbord[j]).getPossibleBridges(op)
                ]
            else:
                possibleBridges = [i for i in possibleBridges if i[j] <= 0]
            j += 1

        possibleBridges = [
            i
            for i in possibleBridges
            if sum(i)
            == self.getIsland().getMaxBridges() - self.getIsland().getTotalBridges()
        ]
        newGrid = []
        for i in possibleBridges:
            g = copy.deepcopy(self)
            j = 0
            for d in Direction:
                op = Direction.opposite(d)
                if i[j] != 0:
                    for k in range(i[j]):
                        g.getIsland().addBridge(d)
                        g.getIsland(cNeighbord[j]).addBridge(op)
                    c = Cursor(g, self.getCursor().getCoord())
                    dual = True if c.getCell().getIsland().getBridges(d) == 2 else False
                    c.move(d)
                    while g.getCell(c).getType() != CellType.ISLAND:
                        g.getCell(c).setType(CellType.BRIDGE)
                        g.getCell(c).setDirection(d)
                        if dual:
                            g.getCell(c).setDual()
                        c.move(d)
                j += 1
            newGrid.append(g)
        return newGrid

    # S'il existe une île pouvant être reliée à celle pointée par le curseur
    # actuel dans la direction donnée, renvoie un curseur pointant sur ses
    # cooronnées. Sinon renvoie 0.
    def __findPossibleNeighbor(self, direction):
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
            return 0

        return c

    def __haveNextIsland(self, cursor=None):
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
            return self.__haveNextIsland(c)
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

    def solve(self):
        if self.getCell().getType() != CellType.ISLAND:
            if self.__haveNextIsland():
                self.__goToNextIsland()
            else:
                return self
        grid = self.__createGrids()
        for i in grid:
            if not i.__haveNextIsland():
                return i
            i.__goToNextIsland()
        while grid:
            g = grid[0]
            del grid[0]
            buf = g.__createGrids()
            for i in buf:
                if not i.__haveNextIsland():
                    print("Un super résultat que voila:")
                    return i
                i.__goToNextIsland()
                grid.append(i)
        return []
