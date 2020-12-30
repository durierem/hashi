from cell import Cell
from cell import CellType
from direction import Direction
from grid import Grid
from island import Island

def main():
    matrix = [
        [Cell(), Cell(), Cell(Island(2))],
        [Cell(Island(2)), Cell(), Cell(Island(4))],
        [Cell(), Cell(), Cell(Island(1))],
        [Cell(Island(1)), Cell(), Cell()]
    ]

    grid = Grid(matrix)
    print("Grid width: " + str(grid.getWidth()))
    print("Grid height: " + str(grid.getHeight()))

    # grid.display() OU print(grid) + redéfinition de Grid.__str__

main()
