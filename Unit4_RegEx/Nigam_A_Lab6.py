# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, re, sys, time, random, queue

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "~"


class Crossword:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [OPENCHAR] * (self.height * self.width)
        self.length = len(self.board)

    def addblock(self, xw, blocked_goal, level=0):
        blocked_so_far = xw.count(BLOCKCHAR)
        if blocked_so_far >= blocked_goal:
            if self.is_valid(xw):
                return xw
            return ""
        if blocked_goal % 2 != 0:
            xw = xw[0:(len(xw) // 2)] + BLOCKCHAR + xw[((len(xw) // 2) + 1):]
            if blocked_goal == 1:
                return xw
        elif blocked_goal == ((self.width + 2) * (self.height + 2)):
            return BLOCKCHAR * ((self.width + 2) * (self.height + 2))

        pick_from = []
        for i in range(len(xw)):
            if (xw[i] != BLOCKCHAR) and (xw[i] != PROTECTEDCHAR):
                pick_from.append(i)
        if len(xw) // 2 in pick_from:
            pick_from.remove(len(xw) // 2)

        for i in range(len(pick_from)):
            # place two blocks
            tempxw = xw
            xw = xw[0:pick_from[i]] + BLOCKCHAR + xw[pick_from[i] + 1:]
            xw = xw[0:len(xw) - 1 - pick_from[i]] + BLOCKCHAR + xw[len(xw) -
                                                                   pick_from[
                                                                       i]:]
            newH = len(xw) // (self.width + 2)
            for counter in range(2):
                xw = re.sub("[#]-(?=[#])", "##", xw)
                xw = re.sub("[#]--(?=[#])", "###", xw)
                xw = self.transpose(xw, len(xw) // newH)
                newH = len(xw) // newH

            # Block Fill
            start = xw.find(OPENCHAR)
            areafilled = self.area_fill(xw, start)
            if areafilled.count(OPENCHAR) > 0:
                for j in range(len(areafilled)):
                    if areafilled[j] == OPENCHAR:
                        xw = xw[0:j] + BLOCKCHAR + xw[j + 1:]

            if (re.search("[#](.?[~]|[~].?)[#]", xw) is None) and (
                    re.search("[#](.?[~]|[~].?)[#]",
                              self.transpose(xw, len(xw) // newH)) is None):

                if xw.count(BLOCKCHAR) <= blocked_goal:
                    ret = ""
                    if xw.count("#--#") == 0 and xw.count("#-#") == 0:
                        ret = self.addblock(xw, blocked_goal, level + 1)
                    elif xw.count(BLOCKCHAR) <= blocked_goal - 6:
                        xw = xw.replace("#---", "####", 1)
                        xw = xw.replace("---#", "####", 1)
                        for counter in range(2):
                            xw = re.sub("[#]-(?=[#])", "##", xw)
                            xw = re.sub("[#]--(?=[#])", "###", xw)
                            xw = self.transpose(xw, len(xw) // newH)
                            newH = len(xw) // newH
                            ret = self.addblock(xw, blocked_goal, level + 1)

                        if ret != "":
                            return ret
                    if ret != "":
                        return ret
            xw = tempxw

        print("Add block 2 failed")
        return ""

    def add_border(self, xw):
        ret = BLOCKCHAR * (self.width + 2)
        for i in range(self.height):
            ret += BLOCKCHAR
            ret += ''.join(xw[(self.width * i):(self.width * i + self.width)])
            ret += BLOCKCHAR
        ret += BLOCKCHAR * (self.width + 2)
        return ret

    def add_protected(self, xw):
        xw = list(xw)
        for i in range(len(xw)):
            if xw[i] != BLOCKCHAR and xw[i] != OPENCHAR:
                xw[i] = PROTECTEDCHAR

        xw = ''.join(xw)
        xw = self.make_palindrome(xw)

        newH = len(xw) // (self.width + 2)
        for counter in range(2):
            xw = re.sub("#((~--)|(-~-)|(--~)|(~~-)|(-~~))", "#~~~", xw)
            xw = re.sub("((~--)|(-~-)|(--~)|(~~-)|(-~~))#", "~~~#", xw)

            xw = re.sub("[#]-(?=[#])", "##", xw)
            xw = re.sub("[#]--(?=[#])", "###", xw)

            xw = self.transpose(xw, len(xw) // newH)
            newH = len(xw) // newH

        xw = self.make_palindrome(xw)
        return xw

    def area_fill(self, board, sp):
        if sp < 0 or sp >= len(board):
            return board
        if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
            board = board[0:sp] + '?' + board[sp + 1:]
            width = self.width + 2
            dirs = [-1, width, 1, -1 * width]
            for d in dirs:
                if d == -1 and sp % width == 0:
                    continue  # left edge
                if d == 1 and sp + 1 % width == 0:
                    continue  # right edge
                board = self.area_fill(board, sp + d)
        return board

    def check_connectivity(self, xw):
        start = xw.find(OPENCHAR)
        xw = self.area_fill(xw, start)
        return xw.count(OPENCHAR) == 0

    def is_valid(self, xw):

        xw = xw.replace(PROTECTEDCHAR, OPENCHAR)
        if xw.count("#--#") > 0 or xw.count("#-#") > 0:
            return False
        temp = self.transpose(xw, self.width + 2)
        if temp.count("#--#") > 0 or temp.count("#-#") > 0:
            return False
        return self.check_connectivity(xw)

    def make_palindrome(self, xw):
        xw = list(xw)
        length = len(xw) - 1
        for i in range(length):
            if xw[i] == PROTECTEDCHAR:
                xw[length - i] = PROTECTEDCHAR
            elif xw[i] == BLOCKCHAR:
                xw[length - i] = BLOCKCHAR
        return ''.join(xw)

    def print_board(self, board, additional_thickness=2):
        if board is None:
            print("Board is none!")
        else:
            for i in range(self.height + additional_thickness):
                print(board[((self.width + additional_thickness) * i):(
                        (self.width + additional_thickness) * (i + 1))])
        print()

    def set_initial(self, initial_values, blocked_goal):
        xw = self.board
        xw = list(xw)
        for i in initial_values:
            xw[i[0]] = i[1]
        xw = ''.join(xw)
        xw = self.add_border(xw)
        xw = self.add_protected(xw)

        xw = self.addblock(xw,
                           blocked_goal + ((self.width + self.height + 2) * 2))

        xw = list(xw)
        for i in initial_values:
            xw[((i[0] // self.width) + 1) * (self.width + 2) + (
                    1 + i[0] % self.width)] = i[1]
        xw = ''.join(xw)
        xw = xw.replace(PROTECTEDCHAR, OPENCHAR)
        # print("added letters back + openchar")
        # self.print_board(xw)

        xw = xw[(self.width + 2):(len(xw) - (self.width + 2))]
        ret = ""
        for i in range(self.height):
            ret += xw[(1 + i * (self.width + 2)):(
                    self.width + 1 + i * (self.width + 2))]
        self.board = list(ret)

    def transpose(self, xw, width):
        height = len(xw) // width
        temp = [0] * len(xw)
        xw = list(xw)
        for i in range(len(xw)):
            x = i // width
            y = i % width
            temp[int((y * height) + x)] = xw[i]

        return ''.join(temp)

    # ****************************************** CLASS: ABOVE = LAB 5, BELOW = LAB 6 ******************************************

    def connected_words(self, xw):
        arcs = {}
        connections = {}
        h_start, h_end, v_start, v_end = -1, -1, -1, -1
        for i in range(len(xw)):
            if xw[i] == "-":
                # HORIZONTAL:
                h_start = i
                while xw[h_start - 1] != BLOCKCHAR:
                    h_start = h_start - 1
                h_end = i
                while xw[h_end + 1] != BLOCKCHAR:
                    h_end = h_end + 1
                # VERTICAL:
                v_start = i
                while xw[v_start - self.width - 2] != BLOCKCHAR:
                    v_start = v_start - self.width - 2
                v_end = i
                while xw[v_end + self.width + 2] != BLOCKCHAR:
                    v_end = v_end + self.width + 2
                arcs[i] = [xw[h_start:h_end], xw[v_start:v_end:self.width]]
                connections[arcs[i][0] + arcs[i][1]] = [h_start, h_end, v_start, v_end]
        return connections, arcs

    def fill(self, guess, start, xw, is_vertical):
        guess = guess[0]

        if is_vertical:
            xw = list(xw)
            for i in range(len(guess)):
                xw[start + (i * (self.width + 2))] = guess[i]
            xw = ''.join(xw)
        else:  # horizontal
            xw = xw[0:start] + guess + xw[start + len(guess):]

        return xw

    def find_longest_word(self, xw):

        horizontal_start = -1
        horizontal_length = -1
        for i in range(self.width, 1, -1):
            if horizontal_start == -1:
                rgx = "#[\w-]{}{}{}#".format("{", i, "}")
                for match in re.finditer(rgx, xw):
                    horizontal_start = match.start()
                    e = match.end()
                    horizontal_length = e - horizontal_start - 2
                    hgroup = xw[horizontal_start + 1:e - 1]
                    if hgroup.find("-") == -1:
                        horizontal_start = -1
                        horizontal_length = -1
                    else:
                        break

        vertical_start = -1
        vertical_length = -1
        xw = self.transpose(xw, self.width + 2)
        for i in range(self.height, 1, -1):
            if vertical_start == -1:
                rgx = "#[\w-]{}{}{}#".format("{", i, "}")
                for match in re.finditer(rgx, xw):
                    vertical_start = match.start()
                    # NEED TO TRANSPOSE
                    e = match.end()
                    vertical_length = e - vertical_start - 2
                    vgroup = xw[vertical_start + 1:e - 1]
                    if vgroup.find("-") == -1:
                        vertical_start = -1
                        vertical_length = -1
                    else:
                        break

        if horizontal_length >= vertical_length and horizontal_length > 0:
            return horizontal_start, False, horizontal_length, hgroup
        elif horizontal_length < vertical_length:
            x = vertical_start // (self.height + 2)
            y = vertical_start % (self.height + 2) + 1
            vertical_start = int(y * (self.width + 2) + x - 1)
            return vertical_start, True, vertical_length, vgroup

        print("Could not find longest word")
        return vertical_start, True, vertical_length, vgroup

    def solve(self, words_by_length, words):
        xw = ''.join(self.board)
        xw = self.add_border(xw)
        connections, arcs = self.connected_words(xw)
        xw = self.solve_helper(xw, words_by_length, connections, arcs, words)
        print("Done Solve")
        self.print_board(xw)
        '''xw = xw[(self.width + 2):(len(xw) - (self.width + 2))]
        ret = ""
        for i in range(self.height):
            ret += xw[(1 + i * (self.width + 2)):(
                    self.width + 1 + i * (self.width + 2))]
        self.board = list(ret)'''
        # return ret

    def solve_helper(self, xw, words_by_length, connections, arcs, words):
        if xw.find(OPENCHAR) < 0:
            return xw
        start, is_vertical, length, rgx = self.find_longest_word(xw)
        print("in solve_helper, with isvert, rgx, board", is_vertical, rgx)
        # self.print_board(xw)
        rgx = rgx.replace("-", ".")
        for guess in words_by_length[length]:
            ret = None
            if re.search(rgx, guess[0]):
                filled = self.fill(guess, start + 1, xw, is_vertical)
                if self.check_valid(filled, xw, start, connections, arcs, words_by_length):  # word is good
                    words_by_length[length].remove(
                        guess)  ###########################################################################################
                    self.print_board(filled)
                    ret = self.solve_helper(filled, words_by_length, connections, arcs, words)
            if ret is not None:
                # print("found:")
                # self.print_board(ret)
                print(ret, "ohsaohsohsaiohs")
                return ret

    def check_valid(self, new, old, start, connections, arcs, words_by_length):
        print(arcs)
        temp = connections[arcs[start + 1][0] + arcs[start + 1][1]]
        # Trying this for each letter of horizonal word - need to do vertical too
        for i in range(temp[0], temp[1]):
            temp2 = connections[arcs[i][0] + arcs[i][1]]
            word = new[temp2[2]:temp2[3] + (self.width + 2):(self.width + 2)]
            word = word.replace("-", ".")
            word_len = len(word)
            v_match = False
            for v_l in words_by_length[word_len]:
                v = v_l[0]
                if re.search(word, v):
                    v_match = True
                    break
            if not v_match:
                return False

        for i in range(temp[2], temp[3] + (self.width + 2), (self.width + 2)):
            temp2 = connections[arcs[i][0] + arcs[i][1]]
            word = new[temp2[0]:temp2[1] + 1]
            word = word.replace("-", ".")
            word_len = len(word)
            v_match = False
            for v_l in words_by_length[word_len]:
                v = v_l[0]
                if re.search(word, v):
                    v_match = True
                    break
            if not v_match:
                return False

        return True


class CSPSolver:
    worklist = queue.Queue()  # a queue of arcs (this can be a queue or set in ac-3)

    # arcs: list of tuples
    # domains: dict of { tuples: list }
    # constraints: dict of { tuples: list }
    def __init__(self, arcs: list, domains: dict, constraints: dict):
        self.arcs = arcs
        self.domains = domains
        self.constraints = constraints

    # returns an empty dict if an inconsistency is found and domains for variables otherwise
    # generate: bool (choose whether or not to use a generator)
    def solve(self, generate=False):
        result = self.solve_helper()
        if generate:
            print("ret", return_value)
            return result
        else:
            return_value = []
            for step in result:
                if step == None:
                    return step  # inconsistency found
                else:
                    return_value = step
            print("ret", return_value)
            return return_value[1]  # return only the final domain

    # returns a generator for each step in the algorithm, including the end result
    # each yield is a tuple containing: (edge, new domains, edges to consider)
    def solve_helper(self):
        # setup queue with given arcs
        [self.worklist.put(arc) for arc in self.arcs]
        # continue working while worklist is not empty
        while not self.worklist.empty():
            (xi, xj) = self.worklist.get()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    # found an inconsistency
                    yield None
                    break
                # get all of xj's neighbors
                neighbors = [neighbor for neighbor in self.arcs if neighbor[0] == xj]
                # put all neighbors into the worklist to be evaluated
                [self.worklist.put(neighbor) for neighbor in neighbors]
                yield (xi, xj), self.domains, neighbors
            else:
                yield (xi, xj), self.domains, None
        # yield the final return value
        yield None, self.domains, None

    # returns true if and only if the given domain i

    def revise(self, xi: object, xj: object):
        revised = False
        # get the domains for xi and xj
        xi_domain = self.domains[xi]
        xj_domain = self.domains[xj]
        # get a list of constraints for (xi, xj)
        constraints = self.constraints[xi+xj]
        for x in xi_domain[:]:
            satisfies = False  # there is a value in xjDomain that satisfies the constraint(s) between xi and xj
            for y in xj_domain:
   #             for constraint in constraints:
                # check y against x for each constraint
                if x[0][constraints[0]] == y[0][constraints[1]]:
                    satisfies = True
                    break
            if not satisfies:
                # delete x from xiDomain
                xi_domain.remove(x)
                revised = True
        return revised


def sort_by_richness(words, frequency):
    temp = []
    for w in words:
        temp.append([w, word_richness(w, frequency)])
    return sorted(temp, key=lambda x: x[1], reverse=True)


def word_richness(word, frequency):
    richness = 0
    for i in range(len(word)):
        richness += frequency[word[i]]
    return richness


def find_horizontal_words(puzzle, xw):
    horizontal_words = {}
    word_count = 0
    while "-" in xw:
        start = xw.index("-")
        temp = start + 2
        while xw[temp + 1] != "#":
            temp += 1
        words_list = [i for i in range(start, temp + 1)]
        horizontal_words["h" + str(word_count)] = [words_list, len(words_list)]
        word_count += 1
        xw = xw.replace("-", "*", temp + 1 - start)
    return horizontal_words


def find_vertical_words(puzzle, xw, transposed_table):
    vertical_words = {}
    word_count = 0
    newH = len(xw) // (puzzle.width + 2)
    xw = puzzle.transpose(xw, len(xw) // newH)
    length = len(xw)
    while "-" in xw:
        start = xw.index("-")
        temp = start + 2
        while xw[temp + 1] != "#":
            temp += 1
        words_list = [i for i in range(transposed_table[start], transposed_table[temp] + 1, puzzle.width + 2)]
        vertical_words["v" + str(word_count)] = [words_list, len(words_list)]
        word_count += 1
        xw = xw.replace("-", "*", temp + 1 - start)
    return vertical_words


def transposed_table(puzzle, xw):
    length = len(xw)
    width = (puzzle.width + 2)
    height = length // width
    table = {}
    for i in range(length):
        x = i // width
        y = i % width
        table[int(y * height) + x] = i
    return table


def find_arc(horizontal_words, vertical_words):
    arcs = []
    arc_table = {}
    for h_word in horizontal_words.keys():
        for v_word in vertical_words.keys():
            intersection = set(horizontal_words[h_word][0]).intersection(set(vertical_words[v_word][0]))
            if len(intersection) == 1:  # words intersect somewhere
                arcs.append([h_word, v_word])
                arcs.append([v_word, h_word])
                space = intersection.pop()
                arc_table[h_word + v_word] = [horizontal_words[h_word][0].index(space),
                                              vertical_words[v_word][0].index(space)]
                arc_table[v_word + h_word] = [vertical_words[v_word][0].index(space),
                                              horizontal_words[h_word][0].index(space)]
    return arcs, arc_table


def ac3solve(puzzle, words_by_length):
    xw = ''.join(puzzle.board)
    xw = puzzle.add_border(xw)
    domains = {}
    horiz = find_horizontal_words(puzzle, xw)
    vert = find_vertical_words(puzzle, xw, transposed_table(puzzle, xw))
    for h_word in horiz:
        domains[h_word] = words_by_length[horiz[h_word][1]]
    for v_word in vert:
        domains[v_word] = words_by_length[vert[v_word][1]]
    arcs, constraints = find_arc(horiz, vert)
    # print(domains)
    print(arcs)
    print(constraints)
    # print(horiz)
    solver = CSPSolver(arcs, domains, constraints)
    print(len(domains["h4"]))
    ret = solver.solve()
    print(len(solver.domains["h4"]))
    return ret

def main():
    int_test = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V|h|v)(\d+)x(\d+)(.+)$"]
    user_input = sys.argv
    for i, v in enumerate(user_input):
        print(i, v)
    initial_values = []
    for i in range(1, len(user_input)):
        if re.match(int_test[0], user_input[i]):  # board size
            result = re.search(r"^(\d+)x(\d+)$", user_input[i])
            height = int(result.group(1))
            width = int(result.group(2))
        elif os.path.isfile(user_input[i]):  # filename scrabble
            filename = user_input[i]
        elif re.match(int_test[1], user_input[i]):  # number of blocked squares
            blocked_square_count = int(user_input[i])
        elif re.match(int_test[2], user_input[i]):  # coordinate + word
            is_vertical = (user_input[i][0] == "V") or (
                    user_input[i][0] == "v")
            result = re.search(r"^(H|V)(\d+)x(\d+)(.+)$", user_input[i],
                               re.IGNORECASE)
            start_index = [int(result.group(2)), int(result.group(3))]
            word = result.group(4)
            if is_vertical:
                for j in range(len(word)):
                    board_pos = (start_index[0] + j) * width + start_index[1]
                    initial_values.append([board_pos, word[j]])
            else:
                for j in range(len(word)):
                    board_pos = (start_index[0] * width) + start_index[1] + j
                    initial_values.append([board_pos, word[j]])
    puzzle = Crossword(height, width)
    puzzle.set_initial(initial_values, blocked_square_count)
    # ****************************************** MAIN: ABOVE = LAB 5, BELOW = LAB 6 ******************************************
    frequency, words_by_length, words = {}, {}, set()
    file = open(filename, 'r')
    for word in file:
        word = word.upper().strip()
        words.add(word)
        for v in word:
            if v in frequency:
                frequency[v] += 1
            else:
                frequency[v] = 1
        length = len(word)
        if length in words_by_length:
            words_by_length[length].append(word)
        else:
            words_by_length[length] = [word]
    for i in words_by_length:
        words_by_length[i] = sort_by_richness(words_by_length[i], frequency)
    ret = ac3solve(puzzle, words_by_length)
    # ret = puzzle.solve(words_by_length, words)
    # puzzle.board=list(ret)
    print("In main, result:", ret)


if __name__ == '__main__':
    main()
