import sys
idx = int(sys.argv[1]) - 40
myRegexList = [
# 0
                r"/^[x.o]{64}$/i",
# 1
                r"/^[xo]*\.[xo]*$/i",
# 2
                r"/^x+o*\.|\.o*x+$|^\.|\.$/i",
# 3
                r"/^.(..)*$/s",
# 4
                r"/^(0|1[01])([01]{2})*$/",
# 5
                r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",

# 6
                r"/^0*(10+)*1*$/",
# 7
                r"/^([bc]+|[bc]*a[bc]*)$/",

# 8
                r"/^([bc]+|(a[bc]*a))+$/",
# 9
                r"/^((1[02]*1|2)0*)+$/"
    ]
print(myRegexList[idx])


'''
X means syntax error
E means script error
T means time out
M means missing
D means no trailing /
O means bad option
I means invalid regular expression
P means shouldn't be doing this
N means internal error
r'\ makes no \\
'''
