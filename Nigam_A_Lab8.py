# Name: Arul Nigam Date: 10/02/2019

import heapq
import random, time, math

class PriorityQueue():
    def __init__(self):
        self.current = None
        self.queue = []
        current = 0  # to make this object iterable

    # To make this object iterable: have __iter__ function and assign next function for __next__
    def next(self):
        if self.current >= len(self.queue):
            raise StopIteration
        out = self.queue[self.current]
        self.current += 1
        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 0

    ''' complete the following functions '''

    def remove(self, index):
        rem = self.queue[index]
        del self.queue[index]
        return rem

    def pop(self):
        # swap first and last. Remove last. Heap down from first.
        self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
        rem = self.queue[-1]
        del self.queue[-1]
        first = 0
        last = len(self.queue) - 1
        while last >= (first * 2 + 1):
            lchild = min((first * 2 + 1), last)
            rchild = min((first * 2 + 2), last)
            child = lchild
            if self.queue[lchild] > self.queue[rchild]:
                child = rchild
            if self.queue[first] > self.queue[child]:
                self.queue[first], self.queue[child] = self.queue[child], self.queue[first]
                first = child
            else:
                first = last
        # return the removed value
        return rem

    def push(self, value):
        # append at last. Heap up.
        self.queue.append(value)
        last = len(self.queue) - 1
        while last > 0:
            next_last = int((last - 1) / 2)
            if self.queue[last] < self.queue[next_last]:
                self.queue[last], self.queue[next_last] = self.queue[next_last], self.queue[last]
            last = next_last
        pass

    def peek(self):
        return self.queue[0]

def inversion_count(new_state, width, N=4):
    '''
    Depends on the size(width, N) of the puzzle,
    we can decide if the puzzle is solvable or not by counting inversions.
    If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
    If N is even, puzzle instance is solvable if
       the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is even.
       the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is odd.
    '''
    inversions = 0
    stateList = list(new_state)
    for i in range(width * N):
        j = i + 1
        while j < width * N:
            if stateList[i] > stateList[j]:  # an inversion occurs
                if stateList[i] != "_":
                    inversions += 1
            j += 1
    if N % 2 != 0:  # odd puzzle
        if inversions % 2 == 0:  # even number of inversions
            return True  # solvable
    else:  # even puzzle
        if (int(stateList.index("_") / N) % 2 == 0 and inversions % 2 == 0) or (
                int(stateList.index("_") / N) % 2 != 0 and inversions % 2 != 0):
            return True
    return False

def check_inversion():
    t1 = inversion_count("_42135678", 3, 3)  # N=3
    f1 = inversion_count("21345678_", 3, 3)
    t2 = inversion_count("4123C98BDA765_EF", 4)  # N is default, N=4
    f2 = inversion_count("4123C98BDA765_FE", 4)
    return t1 and t2 and not (f1 or f2)

def getInitialState(sample, size):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    while not inversion_count(new_state, size, size):
        random.shuffle(sample_list)
        new_state = ''.join(sample_list)
    return new_state

def swap(n, i, j):
    temp = list(n)
    temp[i], temp[j] = temp[j], temp[i]
    return ''.join(temp)

def generateChild(node, size):
    ret = set()
    i = node.index("_")
    if (i - size + 1) % size != 0:  # can be swapped with right
        ret.add(swap(node, i, i + 1))  # swap right
    if i not in range(size * size - size, size * size):  # can be swapped with below
        ret.add(swap(node, i, i + size))  # swap down
    if i not in range(size):  # can be swapped with above
        ret.add(swap(node, i - size, i))  # swap up
    if i % size != 0:  # can be swapped with left
        ret.add(swap(node, i - 1, i))  # swap left
    return ret  # return whatever children were added...there should be at least 2 on a 3x3 board

def display_path(path_list, size):
    for n in range(size):
        for i in range(len(path_list)):
            print(path_list[i][n * size:(n + 1) * size], end=" " * size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""

''' You can make multiple heuristic functions '''

def dist_heuristic(start, goal, size):
    distance = 0
    for i in start:
        current = start.find(i)
        target = goal.find(i)
        distance += (abs(target // size - current // size) + abs(target % size - current % size))
    return distance

def check_heuristic():
    a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
    b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
    return (a < b)

def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size=4):
    minreslen = 0
    if start == goal:
        return [start]
    if inversion_count(start, size):
        frontierF = PriorityQueue()
        frontierB = PriorityQueue()
        frontierF.push((0, start, [start]))
        frontierB.push((0, goal, [goal]))
        exploredF = {}
        exploredB = {}
        pathsF = {}
        pathsB = {}
        exploredF[start] = dist_heuristic(start, goal, size)
        exploredB[goal] = dist_heuristic(goal, start, size)
        while not (frontierF.isEmpty() or frontierB.isEmpty()):
            poppedF = frontierF.pop()
            poppedB = frontierB.pop()
            currentF = poppedF[2] # path
            currentB = poppedB[2] # path
            if poppedF[1] == goal: # current value
                return currentF
            if poppedB[1] == start: # current value
                return currentB                
            childrenF = generateChild(poppedF[1], size) - set(currentF)
            childrenB = generateChild(poppedB[1], size) - set(currentB)
            for child in childrenF:  # for each of the children of the current node...
                new_cost = len(currentF) + 1 + heuristic(child, goal, size)
                if child in exploredB:
                    res = currentF + pathsB[child][::-1]
                    reslen = len(res)
                    if (minreslen == 0) or (minreslen > reslen):
                        minreslen = reslen
                        minres = res
                if (minreslen > 0):
                    return minres
                if child not in exploredF or new_cost < exploredF[child]:
                    exploredF[child] = new_cost
                    frontierF.push((new_cost, child, currentF + [child]))
                    pathsF[child] = currentF + [child]
            for child in childrenB:  # for each of the children of the current node...
                new_cost = len(currentB) + 1 + heuristic(child, start, size)
                if child in exploredF:
                    res = pathsF[child] + currentB[::-1]
                    reslen = len(res)
                    if (minreslen==0) or (minreslen>reslen):
                        minreslen=reslen
                        minres = res
                if (minreslen>0):
                    return minres
                if child not in exploredB or new_cost < exploredB[child]:
                    exploredB[child] = new_cost
                    frontierB.push((new_cost, child, currentB + [child]))
                    pathsB[child] = currentB + [child]
    return None

def main():
    # A star
   print ("Inversion works?:", check_inversion())
   print ("Heuristic works?:", check_heuristic())
   #initial_state = getInitialState("_123456789ABCDEF", 4)
   initial_state = input("Type initial state: ")
   cur_time = time.time()
   path = (a_star(initial_state))
   if path != None: 
      display_path(path, 4)
      for p in range(1, len(path)):
         if path[p] not in generateChild(path[p-1], 4):
            print ("path is not working at {}".format(p))
   else: print ("No Path Found.")
   print ("Duration: ", (time.time() - cur_time))
      
if __name__ == '__main__':
    main()

''' Sample output 1

Inversion works?: True
Initial State: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0


Sample output 2

Inversion works?: True
Initial State: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005014657974243164

Sample output 3

Inversion works?: True
Type initial state: 8936C_24A71FDB5E
8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 37
Duration:  0.27825474739074707


Sample output 4

Inversion works?: True
Type initial state: 8293AC4671FEDB5_
8293    8293    8293    8293    8293    8293    8293    8293    82_3    8_23    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
AC46    AC46    AC46    AC46    AC46    _C46    C_46    C4_6    C496    C496    C_96    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
71FE    71F_    71_F    7_1F    _71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5_    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 39
Duration:  0.7709157466888428

'''