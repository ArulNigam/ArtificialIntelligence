# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, random, re, sys, time

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "~"


def print_board(board, width):
    row = []
    for i in range(width, len(board) - width):
        row.append(board[i])
        if (i + 1) % width == 0:
            print("".join(row)[1: width - 1])
            row = []
    print()


class Crossword():
    def __init__(self, height, width):
        self.row_max = height
        self.col_max = width
        self.length = self.row_max * self.col_max
        self.board = [OPENCHAR] * (height * width)

    def transpose(self, xw, current_width):
        return "".join([xw[col::current_width] for col in range(current_width)])

    def set_initial(self, initial, blocked_square_count):
        for i in range(len(initial)):
            self.board[initial[i][0]] = initial[i][1]
        print("Initial input")
        print_board(self.board, self.col_max)
        xword = "".join(self.board)
        xw = BLOCKCHAR * (self.col_max + 3)
        xw += (BLOCKCHAR * 2).join(xword[p:p + self.col_max] for p in range(0, len(xword), self.col_max))
        xw += BLOCKCHAR * (self.col_max + 3)
        print("Added border")
        print_board(xw, self.col_max + 2)
        letters = xw
        xw = self.add_protected_char(xw, self.col_max + 2)

        print("added protected")
        print_board(xw, self.col_max + 2)

        # Try until number of blocked spaces = target

        xw = self.add_blocked_char(xw, self.col_max + 2)
        num_blocked = xw.count("#")
        board_len = len(self.board)

        for position in range(len(self.board)):
            self.board = list(xw)
            if blocked_square_count % 2 == 1:
                self.board[int(len(self.board) / 2)] = "#"

            # position = random.randint(self.col_max+4, board_len - self.col_max - 4)
            if (num_blocked < blocked_square_count) & (position != int(len(self.board) / 2)):
                if self.board[position] == "-":

                    temp_board = self.board
                    temp_board[position] = "#"
                    temp_xw = "".join(temp_board)
                    temp_xw = self.make_palindrome(temp_xw)
                    temp_xw = "".join(list(temp_xw[0]))
                    # temp_xw = self.add_blocked_char(temp_xw, self.col_max + 2)
                    if self.is_legal(temp_xw):
                        print("2", position)
                        self.board[position] = "#"
                        xw = temp_xw
                        self.board = list(xw)
                        num_blocked = xw.count("#")

        print("added blocked spaces")
        print_board(xw, self.col_max + 2)

        letters = list(letters)
        for i in range(len(self.board)):
            if letters[i].isalpha():
                self.board[i] = letters[i]
            if self.board[i] == PROTECTEDCHAR:
                self.board[i] = OPENCHAR
        xw = "".join(self.board)
        print_board(xw, self.col_max + 2)
        self.board = list(xw)

    def is_legal(self, xw):
        if xw.find("#-#") >= 0:
            print("not legal 1", xw)
            return False
        if xw.find("#--#") >= 0:
            print("not legal 2")
            return False
        if xw.find("#~-#") >= 0:
            print("not legal 3")
            return False
        if xw.find("#-~#") >= 0:
            print("not legal 4")
            return False
        if xw.find("#~#") >= 0:
            print("not legal 5")
            return False
        if xw.find("#~~#") >= 0:
            print("not legal 6", xw)
            return False
        xw = self.transpose(xw, self.col_max + 2)
        if xw.find("#-#") >= 0:
            print("not legal 7")
            return False
        if xw.find("#--#") >= 0:
            print("not legal 8")
            return False
        if xw.find("#~-#") >= 0:
            print("not legal 9", xw)
            return False
        if xw.find("#-~#") >= 0:
            print("not legal 10")
            return False
        if xw.find("#~#") >= 0:
            print("not legal 11")
            return False
        if xw.find("#~~#") >= 0:
            print("not legal 12")
            return False
        return True

    def add_protected_char(self, board, width):

        tempboard = list(board)
        for i in range(len(tempboard)):
            if "".join(tempboard[i]).isalpha():
                tempboard[i] = PROTECTEDCHAR
        board = self.make_palindrome(tempboard)
        board = "".join(list(board[0]))

        originalboard = board
        fixboard = True
        while fixboard:
            board = board.replace("#~-", "#~~")
            board = board.replace("-~#", "~~#")
            board = board.replace("#~~-", "#~~~")
            board = board.replace("#-~-", "#-~~")
            board = board.replace("-~~#", "~~~#")
            board = board.replace("-~-#", "~~-#")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))

            fixboard = not (originalboard == board)
            originalboard = board

        return board

    def add_blocked_char(self, board, width):

        originalboard = board
        fixboard = True
        while fixboard:
            board = board.replace("#-#", "###")
            board = board.replace("#--#", "####")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))
            board = self.transpose(board, self.col_max + 2)
            board = board.replace("#-#", "###")
            board = board.replace("#--#", "####")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))
            board = self.transpose(board, self.row_max + 2)

            fixboard = not (originalboard == board)
            originalboard = board

        return board

    def check_connectivity(self, board):
        start = board.index(OPENCHAR)
        if start < 0:
            start = board.index(PROTECTEDCHAR)
        flood_filled = self.connectivity_helper(start, board, [], [])
        return len(flood_filled) == (board.count(OPENCHAR) + board.count(PROTECTEDCHAR))

    def adjacents(self, space, explored):
        ret = []
        temp = [space + 1, space - 1, space + self.row_max, space - self.row_max]
        for i in temp:
            if i not in explored:
                ret.append(i)
        return ret

    def connectivity_helper(self, space, board, connected, explored):
        if (board[space] == OPENCHAR) or (board[space] == PROTECTEDCHAR):
            connected.append(space)
            for temp_space in self.adjacents(space, explored):
                connected.append(self.connectivity_helper(temp_space, board, connected, explored))
            return connected

    def index_to_coordinates(self, index):
        return [index / self.row_max, index % self.col_max]

    def check_legal(self, moved_board):
        return self.make_palindrome(moved_board)[1]

    def make_palindrome(self, temp_board):  # check if it properly captures middle
        works = True
        board = list(temp_board)
        board_length = len(board)
        for i in range(board_length):
            i_mirror = board_length - i - 1
            if board[i] == BLOCKCHAR:
                if board[i_mirror] == PROTECTEDCHAR:
                    works = False
                else:
                    board[i_mirror] = board[i]
            if board[i] == PROTECTEDCHAR:
                if board[i_mirror] == BLOCKCHAR:
                    works = False
                else:
                    board[i_mirror] = board[i]
        return [board, works]

    def coordinates_to_index(self, row_num, col_num):
        return row_num * self.col_max + col_num

    def display(self, temp_board):
        clean_board = self.clean_protected(temp_board)
        for row in range(self.row_max):
            print(clean_board[(row * self.col_max):(row * self.col_max + self.col_max)])
            print()

    def clean_protected(self, temp_board):
        board_list = list(temp_board)
        for i in board_list:
            if board_list[i] == PROTECTEDCHAR:
                board_list[i] = OPENCHAR
        return ''.join(board_list)


