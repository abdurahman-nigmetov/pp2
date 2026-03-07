import re

s = input()
uppercase_len = len(re.findall('[A-Z]', s))
print(uppercase_len)