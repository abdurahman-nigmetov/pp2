import re

s = input()
count = len(re.findall(r'\b\w{3}\b', s))

print(count)