def connected_words(xw):
    connections = {}
    h_start, h_end, v_start, v_end = -1, -1, -1, -1
    for i in range(len(xw)):
        if xw[i] == "-":
            temp = []
            next_wall = xw.find("##", i)
            # HORIZONTAL:
            x = i + 1
            while x < next_wall:
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x += 1
                else:
                    break
            x = i
            while x > (next_wall - (row_max + 2)):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x -= 1
                else:
                    break
            if len(temp) > 0:
                h_start, h_end = min(temp), max(temp)
            temp = []
            # VERTICAL:
            x = i + (row_max + 2)
            while x < (col_max + 2):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x += (row_max + 2)
                else:
                    break
            x = i - (row_max + 2)
            while x > (row_max + 2):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x -= (row_max + 2)
                else:
                    break
            if len(temp) > 0:
                v_start, v_end = min(temp), max(temp)
            connections[i] = [h_start, h_end, v_start, v_end]
    return connections


def fill(guess, start, xw, is_vertical):
    guess = guess[0]
    xw = list(xw)
    if is_vertical:
        for i in range(len(guess)):
            xw[start + i * (row_max + 2)] = guess[i]
    else:  # horizontal
        for i in range(len(guess)):
            xw[start + i] = guess[i]
    return ''.join(xw)


