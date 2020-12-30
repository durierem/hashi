#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Comment gerer les erreurs ?
class Cursor:
    __maxSizeX__ = 0
    __maxSizeY__ = 0
    __currentPosition__ = [0, 0]

    def __init__(self, sizeX, sizeY, index):
        # erreur ?
        x, y = index
        self.__maxSizeX__ = sizeX
        self.__maxSizeY__ = sizeY
        self.__currentPosition__ = [x, y]

    def getCurrentPosition(self):
        return (self.__currentPosition__[0], self.__currentPosition__[1])

    def setCurrentPosition(self, x, y):
        if x < 0 or x > self.__maxSizeX__ or y < 0 or y > self.__maxSizeY__:
            print("Erreur setCurrentPosition")
            print("il faut gerer cette erreur")
        else:
            self.__currentPosition__[0] = x
            self.__currentPosition__[1] = y

    def cantMove(self, direction):
        directionX, directionY = direction.value

        if directionX == 0 and directionY == -1:
            return self.__currentPosition__[1] == 0

        if directionX == -1 and directionY == 0:
            return self.__currentPosition__[0] == 0

        if directionX == 0 and directionY == 1:
            return self.__currentPosition__[1] == self.__maxSizeY__ - 1

        if directionX == 1 and directionY == 0:
            return self.__currentPosition__[0] == self.__maxSizeX__ - 1
        else:
            print("il faut gerer cette erreur")
            return false

    def goTo(self, direction):
        directionX, directionY = direction.value
        if self.cantMove(direction):
            print("Erreur goTo")
            print("il faut gerer cette erreur")
        else:
            self.__currentPosition__[0] = self.__currentPosition__[0] + directionX
            self.__currentPosition__[1] = self.__currentPosition__[1] + directionY


# In[12]:


class Island:
    __bridgesRequired__ = 0
    __lNeighbors__ = []
    __maximumBridgeByDirection__ = 0

    def __init__(self, bridgesRequired, maximumBridgeByDirection):
        self.__bridgesRequired__ = bridgesRequired
        self.__lNeighbors__ = [0, 0, 0, 0]
        self.__maximumBridgeByDirection__ = maximumBridgeByDirection

    def addPont(self, direction):
        directionX, directionY = direction.value
        if self.__conditionADDBridge__(direction) == False:
            print("Le nombre maximum de pont avec cette ile est atteint")
            return

        if directionX == 0 and directionY == -1:
            self.__lNeighbors__[0] = self.__lNeighbors__[0] + 1

        elif directionX == -1 and directionY == 0:
            self.__lNeighbors__[1] = self.__lNeighbors__[1] + 1

        elif directionX == 0 and directionY == 1:
            self.__lNeighbors__[2] = self.__lNeighbors__[2] + 1

        elif directionX == 1 and directionY == 0:
            self.__lNeighbors__[3] = self.__lNeighbors__[3] + 1
        else:
            print("il faut gerer cette erreur")

    def nbOfBridge(self, direction):
        directionX, directionY = direction.value

        if directionX == 0 and directionY == -1:
            return self.__lNeighbors__[0]

        elif directionX == -1 and directionY == 0:
            return self.__lNeighbors__[1]

        elif directionX == 0 and directionY == 1:
            return self.__lNeighbors__[2]

        elif directionX == 1 and directionY == 0:
            return self.__lNeighbors__[3]

        else:
            print("il faut gerer cette erreur")
            return self.__lNeighbors__

    def nbOfPossibleNewBridge(self, direction):
        return min(
            self.bridgesRequired() - self.someOfBridge(),
            self.maximumBridgeByDirection() - self.nbOfBridge(direction),
        )

    def someOfBridge(self):
        return sum(self.__lNeighbors__)

    def maximumBridgeByDirection(self):
        return self.__maximumBridgeByDirection__

    def bridgesRequired(self):
        return self.__bridgesRequired__

    def __conditionADDBridge__(self, direction):
        if self.nbOfBridge(direction) >= self.__maximumBridgeByDirection__:
            return False
        if sum(self.__lNeighbors__) >= self.__bridgesRequired__:
            return False
        return True


i = Island(4, 2)
i.addPont(Direction.LEFT)
i.addPont(Direction.RIGHT)
i.addPont(Direction.UP)
i.addPont(Direction.UP)
print(i.someOfBridge())
print(i.bridgesRequired())
print(i.nbOfPossibleNewBridge(Direction.RIGHT))


# In[61]:


from enum import Enum

# un Enum est-il vraiment interessant ?
class Direction(Enum):
    LEFT = (0, -1)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)

    def opposite(direction):
        if direction == Direction.LEFT:
            return Direction.RIGHT
        if direction == Direction.UP:
            return Direction.DOWN
        if direction == Direction.RIGHT:
            return Direction.LEFT
        if direction == Direction.DOWN:
            return Direction.UP
        print("erreur")

    opposite = staticmethod(opposite)


