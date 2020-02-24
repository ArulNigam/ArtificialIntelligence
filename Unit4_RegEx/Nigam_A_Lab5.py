# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, re, sys, time

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
        xw = self.add_blocked_char(xw, self.col_max + 2)
        num_blocked = xw.count("#")
        board_len = len(self.board)
        for position in range(len(self.board)):
            self.board = list(xw)
            if blocked_square_count % 2 == 1:
                self.board[int(len(self.board)/2)] = "#"
            #position = random.randint(self.col_max+4, board_len - self.col_max - 4)
            if (num_blocked < blocked_square_count) & (position != int(len(self.board)/2)):
                if self.board[position] == "-":
                    temp_board = self.board
                    temp_board[position] = "#"
                    temp_xw = "".join(temp_board)
                    temp_xw = self.make_palindrome(temp_xw)
                    temp_xw = "".join(list(temp_xw[0]))
                    #temp_xw = self.add_blocked_char(temp_xw, self.col_max + 2)
                    if self.is_legal(temp_xw):
                        print("wgwgwgewegwegwegwegegwgewgewegwg")
                  #      print("2", position)
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
        print("FINAL:", self.check_connectivity(xw))
        print_board(xw, self.col_max + 2)
        self.board = list(xw)

    def is_legal(self, xw):
        if xw.find("#-#") >= 0:
            #print("not legal 1", xw)
            return False
        if xw.find("#--#") >= 0:
            #print("not legal 2")
            return False
        if xw.find("#~-#") >= 0:
            #print("not legal 3")
            return False
        if xw.find("#-~#") >= 0:
            #print("not legal 4")
            return False
        if xw.find("#~#") >= 0:
            #print("not legal 5")
            return False
        if xw.find("#~~#") >= 0:
            #print("not legal 6", xw)
            return False
        xw = self.transpose(xw, self.col_max+2)
        if xw.find("#-#") >= 0:
            #print("not legal 7")
            return False
        if xw.find("#--#") >= 0:
            #print("not legal 8")
            return False
        if xw.find("#~-#") >= 0:
            #print("not legal 9", xw)
            return False
        if xw.find("#-~#") >= 0:
            #print("not legal 10")
            return False
        if xw.find("#~#") >= 0:
            #print("not legal 11")
            return False
        if xw.find("#~~#") >= 0:
            #print("not legal 12")
            return False
        return True
        #return self.check_connectivity(xw)

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
        while fixboard:
            board = board.replace("#-#", "###")
            board = board.replace("#--#", "####")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))
            board = self.transpose(board,self.col_max+2)
            board = board.replace("#-#", "###")
            board = board.replace("#--#", "####")
            board = self.make_palindrome(board)
            board = "".join(list(board[0]))
            board = self.transpose(board, self.row_max+2)
            fixboard = not (originalboard == board)
            originalboard = board
        return board

    '''def add_helper(board, num_of_blocks, curr_num_of_blocks):
        if num_of_blocks == curr_num_of_blocks:  # DONE!
            return board, num_of_blocks
        if TBD
            board = board[0:pos] + BLOCKCHAR + board[pos+1:]
            new_board = update_the_board_TBD
            if not_legal(new_board):
                board = board[0:pos] + OPENCHAR + board[pos+1:]
            else:
                board = new_board
        return add_helper(board, num_of_blocks, curr_num_of_blocks)'''

    def check_connectivity(self, board):
        start = board.index(OPENCHAR)
        if start < 0:
            start = board.index(PROTECTEDCHAR)
        if start < 0:
            return True
        print("connectivity", start, board[start])
        print_board(board, self.col_max + 2)
        flood_filled = self.connectivity_helper(start, board, [], [])[0]
        return len(flood_filled) == (board.count(OPENCHAR) + board.count(PROTECTEDCHAR))

    def adjacents(self, space, explored):
        ret = []
        temp = [space + 1, space - 1, space + self.row_max+2, space - self.row_max+2]
        for i in temp:
            if i not in explored:
                ret.append(i)
#        print(temp, explored, ret)
        return ret

    def connectivity_helper(self, space, board, connected, explored):
        explored.append(space)
        if (board[space] == OPENCHAR) or (board[space] == PROTECTEDCHAR):
            connected.append(space)
            for temp_space in self.adjacents(space, explored):
                temp_search = self.connectivity_helper(temp_space, board, connected, explored)
                if temp_search is not None:
                    connected.append(temp_search[0])
                    explored.append(temp_search[1])
        return [connected, explored]

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
    print("size, block count [", height,"x", width, "] ", blocked_square_count)
    puzzle = Crossword(height, width)
    puzzle.set_initial(initial_values, (blocked_square_count+(width+height+2)*2))


if __name__ == '__main__':
    main()
