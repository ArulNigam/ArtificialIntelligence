# Name: Arul Nigam
# Period: 3

from tkinter import *
from graphics import *

def isValid(tri, assignment, tri_to_edge_dict, possible_ints):
   for i in tri_to_edge_dict[tri]: # neighbors
      if i in assignment:
         return False # invalid
   return True
    
def backtracking_search(initial, tri_to_edge_dict, possible_ints, max_set):
    return recursive_backtracking(initial, tri_to_edge_dict, possible_ints, max_set)

def recursive_backtracking(assignment, tri_to_edge_dict, possible_ints, max_set):
   if len(assignment) > len(max_set):
      max_set = assignment
      return max_set
   for tri in possible_ints:
      if isValid(tri, assignment, tri_to_edge_dict, possible_ints.remove(tri)):
         assignment.add(tri)
         result = recursive_backtracking(assignment, tri_to_edge_dict, possible_ints, max_set) #possible_ints[1: ]
         if len(assignment) > len(max_set):
            max_set = assignment      
   return max_set

def main():
   triangle_to_edges_dict = {} 
   
   triangle_to_edges_dict[0] = [1, 10, 19]
   triangle_to_edges_dict[1] = [0, 2, 8]
   triangle_to_edges_dict[2] = [1, 3, 6]
   triangle_to_edges_dict[3] = [2, 4, 19]
   triangle_to_edges_dict[4] = [3, 5, 17]
   triangle_to_edges_dict[5] = [4, 6, 15]
   triangle_to_edges_dict[6] = [2, 5, 7]
   triangle_to_edges_dict[7] = [6, 8, 14]
   triangle_to_edges_dict[8] = [1, 9, 7]
   triangle_to_edges_dict[9] = [8, 10, 13]
   triangle_to_edges_dict[10] = [0, 9, 11]
   triangle_to_edges_dict[11] = [10, 12, 18]
   triangle_to_edges_dict[12] = [11, 13, 16]
   triangle_to_edges_dict[13] = [9, 12, 14]
   triangle_to_edges_dict[14] = [7, 13, 15]
   triangle_to_edges_dict[15] = [5, 14, 16]
   triangle_to_edges_dict[16] = [12, 15, 17]
   triangle_to_edges_dict[17] = [4, 16, 18]
   triangle_to_edges_dict[18] = [11, 17, 19]
   triangle_to_edges_dict[19] = [0, 3, 18]
    
   possible_ints = [i for i in range(0, 20)] # 1 - 6
   
   solution = backtracking_search(set(), triangle_to_edges_dict, possible_ints, set()) 
   print (solution)

if __name__ == '__main__':
    main()
    
# find largest indpendent set of non-adjacents in 20 sided polygon