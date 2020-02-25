# Name: Arul Nigam
# Period: 3

########################################################################
import re

BLOCKCHAR = '#'
OPENCHAR = "-"
row_max = 5
col_max = 5


def transpose(xw, current_width):
    return "".join([xw[col::current_width] for col in range(current_width)])


def print_board(board, width):
    row = []
    for i in range(width, len(board) - width):
        row.append(board[i])
        if (i + 1) % width == 0:
            print("".join(row)[1: width - 1])
            row = []
    print()


########################################################################

def connected_words(xw):
    connections = {}
    h_start, h_end, v_start, v_end = -1, -1, -1, -1
    for i in range(len(xw)):
        if xw[i] == "-":
            temp = []
            next_wall = xw.find("##", i)
            # HORIZONTAL:
            x = i + 1
            while x < next_wall:
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x += 1
                else:
                    break
            x = i
            while x > (next_wall - (row_max + 2)):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x -= 1
                else:
                    break
            if len(temp) > 0:
                h_start, h_end = min(temp), max(temp)
            temp = []
            # VERTICAL:
            x = i + (row_max + 2)
            while x < (col_max + 2):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x += (row_max + 2)
                else:
                    break
            x = i - (row_max + 2)
            while x > (row_max + 2):
                if xw[x] == OPENCHAR:
                    temp.append(x)
                    x -= (row_max + 2)
                else:
                    break
            if len(temp) > 0:
                v_start, v_end = min(temp), max(temp)
            connections[i] = [h_start, h_end, v_start, v_end]
    return connections


def fill(guess, start, xw, is_vertical):
    guess = guess[0]
    xw = list(xw)
    if is_vertical:
        for i in range(len(guess)):
            xw[start + i * (row_max + 2)] = guess[i]
    else:  # horizontal
        for i in range(len(guess)):
            xw[start + i] = guess[i]
    return ''.join(xw)


def find_longest_word(xw):
    rgx = r'#-+#'
    horizontal_match = re.search(rgx, xw)
    if horizontal_match:
        group = horizontal_match.group()
        horizontal_start = xw.index(group) + 1
        horizontal_length = len(group) - 2
    else:
        horizontal_start = -1
        horizontal_length = -1
    xw = transpose(xw, col_max + 2)
    vertical_match = re.search(rgx, xw)
    if vertical_match:
        group = vertical_match.group()
        vertical_start = len(xw) - (xw.index(group) + 1)  ##################### TRANSPOSE THIS NUM
        vertical_length = len(group) - 2
    else:
        vertical_start = -1
        vertical_length = -1
    if horizontal_length > vertical_length:
        return horizontal_start, False, horizontal_length
    return vertical_start, True, vertical_length


def is_valid(new, old, start, connections, words):
    for i in range(len(old)):
        if new[i] != old[i]:  # there is a modification
            if old[i] != OPENCHAR:  # invalid modification
                return False
    temp = connections[start]
    if new[temp[0]:temp[1]] not in words:
        return False
    if new[temp[2]:temp[3]:(row_max + 2)] not in words:
        return False
    return True


def solve(xw, words_by_length, connections, words):
    return solve_helper(xw, words_by_length, connections, words)


def solve_helper(xw, words_by_length, connections, words):
    if xw.find(OPENCHAR) < 0:
        return xw
    start, is_vertical, length = find_longest_word(xw)
    for guess in words_by_length[length]:
        filled = fill(guess, start, xw, is_vertical)
        if is_valid(filled, xw, start, connections, words):
            print_board(filled, col_max + 4)
            return solve_helper(filled, words_by_length)


def sort_by_richness(words, frequency):
    temp = []
    for w in words:
        temp.append([w, word_richness(w, frequency)])
    return sorted(temp, key=lambda x: x[1], reverse=True)


def word_richness(word, frequency):
    richness = 0
    for i in range(len(word)):
        richness += frequency[word[i]]
    return richness


def main():
    ##############################################################################
    filename = "dct20k.txt"
    xw = "#-----####-----####-------##---#---##-------##-------##-------#"
    ##############################################################################
    frequency, words_by_length, words = {}, {}, set()
    file = open(filename, 'r')
    for word in file:
        word = word.upper().strip()
        words.add(word)
        for i in range(len(word)):
            if word[i] in frequency:
                frequency[word[i]] += 1
            else:
                frequency[word[i]] = 1
        length = len(word)
        if length in words_by_length:
            words_by_length[length].append(word)
        else:
            words_by_length[length] = [word]
    for i in words_by_length:
        words_by_length[i] = sort_by_richness(words_by_length[i], frequency)
    print_board(solve(xw, words_by_length, connected_words(xw), words), col_max + 4)
    # return solve(xw, words_by_length, connected_words(xw), words)


if __name__ == '__main__':
    main()
