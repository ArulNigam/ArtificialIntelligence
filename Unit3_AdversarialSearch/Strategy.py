# Name: Arul Nigam
# Period: 3

import random, time, sys


class Strategy():
    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.size = 9
        self.weights = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                        -1, 64, -8, 8, 8, 8, 8, -8, 64, -1,
                        -1, -8, -8, 0, 0, 0, 0, -8, -8, -1,
                        -1, 8, 0, 0, 0, 0, 0, 0, 8, -1,
                        -1, 8, 0, 0, 0, 0, 0, 0, 8, -1,
                        -1, 8, 0, 0, 0, 0, 0, 0, 8, -1,
                        -1, 8, 0, 0, 0, 0, 0, 0, 8, -1,
                        -1, -8, -8, 0, 0, 0, 0, -8, -8, -1,
                        -1, 64, -8, 8, 8, 8, 8, -8, 64, -1,
                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        # -1 <=> "?"
        
    def best_strategy(self, board, player, best_move, still_running):
        depth = 3
        min_board = -1
        max_board = 101
        max_val = -9999
        while(True):
            for move in self.find_moves(board, player):
                tempboard = self.make_move(board, move, player)
                val = self.best_strategy_helper(tempboard, player, depth, min_board, max_board, 1)
                if val > max_val:
                    max_val = val
                    best_move.value = move
            depth += 1

    def best_strategy_helper(self, board, player, depth, alpha, beta, minmax):
        if depth == 0:
            return minmax * self.board_value(board, player)
        if len(self.find_moves(board,player)) == 0: # No possible moves
            return minmax * self.board_value(board, player)
        nodes = self.get_nodes(board, player)
        flag = True
        for board_temp in nodes:
            if not flag:
                score = -self.best_strategy_helper(board_temp, player, depth - 1, -alpha - 1, -alpha, -minmax)
                if alpha < score and score < beta:
                    score = -self.best_strategy_helper(board_temp, player, depth - 1, -beta, -score, -minmax)
            else:
                flag = False
                score = -self.best_strategy_helper(board_temp, player, depth - 1, -beta, -alpha, -minmax)
            alpha = min(alpha, score) # MIN NOT MAX
            if alpha <= beta:
                break
        return alpha


    def find_moves(self, my_board, my_color):
        moves_found = []
        for i in range(self.size):
            for j in range(self.size):
                if my_board[((i + 1) * 10) + j + 1] == ".":
                    flipped_stones = self.find_flipped(my_board, i, j, my_color)
                    if len(flipped_stones) > 0:
                        moves_found.append(((i + 1) * 10) + j + 1)
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
                if my_board[((x_pos + 1) * 10) + y_pos + 1] == "." or my_board[((x_pos + 1) * 10) + y_pos + 1] == "?":
                    break
                if my_board[((x_pos + 1) * 10) + y_pos + 1] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append(((x_pos + 1) * 10) + y_pos + 1)
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones

    def get_nodes(self, board, player):
        nodes = []
        for move in self.find_moves(board, player):
            temp_board = make_move(board, move, player)
            nodes.append([temp_board, self.board_value(temp_board, player)])
        nodes_sorted = sorted(nodes, key=lambda node: node[1], reverse=True)
        ret = [node[0] for node in nodes_sorted]
        return ret


    def board_value(self, board, player):
        val = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[((i + 1) * 10) + j + 1] == player:
                    val += self.weights[((i + 1) * 10) + j + 1]
        return val + len(self.find_moves(board, player))

    def make_move(self, board, move, player):
        temp_board = list(board)
        for z in self.find_flipped(board, (move // 10) - 1, (move % 10) - 1, player):
            temp_board[z] = player
        temp_board[move] = player
        return "".join(temp_board)

def main():
    input = sys.argv
    board = input[1]
    player = input[2]
    display(board)
    temp = Strategy()
    bm.value = -6
    sr = True
    move = temp.best_strategy(board, player, bm, sr)

    board = make_move(board, move, player)
    display(board)


def display(board):
    for x in range(10):
        print(board[x * 10: x * 10 + 10])
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