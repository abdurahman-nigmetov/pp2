import re

s = input()

digits = re.findall("\\d", s)
if digits:
    for digit in digits:
        print(digit, end=" ")
else:
    print("")