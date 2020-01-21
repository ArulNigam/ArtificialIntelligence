# Name: Arul Nigam
# Period 3

import re

def num_30(str):
    # Current test checks if the string is '0'
    pattern_zero = "^0$"  # notice that python does not want / /
    pattern_onehundred = "^100$"  # notice that python does not want / /
    pattern_onehundredone = "^101$"  # notice that python does not want / /
    match = re.match(pattern_zero, str) or re.match(pattern_onehundred, str) or re.match(pattern_onehundredone, str)
    #print(match == re.match(r"/^101$|^100$|^0$/", str))
    print("string is either 0, 100, or 101: ", match != None)

def num_31(str):
    pattern = "^[01]*$"
    # Current test checks if the string is '0'
    print("string is a binary string:", re.match(pattern, str) != None)

# Pre-condition: input is a binary string, so you do not need to check if it's a binary or not.
def num_32(str):
    pattern = '[01]*0$'
    print("string is an even binary number:", re.match(pattern, str) != None)

def num_33(str):
    # Current test searches words with 'a'
    pattern = r'\w*[aeiou]\w*[aeiou]\w*'
    # Notice that python does not support /i in the pattern.
    # Use re.I for case insensitive when you match(exact same) or search(has one or more)
    print("there's a word at least two vowels:", re.search(pattern, str, re.I) != None)

def num_34(str):
    pattern = r'/^\+?1[01]*0$|^0$/'
    print("even binary integer string:", re.match(pattern, str) != None)

def num_35(str):
    pattern = r'^[01]*(101)[01]*$'
    print("binary string including 110:", re.match(pattern, str) != None)

def num_36(str):
    pattern = r'^.{2,4}$'
    print("length at least two, but at most four:", re.match(pattern, str) != None)

def num_37(str):
    pattern = r'/^\d{3}\s*-?\s*\d{2}\s*-?\s*\d{4}$/'
    print("valid social security number:", re.match(pattern, str) != None)

def num_38(str):
    # When you read multiline input such as "I\nAM\nSAM."
    str = str.replace('\\n', '\n')
    pattern = r'([a-z]*d+[a-z]*){1}+'
    # When you want to use /im options:
    d_search = re.search(pattern, str, re.I | re.MULTILINE)
    print("first word with d on a line:", d_search != None)

def num_39(str):
   print("There's same number of 01 substrings as 10 substrings: ",
         len(re.findall('(01)', str)) == len(re.findall('(10)', str)))

while (True):
    input_num = input("Choose the exercise # (30 - 39 or -1 to terminate):")
    if input_num == '-1': exit("Good bye")
    input_str = input("Input string: ")
    if input_num == '30':
        num_30(input_str)
    elif input_num == '31':
        num_31(input_str)
    elif input_num == '32':
        num_32(input_str)
    elif input_num == '33':
        num_33(input_str)
    elif input_num == '34':
        num_34(input_str)
    elif input_num == '35':
        num_35(input_str)
    elif input_num == '36':
        num_36(input_str)
    elif input_num == '37':
        num_37(input_str)
    elif input_num == '38':
        num_38(input_str)
    elif input_num == '39':
        num_39(input_str)
    print()

''' Sample Output
Choose the exercise # (31 - 40 or -1 to terminate):31
Input string: 100
string is either 0, 100, or 101:  True

Choose the exercise # (31 - 40 or -1 to terminate):31
Input string: 1000
string is either 0, 100, or 101:  False

Choose the exercise # (31 - 40 or -1 to terminate):40
Input string: 101
There's same number of 01 substrings as 10 substrings:  True

Choose the exercise # (31 - 40 or -1 to terminate):40
Input string: 100
There's same number of 01 substrings as 10 substrings:  False

Choose the exercise # (31 - 40 or -1 to terminate):40
Input string: 0
There's same number of 01 substrings as 10 substrings:  True

Choose the exercise # (31 - 40 or -1 to terminate):-1
Good bye

 ----jGRASP wedge2: exit code for process is 1.
 ----jGRASP: operation complete.

'''