# Name: Arul Nigam
# Period: 3

def check_complete(assignment, vars, adjs):
   # check if assignment is complete or not. Goal_Test 
   if sorted(assignment.keys()) != sorted(adjs.keys()):
      return False
   for key in vars:
      if key in adjs:
         for adjacent in adjs[key]:
            if adjacent in assignment:
               if assignment[key] == assignment[adjacent]:
                  return False            
   return True

def select_unassigned_var(assignment, vars, adjs): 
   # Select an unassigned variable - forward checking, MRV, or LCV
   # returns a variable
   for key in vars:
      if key not in assignment: 
         return vars[key]
   
def isValid(value, var, assignment, variables, adjs):
   # value is consistent with assignment
   # check adjacents to check 'var' is working or not.
   for adjacent in adjs[var]:
      if value == assignment[adjacent]: # var is region, value is color
         return False 
   return True

def backtracking_search(variables, adjs): 
   return recursive_backtracking({}, variables, adjs)

def recursive_backtracking(assignment, variables, adjs):
   if check_complete(assignment, variables, adjs):
      return assignment
   var = select_unassigned_var(assignment, variables, adjs) # var isa region
   for value in variables[var]:
      if isValid(value, var, assignment, variables, adjs):
         assignment[var] = value
         result = recursive_backtracking(assignment, variables, adjs)

         if not check_complete(result, variables, adjs):
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

if __name__ == '__main__':
   main()
   
''' Sample output:
{'WA': 'R', 'NT': 'G', 'SA': 'B', 'Q': 'R', 'NSW': 'G', 'V': 'R', 'T': 'R'}
By using graphics functions, visualize the map.
'''