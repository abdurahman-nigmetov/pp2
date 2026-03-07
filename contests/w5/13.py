import re

s = input()
seq = len(re.findall(r'\w+', s))
print(seq)