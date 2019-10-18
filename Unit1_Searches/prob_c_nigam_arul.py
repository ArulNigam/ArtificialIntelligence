# Name: Arul Nigam
# Period: 3

def isPrime(num):
   if num < 2:
      return False
   if num == 2:
      return True
   if num % 2 == 0: # if num is even
      return False
   i = 3   
   while(i < int(num / 2)):
      if (num / i) == int(num / i):
         return False
      i += 1      
   return True

def main():
   n, p, i, x = int(input("Type N: ")), 1, 2, 0
   while x < n: # find P
      if isPrime(i):
         p *= i
         x += 1
      i += 1    
   i = p + 2
   notFoundQ = True      
   while(notFoundQ): # find Q
      if isPrime(i):
         notFoundQ = False
         q = i
      i += 1   
   i = p - 2
   notFoundR = True      
   while(notFoundR): # find R
      if isPrime(i):
         notFoundR = False
         r = i
      i -= 1 
   print(q - p, p - r)   

if __name__ == '__main__':
   main()