def find_longest_word(xw):
    rgx = r'#-+#'
    horizontal_match = re.search(rgx, xw)
    if horizontal_match:
        group = horizontal_match.group()
        horizontal_start = xw.index(group) + 1
        horizontal_length = len(group) - 2
    else:
        horizontal_start = -1
        horizontal_length = -1
    xw = transpose(xw, col_max + 2)
    vertical_match = re.search(rgx, xw)
    if vertical_match:
        group = vertical_match.group()
        vertical_start = len(xw) - (xw.index(group) + 1)  ##################### TRANSPOSE THIS NUM
        vertical_length = len(group) - 2
    else:
        vertical_start = -1
        vertical_length = -1
    if horizontal_length > vertical_length:
        return horizontal_start, False, horizontal_length
    return vertical_start, True, vertical_length


def is_valid(new, old, start, connections, words):
    for i in range(len(old)):
        if new[i] != old[i]:  # there is a modification
            if old[i] != OPENCHAR:  # invalid modification
                return False
    temp = connections[start]
    if new[temp[0]:temp[1]] not in words:
        return False
    if new[temp[2]:temp[3]:(row_max + 2)] not in words:
        return False
    return True


def solve(xw, words_by_length, connections, words):
    return solve_helper(xw, words_by_length, connections, words)


def solve_helper(xw, words_by_length, connections, words):
    if xw.find(OPENCHAR) < 0:
        return xw
    start, is_vertical, length = find_longest_word(xw)
    for guess in words_by_length[length]:
        filled = fill(guess, start, xw, is_vertical)
        if is_valid(filled, xw, start, connections, words):
            print_board(filled, col_max + 4)
            return solve_helper(filled, words_by_length)


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


def main():
    intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V|h|v)(\d+)x(\d+)(.+)$"]
    user_input = sys.argv
    for i in range(len(user_input)):
        print(i, user_input[i])
    initial_words_list = []
    initial_values = []
    for i in range(1, len(user_input)):
        if re.match(intTest[0], user_input[i]):  # board size
            result = re.search("^(\d+)x(\d+)$", user_input[i])
            height = int(result.group(1))
            width = int(result.group(2))
        elif os.path.isfile(user_input[i]):  # filename scrabble
            filename = user_input[i]
        elif re.match(intTest[1], user_input[i]):  # number of blocked squares
            blocked_square_count = int(user_input[i])
        elif re.match(intTest[2], user_input[i]):  # coordinate + word
            is_vertical = ("V" == user_input[i][0]) | ("v" == user_input[i][0])
            result = re.search("^(H|V)(\d+)x(\d+)(.+)$", user_input[i], re.IGNORECASE)
            start_index = [int(result.group(2)), int(result.group(3))]
            word = result.group(4)
            if is_vertical:
                for j in range(len(word)):
                    board_pos = (start_index[0] + j) * width + start_index[1]
                    initial_values.append([board_pos, word[j]])
            else:
                for j in range(len(word)):
                    board_pos = (start_index[0]) * width + start_index[1] + j
                    initial_values.append([board_pos, word[j]])
    print("size, block count [", height, "x", width, "] ", blocked_square_count)
    puzzle = Crossword(height, width)
    puzzle.set_initial(initial_values, (blocked_square_count + (width + height + 2) * 2))
    frequency, words_by_length, words = {}, {}, set()
    file = open(filename, 'r')
    for word in file:
        word = word.upper().strip()
        words.add(word)
        for i in range(len(word)):
            if word[i] in frequency:
                frequency[word[i]] += 1
            else:
                frequency[word[i]] = 1
        length = len(word)
        if length in words_by_length:
            words_by_length[length].append(word)
        else:
            words_by_length[length] = [word]
    for i in words_by_length:
        words_by_length[i] = sort_by_richness(words_by_length[i], frequency)
    print_board(solve(xw, words_by_length, connected_words(xw), words), col_max + 4)
    # return solve(xw, words_by_length, connected_words(xw), words)


if __name__ == '__main__':
    main()