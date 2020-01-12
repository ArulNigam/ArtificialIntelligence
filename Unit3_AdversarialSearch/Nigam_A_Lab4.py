# Name: Arul Nigam
# Date: 01/07/2020

import sys, math

def main():
    #board = sys.argv[0] # REVISE ##################################################################################
    board = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
    turn = "@"
    global size
    size = int(math.sqrt(len(board))) - 2
    print(pos())
    #display(board)
    ask()
    #play(board, turn)

def pos(index):
    return index // size, index % size

def display(board):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = ""
    for x in range(size):
        header += alphabet[x] + " "
    print("   ", header)
    for i in range(size):
        this_row = ""
        for x in range(size):
            this_row += board[x + i * size] + " "
        print(i + 1, " ", this_row)

def ask():
    #figures out whose turn, etc.
    return 1

def play(board, turn):
    opposite_turn = "O"
    if turn == "O":
        opposite_turn = "@"
    moves = possible_moves(board)
    move = get_move(moves, board, turn)
    board[move[0] * size + move[1]] = turn     # turn is a symbol
    display(board)
    winner = whose_win(board)
    if winner == None:
        play(board, opposite_turn)
    else:
        print(winner, "wins!")

def possible_moves(board):
    # return list of tuples w/ (x, y) where you can move
    return []

def get_move(moves, board, turn): # AI
    return 1

def whose_win(board):
    return None

if __name__ == '__main__':
    main()