# Name: Arul Nigam
# Period: 3

# This is the correct shell code for Word Ladder BFS

import pickle

''' Node class or helper methods '''

# you can modify this method or not using it
def generate_path(current, explored):
   list = [current]
   count = 0
   while explored[current] != "s":       #assume the parent of root is "s"
      list.append(explored[current])
      current = explored[current]
      count += 1
   print("The shortest path is: ", list[::-1])
   print("The number of steps is: ", count + 1)
   return ""

def solve(start, end, word_dict):
    if len(start) != 6 or len(end) != 6 or not start.isalpha() or not end.isalpha() or start not in word_dict or end not in word_dict:
      print("Please only enter words for start and end that are 1) English 2) alphabetic 3) six letters long.")
      quit()
    explored, frontier = {}, [start, "s"]
    while frontier: # while frontier is not empty
        state = frontier.pop(0) # state is the first element
        parent = frontier.pop(0) # parent is the second element
        if state not in explored: # if this is a new (unexplored) state on the frontier
            explored[state] = parent # add a new key:value pair (child:parent)...similar to a listNode (value + pointer)
            children = word_dict[state] # capture the list of children
            for child in children: # for each of the children of the current node...
                frontier.append(child) # ...add the child to the frontier...
                frontier.append(state) # and follow the child with the parent (state)
        if state == end: # if you've reached the goal_state:
            return generate_path(state, explored) # display the path
    return ("No solution") # if you expanded everything and never reached the goal_state, then there is no solution

def main():
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   word_dict = {}
   with open("Nigam_A_Lab3.pkl", "rb") as infile:
      word_dict = pickle.load(infile)
   print (solve(initial, goal, word_dict))

if __name__ == '__main__':
   main()