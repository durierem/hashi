import sys

from lib.gridLoader import GridLoader


def main():
    if len(sys.argv) != 2:
        print("Usage: main <grid>.json")
        exit(1)

    grid = GridLoader(sys.argv[1]).load()
    solved = grid.solve()
    if solved == None:
        print("No solution found")
        exit(1)
    else:
        solved.display()


main()
