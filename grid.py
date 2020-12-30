class Grid():
    def __init__(self, cellMatrix):
        self.__matrix = cellMatrix

    def getMatrix(self):
        self.__matrix

    def getWidth(self):
        return len(self.__matrix[0])

    def getHeight(self):
        return len(self.__matrix)
