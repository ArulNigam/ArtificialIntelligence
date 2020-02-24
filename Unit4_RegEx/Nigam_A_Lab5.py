# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, re, sys, time, random

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
    time.sleep(.33)


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

        xword = "".join(self.board)
        xw = BLOCKCHAR * (self.col_max + 3)
        xw += (BLOCKCHAR * 2).join(xword[p:p + self.col_max] for p in range(0, len(xword), self.col_max))
        xw += BLOCKCHAR * (self.col_max + 3)
        print("Initial board w. border")
        print_board(xw, self.col_max + 2)
        letters = xw
        xw = self.add_protected_char(xw, self.col_max + 2)
        print("added protected")
        print_board(xw, self.col_max + 2)
        # Try until number of blocked spaces = target
        if self.row_max * self.col_max == blocked_square_count:
            xw = BLOCKCHAR * len(xw)
        elif blocked_square_count % 2 == 1:
            xw = xw[0:((len(xw) // 2))] + BLOCKCHAR + xw[((len(xw) // 2) + 1):]
        blocked_square_count = blocked_square_count + (self.col_max + self.row_max + 2) * 2
        illegalRegex = "[{}](.?[{}] | [{}].?)[{}]".format(BLOCKCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)
        if re.search(illegalRegex, xw): return xword, len(xword)
        substituteRegex = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
        subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
        newH = len(xw) // (self.col_max + 2)
        for counter in range(2):
            xw = re.sub(substituteRegex, BLOCKCHAR * 2, xw)
            xw = re.sub(subRE2, BLOCKCHAR * 3, xw)
            xw = self.transpose(xw, len(xw) // newH)
            newH = len(xw) // newH
        xw = self.add_blocked_char(xw, self.col_max + 2)
        print("Updated Board to work")
        print_board(xw, self.col_max + 2)
        '''num_blocked = xw.count(BLOCKCHAR)
        board_len = len(self.board)
        for position in range(len(self.board)):
            self.board = list(xw)
            #position = random.randint(self.col_max+4, board_len - self.col_max - 4)
            if (num_blocked < blocked_square_count) & (position != (len(self.board)//2)):
                if self.board[position] == "-":
                    temp_board = self.board
                    temp_board[position] = "#"
                    temp_xw = "".join(temp_board)
                    temp_xw = self.make_palindrome(temp_xw)
                    temp_xw = "".join(list(temp_xw[0]))
                    #temp_xw = self.add_blocked_char(temp_xw, self.col_max + 2)
                    if self.is_legal(temp_xw):
                  #      print("2", position)
                        self.board[position] = "#"
                        xw = temp_xw
                        self.board = list(xw)
                        num_blocked = xw.count("#")'''
        badpositions = {-1}
        pos_list = [x for x in range(len(xw)) if xw[x] == OPENCHAR and xw[len(xw) - x - 1] == OPENCHAR]

        for i in range(len(xw)):
            if xw[i] == PROTECTEDCHAR:
                badpositions.add(i)
            elif xw[i] == BLOCKCHAR:
                badpositions.add(i)
        xw = self.add_helper(xw, blocked_square_count, xw.count(BLOCKCHAR), badpositions, pos_list)[0]
        print("added blocked spaces", xw.count(BLOCKCHAR), blocked_square_count)
        print_board(xw, self.col_max + 2)
        self.board = list(xw)
        letters = list(letters)
        for i in range(len(letters)):
            if letters[i].isalpha():
                self.board[i] = letters[i]
            if self.board[i] == PROTECTEDCHAR:
                self.board[i] = OPENCHAR
        xw = "".join(self.board)
        print("FINAL:", self.check_connectivity(xw,1))
        print_board(xw, self.col_max + 2)
        self.board = list(xw)

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
            board = board.replace("#-~-", "#~~~")
            board = board.replace("-~~#", "~~~#")
            board = board.replace("-~-#", "~~~#")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))
            fixboard = not (originalboard == board)
            originalboard = board
        return board

    def add_blocked_char(self, board, width):
        originalboard = board
        fixboard = True

        # while fixboard:
        for i in range(len(board)):
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

    def add_helper(self, board, num_of_blocks, curr_num_of_blocks, badpositions, poslist):
        if num_of_blocks == curr_num_of_blocks:  # DONE!
            return board, num_of_blocks
        pick = random.randint(0, len(poslist) - 1)
        position = poslist[pick]
        poslist = poslist[0:pick] + poslist[pick + 1:]
        board = board[0:position] + BLOCKCHAR + board[position + 1:]
        xw = board
        illegalRegex = "[#](.?[~]|[~].?)[#]"
        if re.search(illegalRegex, xw): return xw, len(xw)
        substituteRegex = "[#]-(?=[#])"
        subRE2 = "[#]--(?=[#])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
        newH = len(xw) // (self.col_max + 2)
        for counter in range(2):
            xw = re.sub(substituteRegex, BLOCKCHAR * 2, xw)
            xw = re.sub(subRE2, BLOCKCHAR * 3, xw)
            xw = self.transpose(xw, len(xw) // newH)
            newH = len(xw) // newH
        xw = self.add_blocked_char(xw, self.col_max + 2)
        # print("Updated Board (new) to work")
        # print_board(xw, self.col_max + 2)
        if not self.is_legal_board(xw):
            print("backtracting from", position)
            board = board[0:position] + OPENCHAR + board[position + 1:]
            board = self.add_helper(board, num_of_blocks, curr_num_of_blocks, badpositions, poslist)[0]
        else:
            board = xw

        curr_num_of_blocks = board.count(BLOCKCHAR)
        return self.add_helper(board, num_of_blocks, curr_num_of_blocks, badpositions, poslist)

    def is_legal_board(self, xw):
        if xw.find("#~#") >= 0:
            # print("not legal 1", xw)
            return False
        '''if xw.find("#--#") >= 0:
            #print("not legal 2")
            return False'''
        if xw.find("#~-#") >= 0:
            # print("not legal 3")
            return False
        if xw.find("#-~#") >= 0:
            # print("not legal 4")
            return False
        if xw.find("#~#") >= 0:
            # print("not legal 5")
            return False
        if xw.find("#~~#") >= 0:
            # print("not legal 6", xw)
            return False
        xw = self.transpose(xw, self.col_max + 2)
        '''if xw.find("#-#") >= 0:
            #print("not legal 7")
            return False
        if xw.find("#--#") >= 0:
            #print("not legal 8")
            return False'''
        if xw.find("#~-#") >= 0:
            # print("not legal 9", xw)
            return False
        if xw.find("#-~#") >= 0:
            # print("not legal 10")
            return False
        if xw.find("#~#") >= 0:
            # print("not legal 11")
            return False
        if xw.find("#~~#") >= 0:
            # print("not legal 12")
            return False
        # return True
        return self.check_connectivity(xw)

    def area_fill(self, board, sp):
        dirs = [-1, self.col_max + 2, 1, -1 * (self.col_max + 2)]
        if sp < 0 or sp >= len(board):
            return board
        if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
            board = board[0:sp] + '?' + board[sp + 1:]
            for d in dirs:
                if d == -1 & sp % (self.col_max + 2) == 0:
                    continue
                if d == 1 & (sp + 1) % (self.col_max + 2) == 0:
                    continue
                board = self.area_fill(board, sp + d)
        return board

    def check_connectivity(self, board, flag=0):
        try:
            start = board.index(OPENCHAR)
        except ValueError:
            try:
                start = board.index(PROTECTEDCHAR)
            except ValueError:
                return True
        if flag == 1:
            print_board(self.area_fill(board, start),self.col_max)
        return self.area_fill(board, start).count("?") == (board.count(OPENCHAR) + board.count(PROTECTEDCHAR))

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
            elif board[i] == PROTECTEDCHAR:
                if board[i_mirror] == BLOCKCHAR:
                    works = False
                else:
                    board[i_mirror] = board[i]
        if not works:
            print("****Make Palindrome failed****")
        return [board, works]

    def clean_protected(self, temp_board):
        board_list = list(temp_board)
        for i in board_list:
            if board_list[i] == PROTECTEDCHAR:
                board_list[i] = OPENCHAR
        return ''.join(board_list)


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
            is_vertical = ("V" == user_input[i][0]) or ("v" == user_input[i][0])
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
    puzzle.set_initial(initial_values, blocked_square_count)


if __name__ == '__main__':
    main()
