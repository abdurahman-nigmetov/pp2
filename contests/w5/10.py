import re

s = input()
is_true = re.findall(r"cat|dog", s)
if is_true:
    print("Yes")
else:
    print("No")