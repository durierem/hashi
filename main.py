from lib.cell import *
from lib.direction import Direction
from lib.grid import Grid
from lib.island import Island


def main():
    matrix = [
        [Cell(), Cell(), Cell(Island(2))],
        [Cell(Island(2)), Cell(), Cell(Island(4))],
        [Cell(), Cell(), Cell(Island(1))],
        [Cell(Island(1)), Cell(), Cell()],
    ]

    grid = Grid(matrix)
    print("Grid width: " + str(grid.getWidth()))
    print("Grid height: " + str(grid.getHeight()))

    # grid.display() OU print(grid) + redéfinition de Grid.__str__

    for c in grid:
        print(c)

main()
