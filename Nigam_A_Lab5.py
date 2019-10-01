# Name: Arul Nigam Date: 09/17/2019

import math, random, time

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

def check_pq():
    ''' check_pq is checking if your PriorityQueue
   is completed or not'''
    pq = PriorityQueue()
    temp_list = []
    for i in range(10):
        a = random.randint(0, 10000)
        pq.push(a)
        temp_list.append(a)
    temp_list.sort()
    for i in temp_list:
        j = pq.pop()
        if not i == j:
            return False
    return True
    
def generate_adjacents(current, words_set): 
   ''' words_set is a set which has all words.
   By comparing current and words in the words_set,
   generate adjacents set of current and return it'''
   adj_set = set()
   alphabet = set(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"])
   for i in range(6):
      currentChanged = list(current)
      for newLetter in alphabet:
         if current[i] != newLetter:
            currentChanged[i] = newLetter
            if ''.join(currentChanged) in words_set:
               adj_set.add(''.join(currentChanged))
   return adj_set
                
def check_adj(words_set):
    adj = generate_adjacents('listen', words_set)
    target = {'listee', 'listel', 'litten', 'lister', 'listed'}
    return (adj == target)

def dist_heuristic(current, goal):
    ''' current and goal are words to compare. Calculate the heuristic function
   and then return a numeric value'''
    # TODO 3: heuristic
    return sum(current[i] != goal[i] for i in range(6))

def a_star(word_list, start, goal, heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
   Update the cost and path if you find the lower-cost path in your process.
   You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
   '''
    frontier = PriorityQueue()
    if start == goal: return [start]
    # TODO 4: A* Search
    # Your code goes here
    frontier.push((0, start))
    explored = {}
    dist_by_node = {}
    explored[start] = None
    dist_by_node[start] = 0
    while not frontier.isEmpty():
        current = frontier.pop()[1]
        if current == goal:
            break
        children = generate_adjacents(current, word_list)
        for child in children:  # for each of the children of the current node...
            total_dist = dist_by_node[current] + dist_heuristic(current, child)
            if child not in dist_by_node or total_dist < dist_by_node[child]:
                dist_by_node[child] = total_dist
                priority = total_dist + dist_heuristic(goal, child)
                frontier.push((priority, child))
                explored[child] = current
    list = [current]
    while explored[current] != start:
            list.append(explored[current])
            current = explored[current]
    list.append(start)
    return list[::-1]

def main():
    q = PriorityQueue()
    print("PriorityQueue() works:", check_pq())
    words_set = set()
    file = open("words_6_longer.txt", "r")
    for word in file.readlines():
        words_set.add(word.rstrip('\n'))
    print("Check generate_adjacents():", check_adj(words_set))
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path_and_steps = (a_star(words_set, initial, goal))
    if path_and_steps != None:
        print(path_and_steps)
        print("steps: ", len(path_and_steps))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")

if __name__ == '__main__':
    main()

'''Sample output 1
PriorityQueue() works: True
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
steps:  7
Duration: 0.000997304916381836

Sample output 2
PriorityQueue() works: True
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
steps:  13
Duration: 0.0408782958984375

Sample output 3
PriorityQueue() works: True
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'paunch', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'ranged', 'ragged', 'raggee', 'raggle', 'gaggle', 'giggle']
steps:  19
Duration:  0.0867915153503418
'''