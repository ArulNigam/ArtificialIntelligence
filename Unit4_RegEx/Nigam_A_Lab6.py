# Arul Nigam
# Period 3
# Crossword Pt. 2

import os, re, sys, time, random, copy, string, timeit, fnmatch

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "~"


class Crossword():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [OPENCHAR] * (self.height * self.width)
        self.length = len(self.board)
        self.max_score = 0

    def addblock(self, xw, blocked_goal, level=0):
        print("xw=", xw, "blocked_goal=", blocked_goal, "level=", level)
        time.sleep(.2)
        blocked_so_far = xw.count(BLOCKCHAR)
        if blocked_so_far >= blocked_goal:
            if self.is_valid(xw):
                return xw
            else:
                return ""
        if blocked_goal % 2 != 0:
            xw = xw[0:((len(xw) // 2))] + BLOCKCHAR + xw[((len(xw) // 2) + 1):]
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
            xw = xw[0:len(xw) - 1 - pick_from[i]] + BLOCKCHAR + xw[len(xw) - pick_from[i]:]
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
                for i in range(len(areafilled)):
                    if areafilled[i] == OPENCHAR:
                        xw = xw[0:i] + BLOCKCHAR + xw[i + 1:]
            bool1 = re.search("[#](.?[~]|[~].?)[#]", xw) is None
            print("xw")
            self.print_board(xw)
            transp_xw = self.transpose(xw, len(xw) // newH)
            print("transp_xw")
            self.print_board(transp_xw)
            bool2 = re.search("[#](.?[~]|[~].?)[#]", transp_xw) is None
            if bool1 and bool2:
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
            if xw[i] != BLOCKCHAR and xw[i] != OPENCHAR:  # if char is a letter
                xw[i] = PROTECTEDCHAR
        xw = ''.join(xw)
        xw = re.sub("#--~--#", "#~~~AA#", xw)
        xw = self.make_palindrome(xw)
        xw = re.sub("#--~~~#", "#AA~~~#", xw)
        newH = len(xw) // (self.width + 2)

        xw = re.sub("#((~----)|(-~---)|(-~~--)|(~-~--)|(~~---))#", "#~~~AA#", xw)
        xw = re.sub("#((---~-)|(----~)|(---~~)|(--~-~)|(--~~-))#", "#AA~~~#", xw)
        xw = re.sub("#((~--)|(-~-)|(--~)|(~~-)|(-~~)|(~-~))", "#~~~", xw)
        xw = re.sub("((~--)|(-~-)|(--~)|(~~-)|(-~~)|(~-~))#", "~~~#", xw)
        self.print_board(xw)
        xw = re.sub("A", "-", xw)
        xw = re.sub("#-(?=#)", "##", xw)
        xw = re.sub("#--(?=#)", "###", xw)

        xw = self.make_palindrome(xw)
        print("protected f")
        self.print_board(xw)
        return xw

    def area_fill(self, board, sp):
        if sp < 0 or sp >= len(board): return board
        if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
            board = board[0:sp] + '?' + board[sp + 1:]
            width = self.width + 2
            dirs = [-1, width, 1, -1 * width]
            for d in dirs:
                if d == -1 and sp % width == 0: continue  # left edge
                if d == 1 and sp + 1 % width == 0: continue  # right edge
                board = self.area_fill(board, sp + d)
        return board

    def check_connectivity(self, xw):
        start = xw.find(OPENCHAR)
        xw = self.area_fill(xw, start)
        ret = xw.count(OPENCHAR) == 0
        print("check connectivity=", ret)
        return True
        return xw.count(OPENCHAR) == len(self.connectivity_helper(start, xw, set(), set()))

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
        for i in range(self.height + additional_thickness):
            print(board[((self.width + additional_thickness) * i):((self.width + additional_thickness) * (i + 1))])
        print()

    def print_board2(self, board, additional_thickness=2):
        for i in range(self.width + additional_thickness):
            print(board[((self.height + additional_thickness) * i):((self.height + additional_thickness) * (i + 1))])
        print()

    def print_board_final(self, board):
        for i in range(1, self.height + 1):
            print(board[1 + ((self.width + 2) * i):((self.width + 2) * (i + 1)) - 1])
        print()

    def set_initial(self, initial_values, blocked_goal):
        xw = self.board
        xw = list(xw)
        for i in initial_values:
            xw[i[0]] = i[1]
        xw = ''.join(xw)
        xw = self.add_border(xw)
        xw = self.add_protected(xw)
        xw = self.addblock(xw, blocked_goal + ((self.width + self.height + 2) * 2))
        xw = list(xw)
        for i in initial_values:
            xw[((i[0] // self.width) + 1) * (self.width + 2) + (1 + i[0] % self.width)] = i[1]
        xw = ''.join(xw)
        xw = xw.replace(PROTECTEDCHAR, OPENCHAR)

        xw = xw[(self.width + 2):(len(xw) - (self.width + 2))]
        ret = ""
        for i in range(self.height):
            ret += xw[(1 + i * (self.width + 2)):(self.width + 1 + i * (self.width + 2))]
        self.print_board(ret, 0)
        self.board = list(ret)

    def transpose(self, xw, width):
        height = len(xw) // (width)
        temp = [0] * len(xw)
        xw = list(xw)
        for i in range(len(xw)):
            x = i // (width)
            y = i % (width)
            temp[int((y * height) + x)] = xw[i]
        return ''.join(temp)

    def find_arcs(self, horiz, vert):
        arcs, constraints = {}, {}
        for h_word in horiz:
            for v_word in vert:
                intersection = set(horiz[h_word][0]).intersection(set(vert[v_word][0]))
                if len(intersection) == 1:
                    if h_word in arcs.keys():
                        arcs[h_word].append(v_word)
                    else:
                        arcs[h_word] = [v_word]
                    if v_word in arcs.keys():
                        arcs[v_word].append(h_word)
                    else:
                        arcs[v_word] = [h_word]
                    space = intersection.pop()
                    constraints[h_word + v_word] = [horiz[h_word][0].index(space), vert[v_word][0].index(space)]
                    constraints[v_word + h_word] = [vert[v_word][0].index(space), horiz[h_word][0].index(space)]
        print("ARCS", arcs)
        return arcs, constraints

    def score(self, board, arcs, finder, dict_string):
        score = 0
        for word in arcs.keys():
            current_word = finder[word]
            candidate_word = self.get_word(board, current_word)
            if "-" not in candidate_word:
                if candidate_word in dict_string[len(candidate_word)]:
                    score += len(candidate_word)
        return score

    def solve(self, horiz, vert, board, words_by_length, regex_by_length):
        print(words_by_length)
        work = list()
        finder = {}
        all_words = []
        h_lengths = 0
        v_lengths = 0
        for h_word in horiz:
            all_words.append(h_word)
            length = len(horiz[h_word][0])
            h_lengths += length
            work.append({"name": h_word, "start": horiz[h_word][0][0],
                         "end": horiz[h_word][0][-1], "word": "",
                         "length": length})
            if h_word not in finder.keys():
                finder[h_word] = {"name": h_word, "start": horiz[h_word][0][0],
                                  "end": horiz[h_word][0][-1],
                                  "word": "-" * length, "length": length}
        for v_word in vert:
            all_words.append(v_word)
            length = len(vert[v_word][0])
            v_lengths += length
            work.append(
                {"name": v_word, "start": vert[v_word][0][0],
                 "end": vert[v_word][0][-1], "word": "-" * length,
                 "length": length})
            if v_word not in finder.keys():
                finder[v_word] = {"name": v_word, "start": vert[v_word][0][0],
                                  "end": vert[v_word][0][-1],
                                  "word": "-" * length, "length": length}
        arcs, constraints = self.find_arcs(horiz, vert)
        biggest_dict_size = 0
        biggest_dict_key = ""
        only_do = "x"
        if h_lengths >= 49:
            only_do = "h"
        elif v_lengths >= 49:
            only_do = "v"
        if only_do == "h" and v_lengths > h_lengths:  # v > h >= 49
            only_do = "v"
        for key in arcs:
            if len(arcs[key]) > biggest_dict_size:
                biggest_dict_key = key
                biggest_dict_size = len(arcs[key])
                print("biggest:", biggest_dict_key, biggest_dict_size)
        print("words 2", all_words)
        prioritized_work = [finder[biggest_dict_key]]
        all_words.remove(biggest_dict_key)
        temp_q = copy.deepcopy(arcs[biggest_dict_key])
        while len(temp_q) > 0:
            word = temp_q.pop(0)
            if word in all_words:
                prioritized_work.append(finder[word])
                all_words.remove(word)
                temp_q = temp_q + arcs[word]
        if only_do == "x":
            final_work = prioritized_work
        else:
            final_work = [task for task in prioritized_work if only_do in task["name"]]
        dict_string = {}
        for i in words_by_length.keys():
            string_i = "@"
            for j in words_by_length[i]:
                string_i += j
                string_i += "@"
            dict_string[i] = string_i
        return self.back_solve(final_work, finder, arcs, constraints,
                               board, words_by_length, dict_string, regex_by_length, 0)

    def back_solve(self, work, finder, arcs, constraints, board, words_by_length, dict_string, regex_by_length,
                   recur_depth):
        if len(work) == 0:
            return board
        current_space = work.pop(0)
        current_space["word"] = self.get_word(board, current_space)
        rgx_word = current_space["word"].replace("-", ".")
        rgx_letters = list(rgx_word.replace(".", ""))
        word_len = len(current_space["word"])
        words_to_iterate = words_by_length[word_len]
        for letter in rgx_letters:
            words_to_iterate = [x for x in words_to_iterate if letter in x]
        rgx = re.compile(rgx_word)
        for temp_word in words_to_iterate:
            if rgx.match(temp_word):
                current_space["word"] = temp_word
                current_space_word = current_space["name"]
                temp_board = self.add_word(board, current_space)
                valid, new_score = self.regex_is_valid(temp_board, arcs, finder, temp_word, words_by_length,
                                                       dict_string, current_space_word)
                if new_score > self.max_score:
                    self.print_board_final(board)
                    self.max_score = new_score
                if valid:
                    ret = self.back_solve(copy.deepcopy(work), finder, arcs, constraints, temp_board,
                                          words_by_length, dict_string, regex_by_length, recur_depth + 1)
                    if ret is not None:
                        return ret
        return None

    def regex_is_valid(self, board, arcs, finder, temp_word, words_by_length, dict_string, word_try):
        used_words = []
        score = 0
        for word in arcs.keys():
            current_word = finder[word]
            candidate_word = self.get_word(board, current_word)
            if "-" not in candidate_word:
                if candidate_word in used_words:
                    return False, score
                used_words.append(candidate_word)
                score += len(candidate_word)
        for word in arcs[word_try]:
            current_word = finder[word]
            candidate_word = self.get_word(board, current_word)
            # Reject duplicate words
            if "-" not in candidate_word:
                if candidate_word not in dict_string[len(candidate_word)]:
                    return False, score
            else:
                rgx = "@" + candidate_word.replace("-", ".")
                if not re.search(rgx, dict_string[len(rgx) - 1]):
                    # print("returning false with candidate[",rgx,"] - [", candidate_word,"]")
                    return False, score
        return True, score

    def get_word(self, board, current_space):

        start, end, word = current_space["start"], current_space["end"], current_space["word"]
        is_vertical = "v" in current_space["name"]
        step = 1
        if is_vertical:
            step = self.width + 2
        ret = board[start: end + step:step]

        return ret

    def add_word(self, board, current_space):
        start, end, word = current_space["start"], current_space["end"], current_space["word"]
        is_vertical = "v" in current_space["name"]
        if is_vertical:
            newH = len(board) // (self.width + 2)
            board = self.transpose(board, len(board) // newH)
            start = self.reverse_transposed_table(board)[start]
            end = self.reverse_transposed_table(board)[end]
        ret = board[:start] + word + board[start + len(word):]
        if is_vertical:
            ret = self.transpose(ret, newH)
        return ret

    def reverse_transposed_table(puzzle, xw):
        length = len(xw)
        width = (puzzle.width + 2)
        height = length // width
        table = {}
        for i in range(length):
            x = i // width
            y = i % width
            table[i] = int(y * height) + x
        return table


def sort_by_richness(words, frequency):
    temp = []
    for w in words:
        temp.append([w, word_richness(w, frequency)])
    sorted_with_values = sorted(temp, key=lambda x: x[1], reverse=False)
    return [pair[0] for pair in sorted_with_values]


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
        while xw[start - 1] != "#":
            start -= 1
        temp = start - 1
        while xw[temp + 1] != "#":
            temp += 1
            if xw[temp] == "-":
                xw = xw[:temp] + "*" + xw[temp + 1:]
        words_list = [i for i in range(start, temp + 1)]
        horizontal_words["h" + str(word_count)] = [words_list, len(words_list)]
        word_count += 1
    return horizontal_words


def find_vertical_words(puzzle, xw, transp_table):
    vertical_words = {}
    word_count = 0
    newH = len(xw) // (puzzle.width + 2)
    xw = puzzle.transpose(xw, len(xw) // newH)
    while "-" in xw:
        start = xw.index("-")
        while xw[start - 1] != "#":
            start -= 1
        temp = start - 1
        while xw[temp + 1] != "#":
            temp += 1
            if xw[temp] == "-":
                xw = xw[:temp] + "*" + xw[temp + 1:]
        words_list = [i for i in range(transp_table[start], transp_table[temp] + 1, puzzle.width + 2)]
        vertical_words["v" + str(word_count)] = [words_list, len(words_list)]
        word_count += 1
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
    for i in range(len(puzzle.board)):
        puzzle.board[i] = puzzle.board[i].upper()
    # ****************************************** MAIN: ABOVE = LAB 5, BELOW = LAB 6 ******************************************
    words_by_length, words = {}, set()
    regex_by_length = {}
    file = open(filename, 'r')
    frequency = {}
    # frequency = {letter: 0 for letter in string.ascii_uppercase}
    # frequency.update({"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0})
    for word in file:
        word = word.upper().strip().translate(str.maketrans('', '', string.punctuation))
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
        regex_by_length[i] = [re.compile(x) for x in words_by_length[i]]
    xw = ''.join(puzzle.board)
    xw = puzzle.add_border(xw)
    horiz = find_horizontal_words(puzzle, xw)
    vert = find_vertical_words(puzzle, xw, transposed_table(puzzle, xw))
    puzzle.board = puzzle.solve(horiz, vert, xw, words_by_length, regex_by_length)
    print("In main, result:")
    if puzzle.board is not None:
        puzzle.print_board_final(puzzle.board)
        # puzzle.print_board(puzzle.board)
    else:
        print("No solution found.")
    return puzzle.board


if __name__ == '__main__':
    main()
