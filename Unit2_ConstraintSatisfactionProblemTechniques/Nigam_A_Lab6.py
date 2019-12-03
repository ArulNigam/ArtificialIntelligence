# Name: Arul Nigam
# Period: 3

import time, copy, random, math

def display(solution):
   print(solution)

def main():
    n = int(input("What is N? "))
    population = [[random.randint(0, 7) for i in range(n)] for j in range(n)]
    cur_time = time.time()
    solution = genetic_algorithm(population)  # 2 What does '0' represent?
    display(solution)
    print(time.time() - cur_time)

def genetic_algorithm(population):
   n = len(population)
   fit_enough = False
   fittest = None
   while not fit_enough:  
      new_population = [[0 for i in range(n)] for j in range(n)]
      for i in range(1, n):
         x = random_selection(population)
         y = random_selection(population)
         child = reproduce(x, y)
         if random.randint(1, 10) == 1:
            child = mutate(child)
         new_population.append(child)
      population = new_population
      fit_enough, fittest = find_fittest(population)   
   return fittest

def reproduce(x, y):
   c = random.randint(1, 7)
   return x[1 : c] + y[c + 1 : len(x) - 1]

def mutate(child):
   index = random.randint(0, 7)
   val = random.randint(0, 7)
   return child[0 : index - 1] + [val] + child[index + 1 : len(child) - 1]

def random_selection(population):
   index = random.randint(0, len(population) - 1)
   return population[index]
   
def find_fittest(population):
   max_ind, max_fit = 0, 0
   temp_ind, max_ind = None, None 
   fit_enough = False  
   for individual in population:
      temp_fit = fitness(individual, population)
      temp_ind = individual
      if temp_fit > max_fit:
         max_fit, max_ind = temp_fit, temp_ind
   if max_fit == int(math.factorial(len(population[0])) / math.factorial(2) / math.factorial(len(population[0]) - 2)):
      fit_enough = True
   return fit_enough, max_ind      
                 
def fitness(individual, population):   
   attacks = 0
   col = 0
   board = [[0 for i in range(len(individual))] for j in range(len(individual))]
   for i in range(len(board)):
      for j in range(len(board)):
         board[i][j] = individual[i]
   for x in individual:
      try:
         for i in range(col - 1, -1, -1):
            if board[x][i] == 1:
               attacks += 1    
      finally:
         for i, j in zip(range(x - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i][j] == 1:
               attacks += 1
         for i, j in zip(range(x + 1, len(individual), 1), range(col - 1, -1, -1)):
            if board[i][j] == 1:
               attacks += 1
         col += 1
      return int(math.factorial(len(individual)) / math.factorial(2) / math.factorial(len(individual) - 2)) - attacks   
   
if __name__ == '__main__':
    main()
