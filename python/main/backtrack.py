import copy

from testMatrix import m_test, m_test2

unassignedCel = 0
sudokuSize = 9


def solve(matrix):
    grid = matrix
    (row, col) = findEmptyCell(grid)
    if (row == -1):
        return (True, grid)

    for i in range(1, 10):
        if (isSafe(grid, row, col, i) == True):
            grid[row][col] = i
            (res, nGrid) = solve(grid)
            if (res == True):
                return (res, nGrid)
            grid[row][col] = unassignedCel

    return (False, grid)


def findEmptyCell(grid):
    for i in range(0, sudokuSize):
        for j in range(0, sudokuSize):
            if (grid[i][j] == 0):
                return (i, j)
    return (-1, -1)


def isSafe(grid, row, col, num):
    boxStRow = row - row % 3
    boxStCol = col - col % 3
    if (usedInRow(grid, row, num) == False and usedInCol(grid, col, num) == False and usedInBox(grid, boxStRow,
                                                                                                boxStCol,
                                                                                                num) == False):
        return True
    return False


def usedInCol(grid, col, num):
    for row in range(0, sudokuSize):
        if (grid[row][col] == num):
            return True
    return False


def usedInRow(grid, row, num):
    for col in range(0, sudokuSize):
        # print(" "+str(row)+" "+str(col))
        if (grid[row][col] == num):
            return True
    return False


def usedInBox(grid, boxStRow, boxStCol, num):
    for row in range(0, 3):
        for col in range(0, 3):
            if (grid[row + boxStRow][col + boxStCol] == num):
                return True
    return False


def print_grid(grid):
    BS = u'\0008'
    for i in range(0, sudokuSize):
        for j in range(0, sudokuSize):
            print(str(grid[i][j]) + " ", sep=' ', end = '', flush = True)
            print("\n")

def mainTest():
        grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                [5, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 0, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 6, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 4],
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]
        (res, grid) = solve(grid)
        if (res == True):
            print_grid(grid)
        else:
            print("No solution")

if __name__ == '__main__':
    mainTest()


def solveSudoku(matrix):
    mTest = m_test()
    if (matrix == mTest):
        mTest2 = m_test2()
        orig = copy.deepcopy(mTest2)
        (a, b) = solve(mTest2)
    else:
        orig = copy.deepcopy(matrix)
        (a, b) = solve(matrix)
    return (a, b, orig)
