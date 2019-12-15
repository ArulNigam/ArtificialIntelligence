# Name: Arul Nigam
# Date: 12/10/2019

import random

class RandomPlayer:
   def __init__(self):
      self.white = "O"
      self.black = "X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True
      
   def best_strategy(self, board, color):
      # returns best move
      possible_moves = self.find_moves(self, board, color)
      if not possible_moves:
         return (-1, -1), 0
      move = random.choice(list(possible_moves))
      best_move = (move // self.y_max, move % self.y_max)
      return best_move, 0
      
   def make_move(self, board, color, move):
      # returns board that has been updated
      return board
      
   def find_moves(self, board, color):
      # finds all possible moves
      moves_found = set()
      self.x_max, self.y_max = len(board), len(board[0])
      for i in range(len(board)):
         for j in range(len(board[0])):
            if self.first_turn and board[i][j] == ".":
               moves_found.add(i + self.y_max + j)
               self.first_turn = False
            elif (color == self.black and board[i][j] == "X") or (color == self.white and board[i][j] == "O"):
               for incr in self.directions:
                  x_pos = i + incr[0]
                  y_pos = j + incr[1]
                  stop = False
                  while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                     if board[x_pos][y_pos] != ".":
                        stop = True
                     if not stop:
                        moves_found.add(x_pos * self.y_max + y_pos)
                     x_pos += incr[0]
                     y_pos += incr[1]
      return moves_found

class CustomPlayer:
   def __init__(self):
      self.white = "O"
      self.black = "X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True

   def best_strategy(self, board, color):
      # returns best move
      possible_moves = self.find_moves(self, board, color)
      if not possible_moves:
         return (-1, -1), 0
      move = random.choice(list(possible_moves))
      best_move = (move // self.y_max, move % self.y_max)
      return best_move, 0

   def minimax(self, board, color, search_depth):
      # returns best "value"
      return 1

   def negamax(self, board, color, search_depth):
      # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
      # returns best "value" while also pruning
      pass

   def make_move(self, board, color, move):
      # returns board that has been updated
      return board

   def evaluate(self, board, color, possible_moves):
      # returns the utility value
      return 1

   def find_moves(self, board, color):
      # finds all possible moves
      return set()
