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
        self.board = [OPENCHAR] * (self.height * self.width)
        self.length = len(self.board)

    def addblock(self, xw, blocked_goal, level=0):
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
        elif blocked_goal == ((self.width+2)*(self.height+2)):
            return BLOCKCHAR*((self.width+2)*(self.height+2))

        pick_from = []
        for i in range(len(xw)):
            if (xw[i] != BLOCKCHAR) and (xw[i] != PROTECTEDCHAR):
                pick_from.append(i)
        if len(xw)//2 in pick_from:
            pick_from.remove(len(xw)//2)


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

            if (re.search("[#](.?[~]|[~].?)[#]", xw) is None) and (re.search("[#](.?[~]|[~].?)[#]", self.transpose(xw, len(xw) // newH)) is None):

                if xw.count(BLOCKCHAR) <= blocked_goal:
                    ret = ""
                    if xw.count("#--#") == 0 and xw.count("#-#") == 0:
                        ret = self.addblock(xw, blocked_goal, level+1)
                    elif xw.count(BLOCKCHAR) <= blocked_goal-6:
                        xw = xw.replace("#---", "####", 1)
                        xw = xw.replace("---#","####", 1)
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
        xw = self.area_fill(xw,start)
        ret = xw.count(OPENCHAR) == 0
        print("check connectivity=", ret)
        return True
        return xw.count(OPENCHAR) == len(self.connectivity_helper(start, xw, set(), set()))

    def is_valid(self, xw):

        xw = xw.replace(PROTECTEDCHAR, OPENCHAR)
        if xw.count("#--#") > 0 or xw.count("#-#") > 0:
            return False
        temp = self.transpose(xw, self.width+2)
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

    def set_initial(self, initial_values, blocked_goal):
        xw = self.board
        xw = list(xw)
        for i in initial_values:
            xw[i[0]] = i[1]
        xw = ''.join(xw)
        xw = self.add_border(xw)
        xw = self.add_protected(xw)

        xw = self.addblock(xw, blocked_goal+((self.width+self.height+2)*2))

        xw = list(xw)
        for i in initial_values:
            xw[((i[0]//self.width)+1)*(self.width+2)+(1+i[0]%self.width)] = i[1]
        xw = ''.join(xw)
        xw = xw.replace(PROTECTEDCHAR, OPENCHAR)
        print("added letters back + openchar")
        self.print_board(xw)

        xw = xw[(self.width + 2):(len(xw) - (self.width + 2))]
        ret = ""
        for i in range(self.height):
            ret += xw[(1 + i * (self.width + 2)):(self.width + 1 + i * (self.width + 2))]
        self.print_board(ret, 0)
        self.board = list(ret)

    def transpose(self, xw, width):
        height = len(xw)//(width)
        temp = [0]*len(xw)
        xw = list(xw)
        for i in range(len(xw)):
            x = i // (width)
            y = i % (width)
            temp[int((y * height) + x)] = xw[i]

        return ''.join(temp)


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
                    board_pos = (start_index[0] + j) * width + start_index[1]
                    initial_values.append([board_pos, word[j]])
            else:
                for j in range(len(word)):
                    board_pos = width + 2 + (start_index[1] + j) + (start_index[0] + 1) * (width + 2)
                    board_pos = (start_index[0] * width) + start_index[1] + j
                    initial_values.append([board_pos, word[j]])

    print("size, block count [", height, "x", width, "] ", blocked_square_count)
    puzzle = Crossword(height, width)
    puzzle.set_initial(initial_values, blocked_square_count)


if __name__ == '__main__':
    main()