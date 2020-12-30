from lib.cell import *
from lib.cursor import *
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
    c = Cursor(grid)

    # grid.display() OU print(grid) + redéfinition de Grid.__str__ ?
    for cell in grid:
        print(cell)

    print(c)
    while (c.canMove(Direction.DOWN)):
        c.move(Direction.DOWN)
        print(c)

main()
