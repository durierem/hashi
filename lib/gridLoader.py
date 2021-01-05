import json

from lib.cell import Cell
from lib.grid import Grid
from lib.island import Island


class GridLoader:
    def __init__(self, file):
        assert isinstance(file, str)
        self.__file = file

    # Retourne la grille contenue dans file
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
            return Grid(matrix)
        except Exception as e:
            print(e)
            exit(1)
