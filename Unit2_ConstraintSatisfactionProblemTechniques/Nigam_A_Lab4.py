# Name: Arul Nigam
# Period: 3

from tkinter import *
from graphics import *
import math, time


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

    return (int(i / multirow) == int(j / multirow)) and (
            int(int(i % len) / subblockwidth) == int(int(j % len) / subblockwidth))


def same_square_len2(i, j, len):
    if len == 9:
        return j in sameblock9[i]
    elif len == 12:
        return j in sameblock12[i]
    else:
        return j in sameblock16[i]


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
    length = len(possible_ints)
    sqrtlength = int(math.sqrt(length))
    if sqrtlength == 9:
        near = near9[cell]
    elif sqrtlength == 12:
        near = near12[cell]
    else:
        near = near16[cell]
    for i in near:
        if i != cell:
            if assignment[i] != ".":
                if str(assignment[i]) == str(value):  # neighbors are the same:
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
    for value in possible_ints[cell]:  # possible_ints maps cell to [0 - 9]
        assignment[cell] = str(value)
        if isValid(value, cell, assignment, cell_to_groups_dict, possible_ints):
            result = recursive_backtracking(assignment, cell_to_groups_dict, possible_ints, length)
            if check_complete(result):
                return result
        assignment[cell] = "."
    return None


def checksum(pzl):
    length = len(pzl)
    ascii_sum = 0
    for p in range(length):
        ascii_sum += ord(pzl[p])
    ascii_sum -= 48 * length
    return ascii_sum


sameblock9 = [[] for i in range(81)]
sameblock12 = [[] for i in range(144)]
sameblock16 = [[] for i in range(256)]

near9 = [[] for i in range(81)]
near12 = [[] for i in range(144)]
near16 = [[] for i in range(256)]


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
        for j in range(81):
            if same_square_len(cell, j, 9):
                sameblock9[cell].append(j)
                near9[cell].append(j)
            elif row == int(j / 9):
                near9[cell].append(j)
            elif col == (j % 9):
                near9[cell].append(j)

    for cell in range(144):
        row = int(cell / 12)
        col = cell % 12
        cell_to_groups_dict_twelve[cell] = [row, col]
        possible_ints_twelve[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C']  # 1 - 12
        for j in range(144):
            if same_square_len(cell, j, 12):
                sameblock12[cell].append(j)
                near12[cell].append(j)
            elif row == int(j / 12):
                near12[cell].append(j)
            elif col == (j % 12):
                near12[cell].append(j)

    for cell in range(256):
        row = int(cell / 16)
        col = cell % 16
        cell_to_groups_dict_sixteen[cell] = [row, col]
        possible_ints_sixteen[cell] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']  # 1 - 16
        for j in range(256):
            if same_square_len(cell, j, 16):
                sameblock16[cell].append(j)
                near16[cell].append(j)
            elif row == int(j / 16):
                near16[cell].append(j)
            elif col == (j % 16):
                near16[cell].append(j)

    fileName = "puzzles.txt"
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    file = open(fileName, "r")
    initial = []
    for puzzle in file:
        initial.append(list(puzzle))
    initial_time = time.time()
    line = 1
    for puzzle in initial:
        puzzle = ''.join([str(i) for i in puzzle])
        puzzle = puzzle.strip()
        length = int(math.sqrt(len(puzzle)))
        print("Line", line, ": ", puzzle)
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
        print(checksum(solution), "-", solution)
        line += 1
        print("")
    print("Duration: ", time.time() - initial_time)


if __name__ == '__main__':
    main()
