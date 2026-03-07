import re

s = input()
d = input()

line = re.split(d, s)

for i, item in enumerate(line):
    if i == len(line) - 1:
        print(item)
        break
    print(item, end=',')
