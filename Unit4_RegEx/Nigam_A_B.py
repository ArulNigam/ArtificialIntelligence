# -*- coding: utf-8 -*-
"""Nigam_A_B

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KIwjnuTAtkzJh3uZJIeSdDorJCIGbeu5
"""

import sys

idx = int(sys.argv[1]) - 40
myRegexList = [
# 0    r"/^10[01]$|^0$/i",
                r"/^[x.o]{64}$/i",
# 1   r"/^[01]*$/",
                r"/^[xo]*\.[xo]*$/i",
# 2   r"/0$/",
                r"/^x+o*\.|\.o*x+$|^\.|\.$/i",
# 3   r"/\w*[aeiou]\w*[aeiou]\w*/i",
                r"/^(..)*.$/s",
# 4   r"/^1[01]*0$|^0$/",
                r"/^(0|1[01])([01]{2})*$/",
# 5   r"/^[01]*110[01]*$/",
                r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
# 6   r"/^.{2,4}$/si",
                r"/^0*(10+)*1*$/",
# 7  r"/^\d{3} *-? *\d\d *-? *\d{4}$/i",
                r"/^([bc]*a?[bc]+|[bc]+a?[bc]*|a)$/"
# 8  r"/^.*?d\w*/mi",
# 9  r"/^0[01]*0$|^1[01]*1$|^[01]?$/"
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

