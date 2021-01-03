import sys

from lib.gridLoader import GridLoader


def main():
    grid = GridLoader(sys.argv[1]).load()
    solved = grid.solve()
    if solved == None:
        print("No solution found")
        exit(1)
    else:
        solved.display()

main()
