from lib.cell import *
from lib.cursor import *
from lib.direction import Direction
from lib.grid import Grid
from lib.island import Island
from lib.gridLoader import GridLoader


def main():
    grid = GridLoader("grid.json").load()

    # Affiche les éléments de la grille, de gauche à droite, de haut en bas
    for cursor in grid:
        print(str(cursor) + " -> " + str(cursor.getCell()))

main()
