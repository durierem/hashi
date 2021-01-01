from lib.gridLoader import GridLoader


def main():
    grid = GridLoader("grid.json").load()

    # Affiche les éléments de la grille, de gauche à droite, de haut en bas
    # for cursor in grid:
    #     print(str(cursor) + " -> " + str(cursor.getCell()))

    # Test affichage graphique de la grille
    grid.draw()
main()
