import sys

idx = int(sys.argv[1]) - 30
myRegexList = [
    r"/^10[01]$|^0$/i",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/si",
    r"/^\d{3} *-? *\d\d *-? *\d{4}$/i",
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