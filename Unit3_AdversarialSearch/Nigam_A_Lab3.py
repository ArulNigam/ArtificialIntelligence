class Best_AI_bot:

   def __init__(self):
      self.white = "o"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
      # returns best move
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

   def make_key(self, board, color):
      # hashes the board
      return 1

   def stones_left(self, board):
      # returns number of stones that can still be placed
      return 1

   def make_move(self, board, color, move, flipped):
      # returns board that has been updated
      return 1

   def evaluate(self, board, color, possible_moves):
      # returns the utility value
      return 1

   def score(self, board, color):
      # returns the score of the board 
      return 1

   def find_moves(self, board, color):
      # finds all possible moves
      return 1

   def find_flipped(self, board, x, y, color):
      # finds which chips would be flipped given a move and color
      return 1
