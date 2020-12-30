# Pour l'instant ne fait que lire un json.
# Il manque la traduction en une matrice 

import json

class GridLoader:
    def __init__(self, file):
        assert isinstance(file, str)
        self.__file = file

    def load(self):
        try:
            with open(self.__file) as f :
                data = json.load(f)
            print(data)
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