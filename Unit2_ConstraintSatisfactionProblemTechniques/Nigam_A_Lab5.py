# Name: Arul Nigam
# Period: 3

import time

def main():
   #n = int(input("What is N? "))
   n = 8
   board = [[0 for i in range(n)] for j in range(n)]
   #1 What data structure is used for the board? What does the initial board look like?
   cur_time = time.time()
   solution = backtracking_search(board, 0) #2 What does '0' represent?
   display(solution)
   print (time.time() - cur_time)

def backtracking_search(board, col):
   if check_complete(board, col): return board
   for row in range(len(board)):
      if isValid(row, col, board):
         board[row][col] = 1
         result = backtracking_search(board, col + 1) #3 What is the next col?
         if result != None: return result
         board[row][col] = 0 #4 In order to backtrack, what code should be here?
   return None
   
def check_complete(board, colNum): #5 Fill out the blank below
   return colNum == len(board)
   
def isValid(row, col, board):
   for x in range(col):
      if board[row][x] == 1:
         return False
   for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
      if board[i][j] == 1:
         return False
   for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
      if board[i][j] == 1:
         return False
   return True
   
def select_unassigned_var(assignment):
    # Select an unassigned variable - forward checking, MRV, or LCV
    # returns a variable
    for key in range(81):
        if assignment[key] == ".":
            return key
            
def display(solution):
   for row in solution:
      print(' '.join([str(i) for i in row]))
   print("")
            
if __name__ == '__main__':
    main()
