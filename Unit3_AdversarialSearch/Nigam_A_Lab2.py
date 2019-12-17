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

   def best_strategy(self, board, color):
      search_depth = 3
      # returns best move
      if self.first_turn:
         self.x_max, self.y_max = len(board), len(board[0])
      possible_moves = self.find_moves(board, color)
      if not possible_moves:
         return (-1, -1)
      best_move = self.minimax(board, color, search_depth)
      return best_move

   def minimax(self, board, color, search_depth):
      if color == self.black:
         v, s = self.max_value(board, color, search_depth)
      else:
         v, s = self.min_value(board, color, search_depth)
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

   def evaluate(self, board, color):
      # returns the utility value
      possible_moves = self.find_moves(board, color)
      if possible_moves == None:
         if color == self.white: #"O" can't move, "X" wins
            return 1, (-1,-1)
         return -1, (-1,-1)
      return 0, possible_moves.pop()

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

   def max_value(self, board, color, search_depth):
      if self.terminal_test(board, color, search_depth):
         res = self.evaluate(board, color)
         return res
      v = -9999
      res = (-1, -1)
      for s in self.find_moves(board, color):
         newv = self.min_value(board, self.opposite_color[color], search_depth-1)
         if not (isinstance(newv, int)):
            newv = newv[0]
         if v < newv:
            v = newv
            res = s
      return v, res

   def min_value(self, board, color, search_depth):
      if self.terminal_test(board, color, search_depth):
         res = self.evaluate(board, color)
         return res
      v = 9999
      res = (-1, -1)
      for s in self.find_moves(board, color):
         newv = self.max_value(board, self.opposite_color[color], search_depth-1)
         if not (isinstance(newv, int)):
            newv = newv[0]
         if v > newv:
            v = newv
            res = s
      return v, res
