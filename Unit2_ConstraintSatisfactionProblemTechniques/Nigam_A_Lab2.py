# Name: Arul Nigam
# Period: 3

from tkinter import * 
from graphics import *

def check_complete(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):     
   # Goal Test: are there any unassigned (".") 
   if assignment == []:
      return False      
   for triangle_value in assignment:
      if triangle_value == ".":
         return False
   return True

def select_unassigned_var(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict): 
   # Select an unassigned variable - forward checking, MRV, or LCV
   # returns a variable
   for key in range(24):
      if assignment[key] == ".": 
         return key
            
def isValid(value, triangle, assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
   print("trngle", triangle)
   for hex in tri_to_hex_dict[triangle]: 
#      print("val", value, "hex", hex)
      for tri in hex_to_tri_dict[hex]:
         print("tri", tri)
         if assignment[tri] != ".":
            if int(assignment[tri]) == value and tri != triangle: # neighbors are the same:
               print("x", assignment[tri])
               print("FALSE")
               return False # invalid 
   print("TRUE")
   return True

def backtracking_search(assignment, triangle_to_hexagons_dict, possible_ints, hexagon_to_triangles_dict):    
   return recursive_backtracking(assignment, triangle_to_hexagons_dict, possible_ints, hexagon_to_triangles_dict)

def recursive_backtracking(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
   if check_complete(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
      return assignment
   triangle = select_unassigned_var(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict) 
   if triangle != None:
      for value in possible_ints[triangle]: # possible_ints maps traingle to [1 - 6]
         assignment[triangle] = value
         if isValid(value, triangle, assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
            result = recursive_backtracking(assignment, tri_to_hex_dict, possible_ints, hex_to_tri_dict)
            if check_complete(result, tri_to_hex_dict, possible_ints, hex_to_tri_dict):
               return result
            assignment.pop(var)
   return None

def main():
   
   triangle_to_hexagons_dict, possible_ints, hexagon_to_triangles_dict  = {}, [[] for i in range(24)], {} # triangle_to_hexagons_dict: regions, possible_ints: variables, hexagon_to_triangles_dict: adjacents

   triangle_to_hexagons_dict[0] = [1]
   triangle_to_hexagons_dict[1] = [1]
   triangle_to_hexagons_dict[2] = [1, 2]
   triangle_to_hexagons_dict[3] = [2]
   triangle_to_hexagons_dict[4] = [2]
   triangle_to_hexagons_dict[5] = [6]
   triangle_to_hexagons_dict[6] = [1, 6]
   triangle_to_hexagons_dict[7] = [0, 1, 6]
   triangle_to_hexagons_dict[8] = [0, 1, 2]
   triangle_to_hexagons_dict[9] = [0, 2, 3]
   triangle_to_hexagons_dict[10] = [2, 3]
   triangle_to_hexagons_dict[11] = [3]
   triangle_to_hexagons_dict[12] = [6]
   triangle_to_hexagons_dict[13] = [5, 6]
   triangle_to_hexagons_dict[14] = [0, 5, 6]
   triangle_to_hexagons_dict[15] = [0, 4, 5]
   triangle_to_hexagons_dict[16] = [0, 3, 4]
   triangle_to_hexagons_dict[17] = [3, 4]
   triangle_to_hexagons_dict[18] = [3]
   triangle_to_hexagons_dict[19] = [5]
   triangle_to_hexagons_dict[20] = [5]
   triangle_to_hexagons_dict[21] = [4, 5]
   triangle_to_hexagons_dict[22] = [4]
   triangle_to_hexagons_dict[23] = [4]
    
   for r in range(len(triangle_to_hexagons_dict)): 
      possible_ints[r] = [i for i in range(1, 7)] # 1 - 6

   hexagon_to_triangles_dict[0] = [7, 8, 9, 14, 15, 16]
   hexagon_to_triangles_dict[1] = [0, 1 , 2, 6, 7, 8]
   hexagon_to_triangles_dict[2] = [2, 3, 4, 8, 9, 10]
   hexagon_to_triangles_dict[3] = [9, 10, 11, 16, 17, 18]
   hexagon_to_triangles_dict[4] = [15, 16, 17, 21, 22, 23]
   hexagon_to_triangles_dict[5] = [13, 14, 15, 19, 20, 21]
   hexagon_to_triangles_dict[6] = [5, 6, 7, 12, 13, 14]
   
   # solve the map coloring problem by using backtracking_search
   solution = backtracking_search(list(sys.argv[1]), triangle_to_hexagons_dict, possible_ints, hexagon_to_triangles_dict) 
   print (solution)

if __name__ == '__main__':
   main()
