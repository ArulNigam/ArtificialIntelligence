Due Dec 16, 2019, 11:00 PM
Lab2 Isolation
30 points
Nicole Kim Dec 9, 2019
Submit lastName_firstInitial_isolation_runner.py (if you modified the given code) and lastName_firstInitial_Lab2.py (change shell to this).

Complete RandomPlayer() and CustomPlayer().
isolation_runner.py
Text
Lab2_isolation_shell.py
Text
1 class comment
Daniel FuDec 17, 2019
Autocheck your algorithm against random: http://bit.ly/isogame
Your work
Turned in late
Nigam_A_isolation_runner.py
Text
Nigam_A_Lab2.py
Text
Private comments
Lab2 Isolation

# Name: Arul Nigam
# Date: 12/10/2019

import random, time

class RandomPlayer:
    def __init__(self):
        self.white = "#ffffff"
        self.black = "#000000"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move
        if self.first_turn:
            self.x_max, self.y_max = len(board), len(board[0])
        possible_moves = self.find_moves(board, color)
        if not possible_moves:
            return (-1, -1), 0
        best_move = random.choice(list(possible_moves))
        return best_move, 0

    def make_move(self, board, color, move):
        # returns board that has been updated
        return board

    def find_moves(self, board, color):
        # finds all possible moves
        moves_found = set()
        self.x_max, self.y_max = len(board), len(board[0])
        for i in range(len(board)):
            for j in range(len(board[i])):
                if self.first_turn and board[i][j] == ".":
                    moves_found.add((i, j))
                elif (color == self.black and board[i][j] == 'X') or (color == self.white and board[i][j] == 'O'):
                    for incr in self.directions:
                        x_pos = i + incr[0]
                        y_pos = j + incr[1]
                        stop = False
                        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                            if board[x_pos][y_pos] != ".":
                                stop = True
                            if not stop:
                                moves_found.add((x_pos, y_pos))
                            x_pos += incr[0]
                            y_pos += incr[1]
        self.first_turn = False
        return moves_found


class CustomPlayer:

    def __init__(self):
        self.white = "#ffffff"
        self.black = "#000000"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True
        self.best_moveB = None
        self.best_moveW = None
        self.best_move = None


    def best_strategy(self, board, color):
        search_depth = 4
        # returns best move
        if color == self.black:
            self.best_move = self.best_moveB
        else:
            self.best_move = self.best_moveW
        if self.first_turn:
            self.x_max, self.y_max = len(board), len(board[0])
        possible_moves = self.find_moves(board, color)
        if self.best_move is None:
            self.best_move = possible_moves.pop()
        if not possible_moves:
            return [-1, -1], 0
        self.best_move = self.minimax(board, color, search_depth,self.best_move)
        if color == self.black:
            self.best_moveB = self.best_move
        else:
            self.best_moveW = self.best_move
        return list(self.best_move), 0

    def minimax(self, board, color, search_depth, move):
        if color == self.black:
            v, s = self.max_value(board, color, search_depth, move)
        else:
            v, s = self.min_value(board, color, search_depth, move)
        return s

    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        pass

    def make_move(self, board, color, move):
        # returns board that has been updated
        return board

    def evaluate(self, board, color, move):
        # returns the utility value
        possible_moves = self.find_moves2(board, color, move)
        if possible_moves == None:
            if color == self.white:  # "O" can't move, "X" wins
                return 1000, (-1, -1)
            return -1000, (-1, -1)
        res = (len(possible_moves) - 2 * len(self.find_moves2(board, self.opposite_color, move)))
        return res, possible_moves.pop()

    def find_moves(self, board, color):
        # finds all possible moves
        moves_found = set()
        self.x_max, self.y_max = len(board), len(board[0])
        for i in range(len(board)):
            for j in range(len(board[i])):
                if self.first_turn and board[i][j] == ".":
                    moves_found.add((i, j))
                elif (color == self.black and board[i][j] == 'O') or (color == self.white and board[i][j] == 'X'):
                    for incr in self.directions:
                        x_pos = i + incr[0]
                        y_pos = j + incr[1]
                        stop = False
                        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                            if board[x_pos][y_pos] != ".":
                                stop = True
                            if not stop:
                                moves_found.add((x_pos, y_pos))
                            x_pos += incr[0]
                            y_pos += incr[1]
        self.first_turn = False
        return moves_found

    def find_moves2(self, board, color, move):
        # finds all possible moves
        moves_found = set()
        # Horizontal Left
        go = True
        for i in range((move[0] - 1), -1, -1):
            if go and board[i][move[1]] == ".":
                moves_found.add((i, move[1]))
            else:
                go = False
        # Horizontal Right
        go = True
        for i in range((move[0] + 1), len(board)):
            if go and board[i][move[1]] == ".":
                moves_found.add((i, move[1]))
            else:
                go = False
        # Vertical Up
        go = True
        i = move[1] - 1
        while go and i >= 0:
            if board[move[0]][i] == ".":
                moves_found.add((move[0], i))
                i = i - 1
            else:
                go = False

        # Vertical Down
        go = True
        for i in range((move[1] + 1), len(board[0])):
            if go and board[move[0]][i] == ".":
                moves_found.add((move[0], i))
            else:
                go = False
        # Diagonal down left
        i = move[0] - 1
        j = move[1] - 1
        go = True
        while go and i >= 0 and j >= 0:
            if board[i][j] == ".":
                moves_found.add((i, j))
                i = i - 1
                j = j - 1
            else:
                go = False

        # Diagonal Up Right
        i = move[0] + 1
        j = move[1] + 1
        go = True
        while go and i < len(board) and j < len(board[0]):
            if board[i][j] == ".":
                moves_found.add((i, j))
                i = i + 1
                j = j + 1
            else:
                go = False

        # Diagonal Down Right
        i = move[0] + 1
        j = move[1] - 1
        go = True
        while go and i < len(board) and j >= 0:
            if board[i][j] == ".":
                moves_found.add((i, j))
                i = i + 1
                j = j - 1
            else:
                go = False

        # Diagonal Up Left
        i = move[0] - 1
        j = move[1] + 1
        go = True
        while go and i >= 0 and j < len(board[0]):
            if board[i][j] == ".":
                moves_found.add((i, j))
                i = i - 1
                j = j + 1
            else:
                go = False

        return moves_found

    def terminal_test(self, board, color, search_depth):
        if search_depth == 0:
            return True
        full = True
        for i in board:
            if '.' in i:
                full = False
        if full:
            return True
        if self.find_moves(board, color) == None:
            return True
        return False

    def max_value(self, board, color, search_depth, move):
        if self.terminal_test(board, color, search_depth):
            res = self.evaluate(board, color, move)
            return res
        v = -9999
        res = (-1, -1)
        for s in self.find_moves2(board, color, move):
            newv = self.min_value(board, self.opposite_color[color], search_depth - 1, s)
            if not (isinstance(newv, int)):
                newv = newv[0]
            if v < newv:
                v = newv
                res = s
        return v, res

    def min_value(self, board, color, search_depth, move):
        if self.terminal_test(board, color, search_depth):
            res = self.evaluate(board, color, move)
            return res
        v = 9999
        res = (-1, -1)
        for s in self.find_moves2(board, color, move):
            newv = self.max_value(board, self.opposite_color[color], search_depth - 1, s)
            if not (isinstance(newv, int)):
                newv = newv[0]
            if v > newv:
                v = newv
                res = s
        return v, res
