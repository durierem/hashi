import copy
import itertools

from lib.cell import *
from lib.cursor import Cursor
from lib.cursor import EndOfGridException
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
        if Grid.allBridgeCombinations == None:
            Grid.allBridgeCombinations = Grid.__createAllBridgeCombinations()

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
            if c.getCoordX() == self.getWidth() - 1:
                print("")

    # Affiche la matrice associé à la grille.
    def display_matrix(self):
        for c in self:
            c.getCell().display_value()
            if c.getCoordX() == self.getWidth() - 1:
                print("")

    # Renvoie la grille résolue ou None s'il n'existe pas de solution.
    def solve(self):
        # Si aucune île dans le graphe, le graphe est solution de lui-même.
        if not self.getCell().isIsland():
            if not self.__hasNextIsland():
                return False
        
        # L'algorithme nécessite de placer le curseur sur la première île.
        self.__goToNextIsland()
        
        queue = [self]
        while queue:
            grids = queue.pop(0).__createGrids()
            for g in grids:
                if not g.__hasNextIsland():
                    if g.__isConnected():
                        return g
                    else:
                        break
                g.__goToNextIsland()
                queue.append(g)

        return None

    # OUTILS

    # Renvoie une liste de toutes les combinaison de nombres de ponts dans les
    # 4 directions possibles pour une cellule.
    # Les combinaisons sont des dictionnaires associants à chaque direction, le
    # nombre de ponts présents dans cette direction.
    @staticmethod
    def __createAllBridgeCombinations():
        res = []
        keys = [d for d in Direction]
        for a, b, c, d in itertools.product([0, 1, 2], repeat=4):
            values = [a, b, c, d]
            res.append({k:v for (k, v) in zip(keys, values)})
        return res

    # Renvoie une liste composée de nouvelles grilles construites à partir de
    # la grille actuelle en ajoutant les ponts posibles à l'île pointée par
    # le curseur de la grille actuelle.
    def __createGrids(self):
        combinations = self.allBridgeCombinations.copy()
        combinations.pop(0)

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
                    i for i in combinations
                    if i[d] <= self.getIsland(neighborCursors[d]).getPossibleBridges(op)
                ]
            else:
                combinations = [i for i in combinations if i[d] <= 0]

        # ...
        combinations = [
            i
            for i in combinations
            if sum(i.values()) == self.getIsland().getMaxBridges() - self.getIsland().getTotalBridges()
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
                    while not g.getCell(c).isIsland():
                        g.getCell(c).setType(CellType.BRIDGE)
                        g.getCell(c).setDirection(d)
                        if isDual:
                            g.getCell(c).setDual()
                        c.move(d)
            newGrids.append(g)
        return newGrids

    # S'il existe une île pouvant être reliée à la cellule pointée par
    # 'cursor' dans la 'direction' donnée, renvoie un curseur pointant sur les
    # coordonnées de cette île. Sinon renvoie None.
    # Si aucun curseur n'est précisé, celui de la grille est utilisé.
    # Dans tout les cas, le curseur donné n'est pas modifié.
    def __findNeighbor(self, direction, cursor=None):
        c = copy.copy(cursor if cursor != None else self.getCursor())
        condition = self.getCell(c).getIsland().getBridges(direction) > 0

        while c.canMove(direction):
            c.move(direction)
            cl = self.getCell(c)
            if cl.isIsland() or (cl.isBridge() and not condition):
                break
      
        if self.getCursor() == c or not self.getCell(c).isIsland():
            return None
        return c

    # Renvoie vrai une autre est présente dans le sens de lecture.
    def __hasNextIsland(self, cursor=None):
        c = copy.copy(cursor if cursor != None else self.getCursor())
        while True:
            try:
                c.goToNextCell()
            except EndOfGridException:
                return False
            if c.getCell().isIsland():
                if c.getCell().getIsland().isFull():
                    continue
                return True

    # Déplace le curseur sur la prochaîne île dans le sens de lecture.
    def __goToNextIsland(self):
        assert self.__hasNextIsland(), "No island left"

        self.getCursor().goToNextIsland()
        if self.getIsland().isFull():
            return self.__goToNextIsland()

    # Renvoie vrai si le graphe formé par les îles est connexe.
    def __isConnected(self):
            vertex = []
            edge = []
            for c in self:
                if c.getCell().isIsland():
                    buf = Cursor(self, c.getCoord())
                    vertex.append(buf)
                    for d in Direction:
                        if c.getCell().getIsland().getBridges(d) > 0:
                            c2 = self.__findNeighbor(d, c)
                            if c2 != None:
                                buf = Cursor(self,c.getCoord())

                                if edge.count((buf,c2)) == 0 and edge.count((c2,buf)) == 0:
                                    edge.append((buf,c2))

            father = []
            for i in vertex:
                #foretDiscrete()
                father.append(-1)
            for e in edge:
                x,y = e
                x = vertex.index(x)
                y = vertex.index(y)
                #Trouverrapide(x, r1, pere)
                i = x
                while father[i] > -1:
                    i = father[i]
                r1 = i
                i = x
                while father[i] > -1:
                    j = i
                    i = father[i]
                    father[j] = r1
                #Trouverrapide(x, r2, pere)
                i = y
                while father[i] > -1:
                    i = father[i]
                r2 = i
                i = y
                while father[i] > -1:
                    j = i
                    i = father[i]
                    father[j] = r2
                #Reunirpondere(r1,r2,pere)
                if r1 != r2 :
                    if father[r1] > father[r2]:
                        father[r2] = father[r1] + father[r2]
                        father[r1] = r2
                    else:
                        father[r1] = father[r1] + father[r2]
                        father[r2] = r1

            return father.count(-len(father)) == 1

    def solve2(self):
        if not self.getCell().isIsland():
            if self.__hasNextIsland():
                self.__goToNextIsland()
            else:
                return self

        # ALGOOOO
        grids = [self]
        hasChange = True
        while hasChange:
            d = 0
            hasChange = False
            grids[0].getCursor().setCoord((0,0))
            while grids[0].__hasNextIsland():
                grids[0].__goToNextIsland()
                buf = grids[0].__createGrids()
                if len(buf) == 1 and buf != []:
                    grids[0] = buf[0]
                    grids[0].display()
                    hasChange = True
        return grids[0]

    def solveL(self):
        if not self.getCell().getType() != CellType.ISLAND:
            if self.__hasNextIsland():
                self.__goToNextIsland()
            else:
                return self
        #pas bon le dernier cursor
        grids = [(self,[Cursor(self,self.getCursor().getCoord())],Cursor(self,(3,3)))]
        j = 0
        while grids:
            e = grids.pop(0)
            g,lc,lastPositionC = e
            print("-------boucle----------")
            print("lc:")
            print(len(lc))
            print("g:")
            g.display()
            for c in lc:
                g.getCursor().setCoord(c.getCoord())
                buf = g.__createGrids()
                print("buf:")
                print(len(buf))
                for i in buf:
                    lNeighbor = []
                    print("i")
                    i.display()
                    for d in Direction:
                        bufc =  i.__findNeighbor(d)
                        if bufc != None:
                            print("cc")
                            if bufc.getCoord() != lastPositionC.getCoord():
                                if i.getIsland().getBridges(d) > 0:
                                    cn = bufc
                                    lNeighbor.append(cn)
                    print("lN:")
                    [print(i) for i in lNeighbor]
                    print()
                    grids.append((i,lNeighbor[:],Cursor(i,i.getCursor().getCoord())))
            print("grids:")
            [i.display() for (i,x,y) in grids]
            print(len(grids))
            j += 1
        return None
