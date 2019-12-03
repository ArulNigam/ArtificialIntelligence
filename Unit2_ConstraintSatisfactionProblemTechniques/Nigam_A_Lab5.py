Due Nov 24
Lab5 N-Queens
27/30
27 points out of possible 30
Nicole Kim Nov 18 (Edited Nov 25)
File Name: LastName_FirstInitial_Lab5.py
AI U2 Day 6 Student Note.pdf
PDF
Class comments
Your work
Graded
Nigam_A_Lab5.py
Text
Private comments
Nicole KimNov 26
size 64 --> 19 sec

# Name: Arul Nigam
# Period: 3

import time, copy

def main():
    n = int(input("What is N? "))
    columns_done = []
    board = [[0 for i in range(n)] for j in range(n)]
    # 1 What data structure is used for the board? What does the initial board look like?
    cur_time = time.time()
    solution = backtracking_search(board, columns_done)  # 2 What does '0' represent?
    display(solution)
    print(time.time() - cur_time)

def backtracking_search(board, columns_done):
    if check_complete(board, 0): return board
    col = select_unassigned_var(board, columns_done)
    columns_done.append(col)
    for row in range(len(board)):
        if isValid(row, col, board):
            board[row][col] = 1
            result = backtracking_search(board, columns_done)  # 3 What is the next col?
            if result != None: return result
            board[row][col] = 0  # 4 In order to backtrack, what code should be here?
    columns_done.remove(col)
    return None

def check_complete(board, colNum):  # 5 Fill out the blank below
    lngth = len(board)
    count = 0
    for row in range(lngth):
        for col in range(lngth):
            if board[row][col] == 1:
                count += 1
    return count == lngth

def isValid(row, col, board):
    for x in range(len(board)):
        if board[row][x] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, len(board), 1), range(col, len(board), 1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, len(board), 1)):
        if board[i][j] == 1:
            return False
    for x in range(len(board)):
        if board[x][col] == 1:
            return False
    return True

def select_unassigned_var(board, columns_done):  # MRV
    mincol = 0
    mincolvalue = 10000
    for col in range(len(board)):
        if col not in columns_done:
            rowcount = 0
            for row in range(len(board)):
                if (isValid(row, col, board)):
                    rowcount += 1
            if rowcount < mincolvalue and rowcount > 0:
                mincol = col
                mincolvalue = rowcount
    return mincol

def display(solution):
    for row in solution:
        print(' '.join([str(i) for i in row]))
    print("")

if __name__ == '__main__':
    main()
