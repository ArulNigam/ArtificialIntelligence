# Name: Arul Nigam
# Period: 3

from tkinter import * 
from graphics import *

def check_complete(assignment):     
   # Goal Test: are there any unassigned (".") 
   if assignment == None or assignment == []:
      return False      
   for cell_value in assignment:
      if cell_value == ".":
         return False
   return True

def select_unassigned_var(assignment): 
   # Select an unassigned variable - forward checking, MRV, or LCV
   # returns a variable
   for key in range(81):
      if assignment[key] == ".": 
         return key
            
def isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################   
   #ALWAYS ASSIGNS 1 FOR INDEX 0?????????????????????????!!!!!!!!!!!!!!!!!!!!###################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   #############################################################################################
   row_neighbors = []
   col_neighbors = []
   square_neighbors = []
   for i in range(len(assignment)):
      i = int(i)
      if cell_to_groups_dict[cell][0] == int(i / 9): # same row   
         row_neighbors.append(i)
      if cell_to_groups_dict[cell][1] == i % 9: # same col   
         col_neighbors.append(i)
      if same_square(cell, i): # same sub-square
         square_neighbors.append(i)
   for i in cell_to_groups_dict[cell]: 
      for a in row_neighbors:
         if assignment[a] != ".":
            if int(assignment[a]) == value and a != cell: # neighbors are the same:
               return False # invalid
      for b in col_neighbors:
         if assignment[b] != ".":
            if int(assignment[b]) == value and b != cell: # neighbors are the same:
               return False # invalid
      for c in square_neighbors:    
            if assignment[c] != ".":
               if int(assignment[c]) == value and c != cell: # neighbors are the same:
                  return False # invalid
   return True

def backtracking_search(initial, cell_to_groups_dict, possible_ints):    
   return recursive_backtracking(list(initial), cell_to_groups_dict, possible_ints)

def recursive_backtracking(assignment, cell_to_groups_dict, possible_ints):
   if check_complete(assignment):
      s = ""
      for i in assignment:
         s += str(i)
      return s
   cell = select_unassigned_var(assignment) 
   if cell != None:
      for value in possible_ints[cell]: # possible_ints maps cell to [0 - 9]
         assignment[cell] = int(value)
         if isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
            result = recursive_backtracking(assignment, cell_to_groups_dict, possible_ints)
            if check_complete(result):
               return result
            assignment.pop(cell)
            assignment.append(".")
   return None

def display(solution):
   for i in range(0, 81, 9):
      print(solution[i : i + 3], " ", solution[i + 3 : i + 6], " ", solution[i + 6 : i + 9])
      if i == 18 or i == 45:
         print("")
 
def same_square(i, j): 
   return int(i / 27) == int(j / 27) and (i % 9) / 3 == (j % 9) / 3

def main(): 
   initial = list(sys.argv[1])
   initial = ''.join([str(i) for i in initial])

   possible_ints = [[] for i in range(81)]
   for r in range(len(initial)): 
      possible_ints[r] = [i for i in range(1, 10)] # 1 - 9
   
   cell_to_groups_dict = {}

   for cell in range(len(initial)):
      row = int(cell / 9)
      col = cell % 9
      cell_to_groups_dict[cell] = [row, col]
      
   print("input state", "\n", "-------------------")

   display(initial)

   print("-------------------", "\n", "solution", "\n", "-------------------")

   solution = backtracking_search(initial, cell_to_groups_dict, possible_ints) 
   solution = ''.join([str(i) for i in solution])

   display(solution)

if __name__ == '__main__':
   main()
