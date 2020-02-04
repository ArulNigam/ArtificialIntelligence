# Name: Arul Nigam
# Period: 3

import random, time, sys

class Strategy():
    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.size = 9

    def best_strategy(self, board, player, best_move, still_running):
        if still_running:
            best_move.value = self.best_strategy_helper(board, player)

    def best_strategy_helper(self, board, color):
        # returns best move
        possible_moves = self.find_moves(board, color)
        if not possible_moves:
            return -1
        # best_move = possible_moves[random.choice(list(possible_moves.keys()))]
        random_move = random.choice(list(possible_moves.keys()))
        return random_move

    def find_moves(self, my_board, my_color):
        moves_found = {}
        for i in range(self.size):
            for j in range(self.size):
                if my_board[((i + 1) * 10) + j + 1] == ".":
                    flipped_stones = self.find_flipped(my_board, i, j, my_color)
                    if len(flipped_stones) > 0:
                        moves_found.update({((i + 1) * 10) + j + 1: flipped_stones})
        return moves_found

    def find_flipped(self, my_board, x, y, my_color):
        if my_board[((x + 1) * 10) + y + 1] != ".":
            return []
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.size and 0 <= y_pos < self.size:
                if my_board[((x_pos + 1) * 10) + y_pos + 1] == ".":
                    break
                if my_board[((x_pos + 1) * 10) + y_pos + 1] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append(((x_pos + 1) * 10) + y_pos + 1)
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones


def main():
    input = sys.argv
    board = input[1]
    player = input[2]
    display(board)
    temp = Strategy()
    move = temp.best_strategy_helper(board, player)
    board = make_move(board, move, player)
    display(board)


def display(board):
    for x in range(10):
        print(board[x * 10 : x * 10 + 10])
    print()


def make_move(board, move, player):
    temp = Strategy()
    temp_board = list(board)
    for z in temp.find_flipped(board, (move // 10) - 1, (move % 10) - 1, player):
        temp_board[z] = player
    temp_board[move] = player
    return "".join(temp_board)


if __name__ == '__main__':
    main()