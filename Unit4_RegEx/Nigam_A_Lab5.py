# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, random, re, sys

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "'~"

class Crossword():
    def __init__(self):
        self.board = ""
        self.row_max = 1 ##########################
        self.col_max = 1 ##########################
        self.length = self.row_max * self.col_max

#    def add_blocked_squares():

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
            for temp_space in self.adjacents(space):
                connected.append(self.connectivity_helper(temp_space, board, connected))
            return connected

    def index_to_coordinates(index):
        return [index / self.row_max, index % self.col_max]

    def check_legal(self, moved_board):
        return self.make_palindrome(moved_board)[1]

    def make_palindrome(self, temp_board):  # check if it properly captures middle
        board_list = list(temp_board):
        for i in range(len(board_list)):
            if board_list[i] != board_list[self.length - i]:
                if board_list[i] == PROTECTEDCHAR or board_list[self.length - i] == PROTECTEDCHAR:
                    if board_list[i] == OPENCHAR or board_list[self.length - i] == OPENCHAR:
                        board_list[i] = PROTECTEDCHAR
                        board_list[self.length - i] = PROTECTEDCHAR
                    if board_list[i] == BLOCKCHAR or board_list[self.length - i] == BLOCKCHAR:
                        return ["", False]  # THERE IS A BOARD CONFLICT
                else:
                    board_list[i] = BLOCKCHAR
                    board_list[self.length - i] = BLOCKCHAR
        return [''.join(board_list), True]

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

####################################################################################

def main():
    intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
    inp = sys.argv
    filename = input[0]
    inititial_words_list = []
    for i in range(1, len(input)):
        if re.match(intTest[0], input[i]): # board size
            height = input[i][:input[i].index("x") + 1]
            width = input[i][input[i].index("x") + 1:]
        else if re.match(intTest[1], input[i]): # number of blocked squares
            blocked_square_count = int(input[i])
        else if: # filename scrablle
        else if re.match(intTest[2], input[i]):  # coordinate + word
            is_vertical = ("v" == input[i][0])
            start_index = [input[i][1], input[i][3]]
            word = input[i][4:]
            ###########################################add tuple to inititial words, dont use input



    #input = sys.argv
    #temp = Crossword()
    #display(board)

if __name__ == '__main__':
    main()