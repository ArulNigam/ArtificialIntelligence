# Arul Nigam
# Period 3
# Crossword Pt. 1

import os, random, re, sys

BLOCKCHAR = '#'
OPENCHAR = "-"
PROTECTEDCHAR = "'~"


class Crossword():
    def init():  #####
        board = ""
        row_max
        col_max
        length = row_max * col_max

    def add_blocked_squares():

    def check_connectivity(board):
        
        start = board.index(OPENCHAR)
        if start < 0:
            start = board.index(PROTECTEDCHAR)
        flood_filled = connectivity_helper(start, board, [], [])

    def adjacents(space, explored):
        ret = []
        temp = [space + 1, space - 1, space + row_max, space - row_max]
        for i in temp:
            if i not in explored:
                ret.append(i)
        return ret

    def connectivity_helper(space, board, connected, explored):
        if (board[space] == OPENCHAR) or (board[space] == PROTECTEDCHAR):
            connected.append(space)
            for temp_space in adjacents(space):
                connected.append(connectivity_helper(temp_space, board, connected))
            return connected

    def index_to_coordinates(index):

    def check_legal(moved_board):
        return make_palindrome(moved_board)[1]

    def make_palindrome(temp_board):  # check if it properly captures middle
        board_list = list(temp_board):
        for i in range(len(board_list)):
            if board_list[i] != board_list[length - i]:
                if board_list[i] == PROTECTEDCHAR or board_list[length - i] == PROTECTEDCHAR:
                    if board_list[i] == OPENCHAR or board_list[length - i] == OPENCHAR:
                        board_list[i] = PROTECTEDCHAR
                        board_list[length - i] = PROTECTEDCHAR
                    if board_list[i] == BLOCKCHAR or board_list[length - i] == BLOCKCHAR:
                        return ["", False]  # THERE IS A BOARD CONFLICT
                else:
                    board_list[i] = BLOCKCHAR
                    board_list[length - i] = BLOCKCHAR
        return [''.join(board_list), True]

    def coordinates_to_index(row_num, col_num):
        return (row_num * col_max + col_num)

    def display(temp_board):
        clean_board = clean_protected(temp_board)
        for row in range(row_max):
            print(clean_board[(row * col_max):(row * col_max + col_max)])
            print()

    def clean_protected(temp_board):
        board_list = list(temp_board)
        for i in board_list:
            if board_list[i] == PROTECTEDCHAR:
                board_list[i] = OPENCHAR
        return ''.join(board_list)


####################################################################################

def main():
    input = sys.argv
    temp = Crossword()
    display(board)


if __name__ == '__main__':
    main()
