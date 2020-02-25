# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, re, sys, time, random

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "~"


class Crossword():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.length = self.height * self.width
        self.board = [OPENCHAR] * (self.height * self.width)
        self.length = len(self.board)

    def add_blocks(self, xw, blocked_goal):
        blocked_goal += (len(xw) - self.length)
        blocked_so_far = xw.count(BLOCKCHAR)
        if blocked_so_far == blocked_goal:
            return xw
        xw = list(xw)
        if blocked_goal % 2 != 0:
            xw[(len(xw) - 1) / 2] = BLOCKCHAR
            blocked_so_far += 1
        while blocked_so_far < blocked_goal:
            space = random.randint(self.width + 2, len(xw) - 1)
            if xw[space] == OPENCHAR and self.is_valid(space, xw):
                xw[space] = BLOCKCHAR
                xw = list(self.make_palindrome(xw))
                blocked_so_far += 2
        return ''.join(xw)


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
        return self.make_palindrome(xw)

    def check_connectivity(self, xw):
        start = xw.find(OPENCHAR)
        return xw.count(OPENCHAR) == len(self.connectivity_helper(start, xw, set(), set()))

    def connectivity_helper(self, start, xw, connected, explored):
        explored.add(start)
        if xw[start] == OPENCHAR:
            connected.add(start)
            to_explore = []
            if start - 1 not in explored:
                to_explore.append(start - 1)
            if start + 1 not in explored:
                to_explore.append(start + 1)
            if start - (self.width + 2) not in explored:
                to_explore.append(start - (self.width + 2))
            if start + (self.width + 2) not in explored:
                to_explore.append(start + (self.width + 2))
            if len(to_explore) > 0:
                for i in to_explore:
                    temp_ret = self.connectivity_helper(i, xw, connected, explored)
                    print("connected: ", connected, "explored: ", explored)
                    connected.update(temp_ret)
            print(connected, "dsdssdds")
            return connected


    def is_valid(self, space, xw):
        xw = list(xw)
        xw[space] = BLOCKCHAR
        xw = ''.join(xw)
        xw.replace(PROTECTEDCHAR, OPENCHAR)
        invalids = xw.count("#--#") + xw.count("#-#")
        if invalids > 0:
            return False
        temp = self.transpose(xw)
        invalids = temp.count("#--#") + temp.count("#-#")
        if invalids > 0:
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

    def print_board(self, board):
        for i in range(self.height + 2):
            print(board[((self.width + 2) * i):((self.width + 2) * (i + 1))])

    def set_initial(self, initial_values, blocked_goal):
        xw = self.board
        xw = self.add_border(xw)
        xw = list(xw)
        for i in initial_values:
            xw[i[0]] = i[1]
        xw = ''.join(xw)
        xw = self.add_protected(xw)
        xw = self.add_blocks(xw, blocked_goal)
        self.print_board(xw)

    def transpose(self, xw):
        return "".join([xw[col::self.width + 2] for col in range(self.width + 2)])


def main():
    intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V|h|v)(\d+)x(\d+)(.+)$"]
    user_input = sys.argv
    for i in range(len(user_input)):
        print(i, user_input[i])
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
            is_vertical = ("V" == user_input[i][0]) or ("v" == user_input[i][0])
            result = re.search("^(H|V)(\d+)x(\d+)(.+)$", user_input[i], re.IGNORECASE)
            start_index = [int(result.group(2)), int(result.group(3))]
            word = result.group(4)
            if is_vertical:
                for j in range(len(word)):
                    board_pos = width + 2 + (start_index[1] + 1) + (start_index[0] + j) * (width + 2)
                    initial_values.append([board_pos, word[j]])
            else:
                for j in range(len(word)):
                    board_pos = width + 2 + (start_index[1] + j) + (start_index[0] + 1) * (width + 2)
                    initial_values.append([board_pos, word[j]])

    print("size, block count [", height, "x", width, "] ", blocked_square_count)
    puzzle = Crossword(height, width)
    puzzle.set_initial(initial_values, blocked_square_count)


if __name__ == '__main__':
    main()
