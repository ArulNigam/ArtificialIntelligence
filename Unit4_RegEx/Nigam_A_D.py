import sys

idx = int(sys.argv[1]) - 60

myRegexList = [

# 0 (14 IS MIN, @ 16)   

         r"/(?!.*010)^[01]*$/",
         
# 1 (20 IS MIN, @ 22)
  
         r"/(?!.*(101|010))^[01]*$/",

# 2 (14 IS MIN, @ 18)  

         r"/^([01])([01]*\1)*$/i",

# 3 (21 IS MIN)  

         r"//",

# 4 (43 IS MIN)  

         r"//",

# 5 (42 IS MIN)  

         r"//",

# 6 (41 IS MIN)  

         r"//",

# 7 (22 IS MIN)  

         r"//",

# 8 (16 IS MIN)  

         r"//",

# 9 (19 IS MIN)  

         r"//"
                
              ]

print(myRegexList[idx])