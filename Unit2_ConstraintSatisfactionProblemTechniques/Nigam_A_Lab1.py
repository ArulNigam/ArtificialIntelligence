# Name: Arul Nigam
# Period: 3

from tkinter import * 
from graphics import *

def check_complete(assignment, vars, adjs):     
   # check if assignment is complete or not. Goal_Test 
   if assignment != None:
      if sorted(assignment.keys()) != sorted(vars.keys()):
         return False
      for key in vars:
         if key in adjs:
            for adjacent in adjs[key]:
               if adjacent in assignment:
                  if assignment[key] == assignment[adjacent]:
                     return False  
   return True

def select_unassigned_var(assignment, vars, adjs): # Select an unassigned variable - forward checking, MRV, or LCV
   # Forward Checking:
   #return forward_checking(assignment, vars)
   # MRV:
   return minimum_remaining_values(assignment, vars, adjs)
   #LCV:
   #return least_constraining_values(assignment, vars, adjs)
         
def forward_checking(assignment, vars): 
   for key in vars:
      if key not in assignment: 
         return key
         
def minimum_remaining_values(assignment, vars, adjs): 
   min_val_pair = [4, None] # [Number of Remaining Possible Values, Region with Minimum Remianing Possible Values]...start with 4 because maximum possible # of colors is 3
   for key in vars: # for each region that exists
      if key not in assignment: # if region is not already assigned, b/c otherwise would be pointless
         rem_val_count = set() # Temporary Counter
         if key in adjs: # if region has neighbors
            for adj_key in adjs[key]: # for each neighboring region
               if adj_key in assignment: # count it if it has have been assigned (additional constrraint, b/c can't be color x)
                  rem_val_count.add(assignment[adj_key])
         else: # is an island
            rem_val_count.add("temp1") # 3 possible colors b/c no constraints
            rem_val_count.add("temp2") # 3 possible colors b/c no constraints
            rem_val_count.add("temp3") # 3 possible colors b/c no constraints
         if len(rem_val_count) < min_val_pair[0]: # if this region has fewer constraints than what we think the min_val_pair is 
            min_val_pair = [len(rem_val_count), key] # update the min_val_pair
   return min_val_pair[1]
         
def least_constraining_values(assignment, vars, adjs): 
   for key in vars:
      if key not in assignment: 
         return key
            
def isValid(value, var, assignment, variables, adjs):
   # value is consistent with assignment
   # check adjacents to check 'var' is working or not.
   if var in adjs:
      for adjacent in adjs[var]:
         if adjacent in assignment:
            if value == assignment[adjacent]: # var is region, value is color
               return False 
   return True

def backtracking_search(variables, adjs): 
   frame = GraphWin('Australia Map Coloring - CSP Techniques Lab 1', 1000, 1000)
   frame.setCoords(0, 0, 999, 999) 
   shapes = {'WA': Polygon([Point(400, 450), Point(400, 800), Point(50, 600)]), 'NT': Polygon([Point(400, 800), Point(600, 750), Point(600, 600), Point(400, 600)]), 'SA': Polygon([Point(400, 600), Point(400, 450), Point(650, 300), Point(650, 600)]), 'Q': Polygon([Point(650, 600), Point(600, 600), Point(600, 750), Point(950, 500), Point(650, 500)]), 'NSW': Polygon([Point(950, 500), Point(650, 500), Point(650, 400), Point(900, 300)]), 'V': Polygon([Point(650, 400), Point(900, 300), Point(650, 300)]), 'T': Polygon([Point(750, 250), Point(800, 250), Point(800, 200), Point(750, 200)])}
   colors = {'R': "red", 'G': "green", 'B': "blue"}
   return recursive_backtracking({}, variables, adjs, frame, shapes, colors)

def recursive_backtracking(assignment, variables, adjs, frame, shapes, colors):
   if check_complete(assignment, variables, adjs):
      return assignment
   var = select_unassigned_var(assignment, variables, adjs) # var isa region
   if var != None:
      for value in variables[var]: # variables maps region to rgb color
         assignment[var] = value
         shape = shapes[var]   
         shape.setFill(colors[assignment[var]]) 
         shape.setOutline("black") 
         shape.undraw()
         shape.draw(frame)
         time.sleep(0.5)
         if isValid(value, var, assignment, variables, adjs):
            result = recursive_backtracking(assignment, variables, adjs, frame, shapes, colors)
            if check_complete(result, variables, adjs):
               return result
            assignment.pop(var)
   return None

def main():
   
   regions, variables, adjacents  = [], {}, {}
   # Read mcNodes.txt and store all regions in regions list
   fileName = "mcNodes.txt"
   file = open(fileName, "r")
   for node in file.readlines():
       region = node.rstrip('\n')
       regions.append(region)
   file.close()
   
   # Fill variables by using regions list -- no additional code for this part
   for r in regions: variables[r] = ['R', 'G', 'B']

   # Read mcEdges.txt and fill the adjacents. Edges are bi-directional.
   fileName = "mcEdges.txt"
   file = open(fileName, "r")
   for node in file.readlines():
       node = node.rstrip('\n')
       nodeList = node.split(" ")
       node1 = nodeList[0]
       node2 = nodeList[1]
       if node1 not in adjacents:
           adjacents[node1] = [node2]
       else:
           adjacents[node1].append(node2)
       if node2 not in adjacents:
           adjacents[node2] = [node1]
       else:
           adjacents[node2].append(node1)
   file.close()

   # solve the map coloring problem by using backtracking_search
   solution = backtracking_search(variables, adjacents) 
   print (solution)
   mainloop()

if __name__ == '__main__':
   main()
   
''' Sample output:
{'WA': 'R', 'NT': 'G', 'SA': 'B', 'Q': 'R', 'NSW': 'G', 'V': 'R', 'T': 'R'}
By using graphics functions, visualize the map.
'''
