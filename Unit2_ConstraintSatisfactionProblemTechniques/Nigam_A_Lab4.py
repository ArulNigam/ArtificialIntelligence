# Name: Arul Nigam
# Period: 3

from tkinter import *
from graphics import *
import math  

def check_complete(assignment):
    # Goal Test: are there any unassigned (".")
    if assignment is None or assignment == []:
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
    neighbors = []
    for i in range(81):
        if i != cell:
            if cell_to_groups_dict[cell][0] == int(i / 9):  # same row
                neighbors.append(i)
            if cell_to_groups_dict[cell][1] == i % 9:  # same col
                neighbors.append(i)
            if same_square(cell, i):  # same sub-square
                neighbors.append(i)
    for a in neighbors:
        if assignment[a] != ".":
            if int(assignment[a]) == value:  # neighbors are the same:
                return False  # invalid
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
    for value in possible_ints[cell]:  # possible_ints maps cell to [0 - 9]
        assignment[cell] = str(value)
        if isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
            result = recursive_backtracking(assignment, cell_to_groups_dict, possible_ints)
            if check_complete(result):
                return result
        assignment[cell] = "."
    return None

def display(solution):
    for i in range(0, 81, 9):
        print(solution[i: i + 3], " ", solution[i + 3: i + 6], " ", solution[i + 6: i + 9])
        if i == 18 or i == 45:
            print("")

def same_square(i, j):
    return int(i / 27) == int(j / 27) and (int(int(i % 9) / 3) == int(int(j % 9) / 3))

def main():
   cell_to_groups_dict_nine = {}
   cell_to_groups_dict_twelve = {}
   cell_to_groups_dict_sixteen = {}
      
   possible_ints_nine = [[] for i in range(81)]
   possible_ints_twelve = [[] for i in range(144)]
   possible_ints_sixteen = [[] for i in range(256)]
     
   for cell in range(81):
       row = int(cell / 9)
       col = cell % 9
       cell_to_groups_dict_nine[cell] = [row, col]
       possible_ints_nine[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # 1 - 9
       
   for cell in range(144):
       row = int(cell / 9)
       col = cell % 9
       cell_to_groups_dict_twelve[cell] = [row, col]
       possible_ints_twelve[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C']  # 1 - 12
       
   for cell in range(256):
       row = int(cell / 9)
       col = cell % 9
       cell_to_groups_dict_sixteen[cell] = [row, col]
       possible_ints_sixteen[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']  # 1 - 16
                  
   fileName = sys.argv[1]
   file = open(fileName, "r")
   initial = []
   for puzzle in file:
      initial.append(list(puzzle))
   for puzzle in initial:
      puzzle = ''.join([str(i) for i in puzzle])
      puzzle = puzzle.strip()
      print("input state", "\n", "-------------------")
      display(puzzle)
      print("-------------------", "\n", "solution", "\n", "-------------------")
      length = math.sqrt(len(puzzle))
      if length == 9:
         cell_to_groups_dict = cell_to_groups_dict_nine
         possible_ints = possible_ints_nine
      elif length == 12:
         cell_to_groups_dict = cell_to_groups_dict_twelve
         possible_ints = possible_ints_twelve
      elif length == 16:
         cell_to_groups_dict = cell_to_groups_dict_sixteen
         possible_ints = possible_ints_sixteen

      solution = backtracking_search(puzzle, cell_to_groups_dict, possible_ints)
      solution = ''.join([str(i) for i in solution])
      display(solution)

if __name__ == '__main__':
    main()