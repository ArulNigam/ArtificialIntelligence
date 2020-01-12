# Name: Arul Nigam
import random

class RandomBot():

   def __init__(self):
      self.white = "O"
      self.black = "@"
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
            return [-1, -1], 0
        #best_move = possible_moves[random.choice(list(possible_moves.keys()))]
        random_move = random.choice(list(possible_moves.keys()))
        return [random_move // self.y_max, random_move % self.y_max], 0

   def find_moves(self, my_board, my_color):
      moves_found = {}
      for i in range(len(my_board)):
         for j in range(len(my_board[i])):
            if my_board[i][j] == ".":
               flipped_stones = self.find_flipped(my_board, i, j, my_color)
               if len(flipped_stones) > 0:
                  moves_found.update({i * self.y_max + j: flipped_stones})
      return moves_found

   def find_flipped(self, my_board, x, y, my_color):
      if my_board[x][y] != ".":
         return []
      if my_color == self.black:
         my_color = "@"
      else:
         my_color = "O"
      flipped_stones = []
      for incr in self.directions:
         temp_flip = []
         x_pos = x + incr[0]
         y_pos = y + incr[1]
         while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if my_board[x_pos][y_pos] == ".":
               break
            if my_board[x_pos][y_pos] == my_color:
               flipped_stones += temp_flip
               break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones

class Minimax_AI_bot():

   def __init__(self):
      self.white = "O"
      self.black = "@"
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
            return [-1, -1], 0
         #best_move = possible_moves[random.choice(list(possible_moves.keys()))]
         #random_move = random.choice(list(possible_moves.keys()))
         #return [random_move // self.y_max, random_move % self.y_max], 0
         return self.evaluate(board, color, possible_moves)

   def make_move(self, board, color, x, y):
      if color == "#ffffff":
        color_symbol = "O"
      else:
         color_symbol = "@"
      board[x][y] = color_symbol

   def evaluate(self, board, color, possible_moves):
      start_val = self.score(board, color) + 1
      max_value = -999
      best_move = None
      for move in list(possible_moves.keys()):
         value = start_val + len(self.find_flipped(board, move // self.y_max, move % self.y_max, color))
         if value > max_value:
            max_value = value
            best_move = move
      return [best_move // self.y_max, best_move % self.y_max], max_value

   def score(self, board, color):
      score1 = 0 # @
      score2 = 0 # O
      for i in range(len(board)):
         for j in range(len(board[i])):
            if board[i][j] == "@":
               score1 += 1
            if board[i][j] == "O":
               score2 += 1
      if color == self.white:
         return score2 - score1
      return score1 - score2

   def find_moves(self, my_board, my_color):
      moves_found = {}
      for i in range(len(my_board)):
         for j in range(len(my_board[i])):
            if my_board[i][j] == ".":
               flipped_stones = self.find_flipped(my_board, i, j, my_color)
               if len(flipped_stones) > 0:
                  moves_found.update({i * self.y_max + j: flipped_stones})
      return moves_found

   def find_flipped(self, my_board, x, y, my_color):
      if my_board[x][y] != ".":
         return []
      if my_color == self.black:
         my_color = "@"
      else:
         my_color = "O"
      flipped_stones = []
      for incr in self.directions:
         temp_flip = []
         x_pos = x + incr[0]
         y_pos = y + incr[1]
         while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if my_board[x_pos][y_pos] == ".":
               break
            if my_board[x_pos][y_pos] == my_color:
               flipped_stones += temp_flip
               break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones

class Alpha_beta_AI_bot():
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

class Best_AI_bot():
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None