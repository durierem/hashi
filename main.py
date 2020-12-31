from lib.cell import *
from lib.cursor import *
from lib.direction import Direction
from lib.grid import Grid
from lib.island import Island
from gridLoader import GridLoader


def main():

    grid = Grid(GridLoader("grid.json").load())
    c = Cursor(grid)

    # Affiche les éléments de la grille, de gauche à droite, de haut en bas
    for cursor in grid:
        print(str(cursor) + " -> " + str(cursor.getCell()))

    # Affiche les coordonnées d'un curseur qui bouge vers le bas
    print(c)
    while (c.canMove(Direction.DOWN)):
        c.move(Direction.DOWN)
        print(c)

main()
