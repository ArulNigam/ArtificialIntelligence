import sys

idx = int(sys.argv[1]) - 30
myRegexList = [
    r"/^101$|^100$|^0$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^\+?1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s",
    r"/^\d{3} *-? *\d{2} *-? *\d{4}$/",
    r"/^.*?d\w*/mi",
    r"/^0[01]*0$|^1[01]*1$|^[01]?$/"
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