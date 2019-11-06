# Name: Arul Nigam
# Period: 3

from tkinter import * 
from graphics import *

def check_complete(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):     
   # Goal Test: are there any unassigned (".") 
   if assignment == None or assignment == []:
      return False      
   for cell_value in assignment:
      if cell_value == ".":
         return False
   return True

def select_unassigned_var(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict): 
   # Select an unassigned variable - forward checking, MRV, or LCV
   # returns a variable
   for key in range(24):
      if assignment[key] == ".": 
         return key
            
def isValid(value, cell, assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
   for hex in tri_to_hex_dict[cell]: 
      for tri in hex_to_tri_dict[hex]:
         if assignment[tri] != ".":
            if int(assignment[tri]) == value and tri != cell: # neighbors are the same:
               return False # invalid 
   return True

def backtracking_search(assignment, cell_to_squares_dict, possible_ints, square_to_cells_dict):    
   return recursive_backtracking(assignment, cell_to_squares_dict, possible_ints, square_to_cells_dict)

def recursive_backtracking(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
   if check_complete(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
      s = ""
      for i in assignment:
         s += str(i)
      return s
   cell = select_unassigned_var(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict) 
   if cell != None:
      for value in possible_ints[cell]: # possible_ints maps traingle to [1 - 6]
         assignment[cell] = int(value)
         if isValid(value, cell, assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
            result = recursive_backtracking(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict)
            if check_complete(result, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
               return result
            assignment.pop(cell)
            assignment.append(".")
   return None

def display(solution):
   solution = ''.join([str(i) for i in solution])
   for i in range(0, 81, 9):
      print(solution[i : i + 3], " ", solution[i + 3 : i + 6], " ", solution[i + 6 : i + 9])
      if i == 18 or i == 45:
         print("")
 
def main(): 
   
   cell_to_squares_dict, possible_ints, square_to_cells_dict  = {}, [[] for i in range(24)], {} # cell_to_squares_dict: regions, possible_ints: variables, square_to_cells_dict: adjacents

   cell_to_squares_dict[0] = [1]
   cell_to_squares_dict[1] = [1]
   cell_to_squares_dict[2] = [1, 2]
   cell_to_squares_dict[3] = [2]
   cell_to_squares_dict[4] = [2]
   cell_to_squares_dict[5] = [6]
   cell_to_squares_dict[6] = [1, 6]
   cell_to_squares_dict[7] = [0, 1, 6]
   cell_to_squares_dict[8] = [0, 1, 2]
   cell_to_squares_dict[9] = [0, 2, 3]
   cell_to_squares_dict[10] = [2, 3]
   cell_to_squares_dict[11] = [3]
   cell_to_squares_dict[12] = [6]
   cell_to_squares_dict[13] = [5, 6]
   cell_to_squares_dict[14] = [0, 5, 6]
   cell_to_squares_dict[15] = [0, 4, 5]
   cell_to_squares_dict[16] = [0, 3, 4]
   cell_to_squares_dict[17] = [3, 4]
   cell_to_squares_dict[18] = [3]
   cell_to_squares_dict[19] = [5]
   cell_to_squares_dict[20] = [5]
   cell_to_squares_dict[21] = [4, 5]
   cell_to_squares_dict[22] = [4]
   cell_to_squares_dict[23] = [4]
    
   for r in range(len(cell_to_squares_dict)): 
      possible_ints[r] = [i for i in range(10)] # 0 - 9

   square_to_cells_dict[0] = [7, 8, 9, 14, 15, 16]
   square_to_cells_dict[1] = [0, 1 , 2, 6, 7, 8]
   square_to_cells_dict[2] = [2, 3, 4, 8, 9, 10]
   square_to_cells_dict[3] = [9, 10, 11, 16, 17, 18]
   square_to_cells_dict[4] = [15, 16, 17, 21, 22, 23]
   square_to_cells_dict[5] = [13, 14, 15, 19, 20, 21]
   square_to_cells_dict[6] = [5, 6, 7, 12, 13, 14]
   
   initial = list(sys.argv[1])
   print("input state", "\n", "-------------------")
   display(initial)
   print("-------------------", "\n", "solution", "\n", "-------------------")
   solution = backtracking_search(initial, cell_to_squares_dict, possible_ints, square_to_cells_dict) 
   display(solution)

if __name__ == '__main__':
   main()