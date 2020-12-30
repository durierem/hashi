from lib.island import *
from lib.grid import *
import json

class GridLoader:
    def __init__(self, file):
        assert isinstance(file, str)
        self.__file = file


    # Retourne la grille contenue dans file sous forme d'une matrice
    def load(self):
        try:
            with open(self.__file) as f:
                data = json.load(f)
            matrix = []
            for arr in data["grid"]:
                column = []
                for x in arr:
                    if x == 0:
                        column.append(Cell())
                    if x > 0:
                        column.append(Cell(Island(x)))
                matrix.append(column)
            return matrix
        except:
            print("Error reading the grid")


## Test section

def main():
    print("Entrez le nom du fichier contenant la grille : ")
    file = input()
    gl = GridLoader(file)
    grid = gl.load()
    print(grid)

main()