Direction.opposite(Direction.DOWN)


# In[ ]:


# In[171]:


class Hashiwokakera:
    def __init__(self, graphe):
        ##tester le graphe
        self.graphe = graphe
        x, y = graphe.shape
        self.cursor = Cursor(x, y, (0, 0))
        self.__allPosibilityOfBridge__ = createPossibility()

    def __createBridge__(self):
        possibleBridge = self.__allPosibilityOfBridge__[:]

        nbOfLeftPossibleBridge = self.__foundNbOfPossibleBridge__(Direction.LEFT)
        nbOfUpPossibleBridge = self.__foundNbOfPossibleBridge__(Direction.UP)
        nbOfRightPossibleBridge = self.__foundNbOfPossibleBridge__(Direction.RIGHT)
        nbOfDownPossibleBridge = self.__foundNbOfPossibleBridge__(Direction.DOWN)

        print(nbOfLeftPossibleBridge)
        print(nbOfUpPossibleBridge)
        print(nbOfRightPossibleBridge)
        print(nbOfDownPossibleBridge)

        possibleBridge = [
            i for i in possibleBridge if i[0] < nbOfLeftPossibleBridge + 1
        ]
        possibleBridge = [i for i in possibleBridge if i[1] < nbOfUpPossibleBridge + 1]
        possibleBridge = [
            i for i in possibleBridge if i[2] < nbOfRightPossibleBridge + 1
        ]
        possibleBridge = [
            i for i in possibleBridge if i[3] < nbOfDownPossibleBridge + 1
        ]
        possibleBridge = [
            i
            for i in possibleBridge
            if sum(i)
            == self.graphe[self.cursor.getCurrentPosition()].bridgesRequired()
            - self.graphe[self.cursor.getCurrentPosition()].someOfBridge()
        ]
        return possibleBridge

    def __foundNbOfPossibleBridge__(self, direction):
        # Comment gerer un mauvais index ?
        directionX, directionY = direction.value
        # erreur ?
        a, b = self.graphe.shape
        cursor = Cursor(a, b, self.cursor.getCurrentPosition())
        cursor.goTo(direction)
        while (
            type(self.graphe[cursor.getCurrentPosition()]) != Island
            and (
                self.graphe[cursor.getCurrentPosition()] != -1
                or self.graphe[self.cursor.getCurrentPosition()].nbOfBridge(direction)
                == 1
            )
            and not cursor.cantMove(direction)
        ):
            print("coucou")
            cursor.goTo(direction)

        if self.cursor.getCurrentPosition() == cursor.getCurrentPosition():
            return 0
        if self.graphe[cursor.getCurrentPosition()] == -1:
            return 0
        if self.graphe[cursor.getCurrentPosition()] == 0:
            return 0
        return self.graphe[cursor.getCurrentPosition()].nbOfPossibleNewBridge(
            Direction.opposite(direction)
        )


# In[170]:


import numpy as np

graphe = np.array(
    [
        [Island(4, 2), -1, Island(4, 2)],
        [0, Island(0, 0), Island(0, 0)],
        [Island(1, 2), Island(0, 0), Island(0, 0)],
    ],
    dtype=object,
)

i = Island(4, 2)
i.addPont(Direction.LEFT)
graphe[1, 2] = i

i = Island(4, 2)
i.addPont(Direction.RIGHT)
graphe[0, 0] = i

hashiwokakera = Hashiwokakera(graphe)
hashiwokakera.cursor.setCurrentPosition(0, 0)
hashiwokakera.__createBridge__()


# In[ ]:


hashiwokakera.cursor.goTo(Direction.LEFT)
print(hashiwokakera.cursor.getCurrentPosition())


# In[14]:


hashiwokakera.cursor.goTo(Direction.UP)
print(hashiwokakera.cursor.getCurrentPosition())


# In[7]:


hashiwokakera.cursor.goTo(Direction.RIGHT)
print(hashiwokakera.cursor.getCurrentPosition())


# In[8]:


hashiwokakera.cursor.goTo(Direction.DOWN)
print(hashiwokakera.cursor.getCurrentPosition())


# In[9]:


S


# In[10]:


# la rendre plus flexible
def createPossibility():
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


# renvoie une listes dont les éléments sont les nombres d'occurances des éléemnts l1 dans l0
def compteOccurence(l0, l1):
    s = 0
    r = [0 for i in range(len(l1))]
    for i in range(len(l1)):
        for j in l0:
            if l1[i] == j:
                r[i] = r[i] + 1
    return r


l = createPossibility()
l = [i for i in l if i[0] < 1]
l = [i for i in l if i[1] < 1]
l = [i for i in l if i[2] < 3]
l = [i for i in l if i[3] < 2]
l = [i for i in l if sum(i) == 3]
print(l)


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
