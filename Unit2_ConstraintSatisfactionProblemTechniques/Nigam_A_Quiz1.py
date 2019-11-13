# Arul Nigam
# Period: 2

from random import * 

def check_complete(assignment, vars, adjs): 
   if len(vars) != len(assignment):
       return False
   return True

def select_unassigned_var(assignment, vars):
   for v in vars:
      if v not in assignment: 
         return v
   return None
      
def isValid(value, var, assignment, vars, sd):
   all_set = {abs(assignment[a1] - assignment[a2]) for a1 in assignment for a2 in assignment if a1 != a2} # get all differences from the current assignment
   check_sum = sum([x for x in range(0, len(assignment))]) 
   if len(all_set) != check_sum: 
      return False 
   if value in assignment.values(): 
      return False 
   for a in assignment: 
      if abs(assignment[a] - value) in all_set:
         return False
   s_set = {assignment[a] for a in assignment} | {value} # union of two sets
   s_diff_set = {abs(a-b) for a in s_set for b in s_set if a != b} 
   if len(s_diff_set) != (check_sum + len(s_set) - 1): 
      return False
   return True 

def update_ds(assignment, vars, sd): 
   new_vars = {key:[x for x in value if x not in assignment.values()] for key, value in vars.items()} # this is a deep copy of a dictionary
   for k in new_vars:
      if k in assignment:
         new_vars[k] = []
   new_sd = {s for s in sd if s not in assignment.values()}
   all_set = {abs(assignment[a1] - assignment[a2])
      for a1 in assignment for a2 in assignment if a1 != a2}
   new_sd -= all_set
   return new_vars, new_sd
   
def backtracking_search(vars, sd):
   return recursive_backtracking({'T': 0}, vars, sd)

def recursive_backtracking(assignment, vars, sd):
   sol_set = set()
   print(assignment)
   if check_complete(assignment, vars, sd): 
      print(sol_set)
      sol_set.update(assignment) # return assignment
      print(sol_set)
      return sol_set
   var = select_unassigned_var(assignment, vars)
   for value in vars[var]:
      value = choice(vars[var])
      if isValid(value, var, assignment, vars, sd):
         assignment[var] = value
         new_vars, new_sd = update_ds(assignment, vars, sd) # make deep copies before recursive call
         result = recursive_backtracking(assignment, new_vars, new_sd)
         if result != None: 
            sol_set.update(result)
         del assignment[var]
   print("returning")
   return sol_set
   
def main():
   solution = backtracking_search({'T':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'A':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'B':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'C':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'D':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}, [1, 2])
   print(solution)
   
if __name__ == '__main__':
   main()