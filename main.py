from cell import Cell
from cell import CellType
from direction import Direction
from island import Island

def main():
    matrix = [
        [Cell(), Cell(), Cell(Island(2))],
        [Cell(Island(1)), Cell(), Cell(Island(4))],
        [Cell(), Cell(), Cell(Island(1))]
    ]

    grid = Grid(matrix)
    print(grid.getWidth())
    print(grid.getHeight())

    for line in grid:
        for cell in line:
            print(str(cell.getType()))
main()
