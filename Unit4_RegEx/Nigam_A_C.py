import sys

idx = int(sys.argv[1]) - 50

myRegexList = [

# 0 MIN
                r"/(\w)+\w*\1\w*/i",
# 1 MIN
                r"/(\w)+(\w*\1){3}\w*/i",
# 2 7 OVER
                r"/^([01])([01]*\1)*$/i",
# 3 MIN
                r"/(?=\w*cat)\b\w{6}\b/si",
# 4 MIN
                r"/(?=\w*bri)(?=\w*ing)\b\w{5,9}\b/is",
# 5 1 OVER
                r"/(?!\w*cat)\b\w{6}\b/si",
# 6 1 OVER
                r"/\b((\w)(?!\w*\2))+\b/i",
# 7 5 OVER
                r"/(?!.*10011)^[01]*$/",
# 8 2 OVER
                r"/\w*([aeiou]){2}(?<!\1\1)\w*/i",
# 9 4 OVER
                r"/(?!.*1.1)^[01]*$/"
    ]

print(myRegexList[idx])