import re

s = input()
p = input()

count = re.findall(p, s)
print(len(count))