# Name: Arul Nigam
# Period: 3

import time

def main():
   #n = int(input("What is N? "))
   board = [[0 for i in range(8)] for j in range(8)]
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
         result = backtracking_search(board,________) #3 What is the next col?
         if result != None: return result
         _________________________ #4 In order to backtrack, what code should be here?
   return None
   
def check_complete(board, colNum): #5 Fill out the blank below
   _____________________________________________________________
   if assignment is None or assignment == []:
       return False
   for cell_value in assignment:
       if cell_value == ".":
           return False
   return True


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