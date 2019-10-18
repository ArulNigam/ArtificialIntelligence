# Name: Arul Nigam
# Period: 3

import pickle

''' helper methods goes here '''

def generate_path(current, explored):
    list = [current]
    count = 0
    while explored[current] != "":  # assume the parent of root is ""
        list.append(explored[current])
        current = explored[current]
        count += 1
    return (list[::-1], count + 1)

def recur(start, end, word_dict, explored, limit):
    if start == end:
        return generate_path(end, explored)  # display the path
    elif limit == 0:
        return None
    children = word_dict[start]  # capture the list of children
    for child in children:  # for each of the children of the current node...
        if child not in explored:  # if this is a new (unexplored) state on the frontier
            explored[child] = start
            result = recur(child, end, word_dict, {key: explored[key] for key in explored}, limit - 1)
            if (result != None):
               return result
    return None

def solve(start, end, word_dict, limit):
    if len(start) != 6 or len(end) != 6 or not start.isalpha() or not end.isalpha() or start not in word_dict or end not in word_dict:
      print("Please only enter words for start and end that are 1) English 2) alphabetic 3) six letters long.")
      quit()
    explored = {start: ""}
    result = recur(start, end, word_dict, explored, limit)
    if result != None:
        if (result[0][-1] == end):
            return result
    return None

def main():
   limit = int(input("Type the limit (1 - 20): "))
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   word_dict = {}
   # You need to change the pickle file name
   with open("Nigam_A_Lab3.pkl", "rb") as infile:
      word_dict = pickle.load(infile)
   path_and_steps = (solve(initial, goal, word_dict, limit))
   if path_and_steps != None:
      print ("Path:", path_and_steps[0])
      print ("steps within {} limit:".format(limit), path_and_steps[1])
   else:
      print ("Solution not found in {} steps".format(limit))

   # Now, start iterative deepening
   for depth in range(1, 20 + 1):
      path_and_steps = (solve(initial, goal, word_dict, depth))
      if path_and_steps != None:
         break

   # Print out the shortest path and length of the path (number of steps)
   if path_and_steps != None:
      print("Shortest Path:", path_and_steps[0])
      print("Steps:", path_and_steps[1])
   else:
      print("Solution not found in {} steps".format(limit))

if __name__ == '__main__':
    main()
