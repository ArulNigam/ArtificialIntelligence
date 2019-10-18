# Name: Arul Nigam Date: 09/26/2019

import heapq
import random, time, math

class PriorityQueue():
    def __init__(self):
        self.queue = []
        current = 0  # to make this object iterable

    # To make this object iterable: have __iter__ function and assign next function for __next__
    def next(self):
        if self.current >= len(self.queue):
            self.current
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
        while (last >= (first*2+1)):
            lchild = min((first * 2 + 1), last)
            rchild = min((first * 2 + 2), last)
            child = lchild
            if (self.queue[lchild]>self.queue[rchild]):
                child = rchild
            if (self.queue[first] > self.queue[child]):
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
        while (last > 0):
            if (self.queue[last] < self.queue[int((last - 1) / 2)]):
                self.queue[last], self.queue[int((last - 1) / 2)] = self.queue[int((last - 1) / 2)], self.queue[last]
            last = int((last - 1) / 2)
        pass

    def peek(self):
        return self.queue[0]

def inversion_count(new_state, size):
   ''' Depends on the size(width, N) of the puzzle, 
   we can decide if the puzzle is solvable or not by counting inversions.
   If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
   If N is even, puzzle instance is solvable if
      the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is even.
      the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is odd.
   ''' 
   inversions = 0
   stateList = list(new_state)
   for i in range(size * size):
      j = i + 1
      while j < size * size:
         if stateList[i] > stateList[j]: # an inversion occurs
            if stateList[i] != "_":
               inversions += 1  
         j += 1
   if size % 2 != 0: # odd puzzle
      if inversions % 2 == 0: # even number of inversions
         return True # solvable
   else: # even puzzle
      if (int(stateList.index("_") / size) % 2 == 0 and inversions % 2 == 0) or (int(stateList.index("_") / size) % 2 != 0 and inversions % 2 != 0):
         return True   
   return False
   
def check_inversion():
   t1 = inversion_count("_42135678", 3)
   f1 = inversion_count("21345678_", 3)
   return t1 and not f1

def getInitialState(sample):
   sample_list = list(sample)
   random.shuffle(sample_list)
   new_state = ''.join(sample_list)
   if(inversion_count(new_state, 3)): return new_state
   else: return None
   
def swap(n, i, j):
   temp = list(n)
   temp[i], temp[j] = temp[j], temp[i]
   return ''.join(temp)
         
def generate_children(n, size):
   ret = set()
   i = n.index("_")
   if (i - size + 1) % size != 0: # can be swapped with right
      ret.add(swap(n, i, i + 1)) # swap right
   if i not in range(size * size - size, size * size): # can be swapped with below
      ret.add(swap(n, i, i + size)) # swap down
   if i not in range(size): # can be swapped with above
      ret.add(swap(n, i - size, i)) # swap up
   if i % size != 0: # can be swapped with left
      ret.add(swap(n, i - 1, i)) # swap left
   return ret # return whatever children were added...there should be at least 2 on a 3x3 board   

def display_path(path_list, size):
   for n in range(size):
      for i in range(len(path_list)):
         print (path_list[i][n*size:(n+1)*size], end = " "*size)
      print ()
   print ("\nThe shortest path length is :", len(path_list))
   return ""

def dist_heuristic(start, goal, size):
    distance = 0
    for i in start:
        current = start.find(i)
        target = goal.find(i)
        distance += (abs(target // size - current // size) + abs(target % size - current % size))
    return distance   

def a_star(start, goal="_12345678", heuristic=dist_heuristic):
    size = int(math.sqrt(len(goal)))
    if start == goal:
        return [start]
    if inversion_count(start, size):
        frontier = PriorityQueue()
        frontier.push((0, start, [start]))
        explored = {}
        dist_by_node = {}
        explored[start] = dist_heuristic(start, goal, size)
        while not frontier.isEmpty():
            popped = frontier.pop()
            current = popped[2] # path
            if popped[1] == goal: # current value
                return current
            children = generate_children(popped[1], size) - set(current)
            for child in children:  # for each of the children of the current node...
                new_cost = len(current) + 1 + heuristic(child, goal, size)
                if child not in explored or new_cost < explored[child]:
                    explored[child] = new_cost
                    frontier.push((new_cost,child, current + [child]))
    return None
    
def main():
    # A star
   print ("Inversion works?:", check_inversion())
#    initial_state = getInitialState("_12345678")
#    while initial_state == None:
#       initial_state = getInitialState("_12345678")
   initial_state = input("Type initial state: ")
   cur_time = time.time()
   path = (a_star(initial_state))
   if path != None: display_path(path, 3)
   else: print ("No Path Found.")
   print ("Duration: ", (time.time() - cur_time))

if __name__ == '__main__':
   main()

''' Sample output 1:

Inversion works?: True
Type initial state: 76423_581
764   764   764   764   764   _64   6_4   64_   641   641   641   641   641   _41   4_1   431   431   431   431   _31   3_1   31_   312   312   312   _12   
23_   231   231   2_1   _21   721   721   721   72_   7_2   732   732   _32   632   632   6_2   652   652   _52   452   452   452   45_   4_5   _45   345   
581   58_   5_8   538   538   538   538   538   538   538   5_8   _58   758   758   758   758   7_8   _78   678   678   678   678   678   678   678   678   

The shortest path length is : 26
Duration:  0.06485509872436523


Sample output 2:

Inversion works?: True
Type initial state: 84765231_
847   847   847   847   _47   4_7   47_   472   472   472   472   472   472   472   472   472   472   472   472   472   472   4_2   _42   142   142   142   142   1_2   _12   
652   652   6_2   _62   862   862   862   86_   861   861   8_1   _81   381   381   3_1   31_   315   315   315   _15   1_5   175   175   _75   375   375   3_5   345   345   
31_   3_1   351   351   351   351   351   351   35_   3_5   365   365   _65   6_5   685   685   68_   6_8   _68   368   368   368   368   368   _68   6_8   678   678   678   

The shortest path length is : 29
Duration:  0.28726887702941895

'''
