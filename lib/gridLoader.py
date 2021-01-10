import json

from lib.cell import Cell
from lib.grid import Grid
from lib.island import Island

class IllegalValue(Exception):
    pass

class BadDataFormat(Exception):
    pass

class GridLoader:
    @staticmethod
    def load(file):
        try:
            with open(file) as f:
                data = json.load(f)
            matrix = []
            length = -1
            for arr in data["grid"]:
                column = []
                for x in arr:
                    if x < 0 or x > 8 :
                        raise IllegalValue("Illegal value in the json grid")
                    if x == 0:
                        column.append(Cell())
                    if x > 0:
                        column.append(Cell(Island(x)))
                if length == -1:
                    length = len(column)
                if not len(column) == length:
                    raise BadDataFormat("One of the line in json grid is shorter")
                matrix.append(column)
            return Grid(matrix)
        except Exception as e:
            print(e)
            exit(1)