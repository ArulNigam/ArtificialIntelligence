# Name: Arul Nigam
# Period: 3

from tkinter import *
import math, time, copy


def display(solution, length):
    subblockheight = int(math.sqrt(length))
    subblockwidth = int(length / subblockheight)
    for i in range(0, length * length, subblockwidth):
        if ((i % (length * subblockheight)) == 0):
            print("")
        print(str(solution[i:i + subblockwidth]), " ", end="")
        if (((i + subblockwidth) % length) == 0):
            print("")


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
    if assignment is None:
        return False
    return "." not in assignment


def select_unassigned_var(assignment, length, possible_ints):
    # Select an unassigned variable - forward checking, MRV, or LCV
    # returns a variable
    size = length * length
    minints = length
    minkey = 0

    for key in range(size):
        if assignment[key] == ".":
            numberofints = len(possible_ints[key])
            if numberofints == 0 or numberofints == 2:
                return key
            elif (numberofints < minints):
                minints = numberofints
                minkey = key

    return minkey


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
    newassignment = copy.deepcopy(assignment)
    #print("-->",assignment)
    size = length * length

    if length == 9:
        near = near9
    elif length == 12:
        near = near12
    else:
        near = near16

    # Setup possible values for each position
    for i in range(size):
        if newassignment[i] == ".":
            possible_ints[i] = sudokunumbers[0:length]
            for neighbor in near[i]:
                if newassignment[neighbor] != ".":
                    if str(newassignment[neighbor]) in str(possible_ints[i]):
                        possible_ints[i].remove(newassignment[neighbor])

    # Assign the easy ones
    change = TRUE
    while change:
        change = FALSE
        for i in range(size):
            if newassignment[i] == ".":
                if len(possible_ints[i]) == 1:
                    newassignment[i] = str(possible_ints[i][0])
                    change = TRUE
                    for neighbor in near[i]:
                        if possible_ints[i][0] in possible_ints[neighbor]:
                            possible_ints[neighbor].remove(possible_ints[i][0])

    # Assign unique ones in row
    change = TRUE
    while change:
        change = FALSE
        for i in range(0, size, length):
            rowints = []
            for j in range(i, i + length):
                rowints = rowints + possible_ints[j]
            for j in range(length):
                if rowints.count(sudokunumbers[j]) == 1:
                    for cell in range(i, i + length):
                        if newassignment[cell] == ".":
                            if sudokunumbers[j] in possible_ints[cell]:
                                newassignment[cell] = str(sudokunumbers[j])
                                change = TRUE

    # Assign unique ones in column
    change = TRUE
    while change:
        change = FALSE
        for i in range(0, length):
            colints = []
            for j in range(i, size, length):
                colints = colints + possible_ints[j]
            for j in range(length):
                if colints.count(sudokunumbers[j]) == 1:
                    for cell in range(i, size, length):
                        if newassignment[cell] == ".":
                            if sudokunumbers[j] in possible_ints[cell]:
                                newassignment[cell] = str(sudokunumbers[j])
                                change = TRUE

    # Check for completion
    if check_complete(newassignment):
        return "".join(newassignment)

    # Do the harder ones with backtracking
    cell = select_unassigned_var(newassignment, length, possible_ints)
    values = copy.deepcopy(possible_ints[cell])
    for value in values:
        newassignment[cell] = str(value)
        if isValid(value, cell, newassignment, cell_to_groups_dict, possible_ints):
            result = recursive_backtracking(newassignment, cell_to_groups_dict, possible_ints, length)
            if check_complete(result):
                return result
        newassignment[cell] = "."

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

sudokunumbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def main():
    cell_to_groups_dict = {}
    possible_ints9 = [[] for i in range(81)]
    possible_ints12 = [[] for i in range(144)]
    possible_ints16 = [[] for i in range(256)]

    for cell in range(81):
        row = int(cell / 9)
        col = cell % 9

        for j in range(81):
            if j != cell:
                if same_square_len(cell, j, 9):
                    sameblock9[cell].append(j)
                    near9[cell].append(j)
                elif row == int(j / 9):
                    near9[cell].append(j)
                elif col == (j % 9):
                    near9[cell].append(j)
        while cell in near9[cell]:
            near9[cell].remove(cell)

    for cell in range(144):
        row = int(cell / 12)
        col = cell % 12
        for j in range(144):
            if same_square_len(cell, j, 12):
                sameblock12[cell].append(j)
                near12[cell].append(j)
            elif row == int(j / 12):
                near12[cell].append(j)
            elif col == (j % 12):
                near12[cell].append(j)
        while cell in near12[cell]:
            near12[cell].remove(cell)

    for cell in range(256):
        row = int(cell / 16)
        col = cell % 16
        for j in range(256):
            if same_square_len(cell, j, 16):
                sameblock16[cell].append(j)
                near16[cell].append(j)
            elif row == int(j / 16):
                near16[cell].append(j)
            elif col == (j % 16):
                near16[cell].append(j)
        while cell in near16[cell]:
            near16[cell].remove(cell)

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
        if length == 9:
            near = near9
            possible_ints = possible_ints9
        elif length == 12:
            near = near12
            possible_ints = possible_ints12
        else:
            near = near16
            possible_ints = possible_ints16

        print("Line", line, ": ", puzzle)

        solution = backtracking_search(puzzle, cell_to_groups_dict, possible_ints, length)
        solution = ''.join([str(i) for i in solution])
        print(checksum(solution), "-", solution)
        line += 1
        print("")
    print("Duration: ", time.time() - initial_time)


if __name__ == '__main__':
    main()
