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

def select_unassigned_var(assignment, length):
    # Select an unassigned variable - forward checking, MRV, or LCV
    # returns a variable
    size = length * length
    for key in range(size):
        if assignment[key] == ".":
            return key

def isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
    length = int(math.sqrt(len(possible_ints)))
    #subblockheight = int(math.sqrt(length))
    #subblockwidth = int(length/subblockheight)
    neighbors = []
    for i in range(length * length):
        if i != cell:
            if cell_to_groups_dict[cell][0] == int(i / length):  # same row
                neighbors.append(i)
            if cell_to_groups_dict[cell][1] == i % length:  # same col
                neighbors.append(i)
            if same_square_len(cell, i, length):  # same sub-square
                neighbors.append(i)
    for a in neighbors:
        if assignment[a] != ".":
            if str(assignment[a]) == str(value):  # neighbors are the same:
                return False  # invalid
    return True

def backtracking_search(initial, cell_to_groups_dict, possible_ints, length):
    return recursive_backtracking(list(initial), cell_to_groups_dict, possible_ints, length)

def recursive_backtracking(assignment, cell_to_groups_dict, possible_ints, length):
    if check_complete(assignment):
        s = ""
        for i in assignment:
            s += str(i)
        return s
    cell = select_unassigned_var(assignment, length)
    for value in possible_ints[cell]:  
        assignment[cell] = str(value)
        if isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
            result = recursive_backtracking(assignment, cell_to_groups_dict, possible_ints, length)
            if check_complete(result):
                return result
        assignment[cell] = "."
    return None

def display(solution, length):
    subblockheight = int(math.sqrt(length))
    subblockwidth = int(length/subblockheight)

    for i in range(0, length*length, subblockwidth):
        if((i % (length * subblockheight)) == 0):
            print("")
        print(solution[i:i+subblockwidth], " ", end = "")
        if(((i + subblockwidth) % length) == 0):
            print("")

'''def display(solution, length):

    if length == 9:
        for i in range(0, 81, 9):
            print(solution[i: i + 3], " ", solution[i + 3: i + 6], " ", solution[i + 6: i + 9])
            if i == 18 or i == 45:
                print("")

    if length == 12:
        for i in range(0, 144, 12):
            print(solution[i: i + 4], " ", solution[i + 4: i + 8], " ", solution[i + 8: i + 12])
            if i == 24 or i == 60 or i == 96:
                print("")

    if length == 16:
        for i in range(0, 256, 16):
            print(solution[i: i + 4], " ", solution[i + 4: i + 8], " ", solution[i + 8: i + 12])
            if i == 32 or i == 80:
                print("")'''

def same_square_len(i, j, len):
    if len == 9:
        subblockwidth = 3
        multirow = 27
    elif len == 12:
        subblockwidth = 4
        multirow = 36
    elif len == 16:
        subblockwidth = 4
        multirow = 64
    return (int(i / multirow) == int(j / multirow)) and (int((i % len) / subblockwidth) == int((j % len) / subblockwidth))
    
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
        row = int(cell / 12)
        col = cell % 12
        cell_to_groups_dict_twelve[cell] = [row, col]
        possible_ints_twelve[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C']  # 1 - 12

    for cell in range(256):
        row = int(cell / 16)
        col = cell % 16
        cell_to_groups_dict_sixteen[cell] = [row, col]
        possible_ints_sixteen[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']  # 1 - 16

    fileName = "puzzles.txt"
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    file = open(fileName, "r")
    initial = []
    for puzzle in file:
        initial.append(list(puzzle))
    for puzzle in initial:
        puzzle = ''.join([str(i) for i in puzzle])
        puzzle = puzzle.strip()
        length = int(math.sqrt(len(puzzle)))
        print("input state", "\n", "-------------------")
        print("puzzle length=", length)
        print("puzzle=",puzzle)
        time.sleep(10)
        display(puzzle, length)
        print("-------------------", "\n", "solution", "\n", "-------------------")
        if length == 9:
            cell_to_groups_dict = cell_to_groups_dict_nine
            possible_ints = possible_ints_nine
        elif length == 12:
            cell_to_groups_dict = cell_to_groups_dict_twelve
            possible_ints = possible_ints_twelve
        elif length == 16:
            cell_to_groups_dict = cell_to_groups_dict_sixteen
            possible_ints = possible_ints_sixteen
        solution = backtracking_search(puzzle, cell_to_groups_dict, possible_ints, length)
        solution = ''.join([str(i) for i in solution])
        display(solution, length)

if __name__ == '__main__':
    main()
