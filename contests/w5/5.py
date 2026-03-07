import re

s = input()
x = re.match("^[a-zA-Z]+[0-9]$", s)
if x:
    print("Yes")
else:
    print("No")