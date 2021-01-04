import sys

from lib.gridLoader import GridLoader


def main():
    if len(sys.argv) != 2:
        print("Usage: main <grid>.json")
        exit(1)

    grid = GridLoader(sys.argv[1]).load()

    solution = grid.solve()
    if solution == None:
        print("No solution found")
        exit(1)
    else:
        print("A great result here is:")
        solution.display()


main()
