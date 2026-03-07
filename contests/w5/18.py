import re

s = input()
pattern = input()

escaped = re.escape(pattern)
print(len(re.findall(escaped, s)))