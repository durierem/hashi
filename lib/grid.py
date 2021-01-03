from lib.cell import *
from lib.cursor import Cursor
from lib.direction import Direction
import copy


import copy

class Grid:

    # CONSTRUCTEUR

    def __init__(self, matrix):
        self.__matrix = matrix
        self.__cursor = Cursor(self)

    # ÉNUMÉRATEUR

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

    def getMatrix(self):
        self.__matrix

    def getWidth(self):
        return len(self.__matrix[0])

    def getHeight(self):
        return len(self.__matrix)

    def getCursor(self):
        return self.__cursor

    def getCell(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        x, y = c.getCoord()
        return self.__matrix[y][x]

    def getIsland(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        return self.getCell(c).getIsland()
    
    
    
    def display(self):
        c = Cursor(self,(0,0))
        if self.getCell(c).getType() == CellType.ISLAND:
                print(str(self.getIsland(c).getMaxBridges()), end=",")
                print("[", end="")
                for d in Direction:
                    print(str(self.getIsland(c).getBridges(d)),end=",")
                print("]", end="")
        if self.getCell(c).getType() == CellType.BRIDGE: 
            print("-", end = "")
        if self.getCell(c).getType() == CellType.EMPTY: 
            print("x", end = "")
        print(end = " ")
        
        if c.canMove(Direction.RIGHT):
            c.move(Direction.RIGHT)
        else:
            if c.canMove(Direction.DOWN):
                c.setCoord((0,c.getCoordY() + 1))
            else:
                raise StopIteration
        while c.canMove(Direction.RIGHT) or c.canMove(Direction.DOWN):
            if self.getCell(c).getType() == CellType.ISLAND:
                print(str(self.getIsland(c).getMaxBridges()), end=",")
                print("[", end="")
                for d in Direction:
                    print(str(self.getIsland(c).getBridges(d)),end=",")
                print("]", end="")
            if self.getCell(c).getType() == CellType.BRIDGE: 
                print("-", end = "")
            if self.getCell(c).getType() == CellType.EMPTY: 
                print("x", end = "")
                
            if c.canMove(Direction.RIGHT):
                c.move(Direction.RIGHT)
                print(end = " ")
            else:
                if c.canMove(Direction.DOWN):
                    c.setCoord((0,c.getCoordY() + 1))
                    print()
                else:
                    raise StopIteration
                    
        if self.getCell(c).getType() == CellType.ISLAND:
                print(str(self.getIsland(c).getMaxBridges()), end=",")
                print("[", end="")
                for d in Direction:
                    print(str(self.getIsland(c).getBridges(d)),end=",")
                print("]", end="")
        if self.getCell(c).getType() == CellType.BRIDGE: 
            print("-", end = "")
        if self.getCell(c).getType() == CellType.EMPTY: 
            print("x", end = "")
        return
    
   
        
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
        return l;

    def __createGrids(self):
        possibleBridges = self.__createPossibleBridges() # [:]
        possibleBridges.remove([0,0,0,0])
        cNeighbord = []
        j = 0
        for d in Direction:
            cNeighbord.append(self.__findPossibleNeighbor(d))
            op = Direction.opposite(d)
            if cNeighbord[j] != 0:
                possibleBridges = [i for i in possibleBridges if i[j] <= self.getIsland(cNeighbord[j]).getPossibleBridges(op)]
            else :
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
                    c.move(d)
                    while g.getCell(c).getType() != CellType.ISLAND:
                        g.getCell(c).setType(CellType.BRIDGE)
                        c.move(d)
                j += 1
            newGrid.append(g)
        return newGrid
    
    

    def __findPossibleNeighbor(self, direction):
        c = Cursor(self, self.getCursor().getCoord())
        if c.canMove(direction) :
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
            # TODO: Redéfinir l'égalité de 2 curseurs comme en Java ?
            self.getCursor().getCoord() == c.getCoord()
            or self.getCell(c).getType() == CellType.BRIDGE
            or self.getCell(c).getType() == CellType.EMPTY
        ):
            return 0
        
        return c
    
    def __haveNextIsland(self, cursor=None):
        c = Cursor(self,cursor.getCoord()) if cursor != None else Cursor(self,self.getCursor().getCoord())
        if c.canMove(Direction.RIGHT):
            c.move(Direction.RIGHT)
        else:
            if c.canMove(Direction.DOWN):
                c.setCoord((0,c.getCoordY() + 1))
            else:
                return False
        while c.getCell().getType() != CellType.ISLAND:
            if c.canMove(Direction.RIGHT):
                c.move(Direction.RIGHT)
            else:
                if c.canMove(Direction.DOWN):
                    c.setCoord((0,c.getCoordY() + 1))
                else:
                    return False
        if c.getCell().getIsland().getMaxBridges() - c.getCell().getIsland().getTotalBridges() == 0:
            return self.__haveNextIsland(c)
        return True
        
    def __findNextIsland(self, cursor=None):
        c = cursor if cursor != None else self.getCursor()
        if c.canMove(Direction.RIGHT):
            c.move(Direction.RIGHT)
        else:
            if c.canMove(Direction.DOWN):
                c.setCoord((0,c.getCoordY() + 1))
            else:
                raise StopIteration
        while c.getCell().getType() != CellType.ISLAND:
            if c.canMove(Direction.RIGHT):
                c.move(Direction.RIGHT)
            else:
                if c.canMove(Direction.DOWN):
                    c.setCoord((0,c.getCoordY() + 1))
                else:
                    raise StopIteration
        if c.getCell().getIsland().getMaxBridges() - c.getCell().getIsland().getTotalBridges() == 0:
            return self.__findNextIsland()
    
    def solve(self):
        if self.getCell().getType() != CellType.ISLAND:
            if self.__haveNextIsland():
                self.__findNextIsland()
            else :
                return self
        grid = self.__createGrids()
        for i in grid:
            if not i.__haveNextIsland():
                return i
            i.__findNextIsland()
        while grid :
            g = grid[0]
            del grid[0]
            buf = g.__createGrids()
            for i in buf:
                if not i.__haveNextIsland():
                    print("Un super résultat que voila:")
                    return i
                i.__findNextIsland()
                grid.append(i)
        return []