# Name: Arul Nigam
# Period: 3

def fill(guess, start, xw, is_vertical):
    xw = list(xw)
    if is_vertical:
        for i in range(len(guess)):
            xw[start + i * (self.row_max + 2)] = guess[i]
    else: # horizontal
        for i in range(len(guess)):
            xw[start + i] = guess[i]
    return ''.join(xw)

def find_longest_word(xw):
    vertical_start = - 1
    vertical_length = -1
    horizontal_start = - 1
    horizontal_length = -1
    if horizontal_length > vertical_length:
        return horizontal_start, False, horizontal_length
    return vertical_start, True, vertical_length

def is_valid(new, old):
    for i in range(len(old)):
        if new[i] != old[i]: # there is a modification
            if old[i] != BLOCKCHAR: # invalid modification
                return False
    return True

def solve(xw):
    return solve_helper(xw)

def solve_helper(xw):
    if xw.find(OPENCHAR) < 0:
        return xw
    start, is_vertical, length = find_longest_word(xw)
    for guess in words_by_length[length]:
        filled = fill(guess, start, xw, is_vertical)
        if is_valid(filled, xw):
            solve_helper(filled)

def sort_by_richness(words):
    temp = []
    for w in words:
        temp.append([w, word_richness(w)])
    return sorted(temp, key = lambda x: x[1])

def word_richness(word):
    richness = 0
    for i in len(word):
        richness += frequency[i]
    return richness

def main():
##############################################################################
    filename =
    xw = "###########-----####-----####--#--####-----####-----###########"
##############################################################################
    frequency, words_by_length = {}, {}
    file = open(filename, “r”)
    for word in file:
        for i in len(word):
            if i in frequency:
                frequency[i] += 1
            else:
                frequency[i] = 1
        length = len(word)
        if length in words_by_length:
            words_by_length[length].append(word)
        else:
            words_by_length = [word]
    for i in words_by_length.keys():
        words_by_length[i] = sort_by_richness(words_by_length[i])
    return solve(xw)

if __name__ == '__main__':
    main()