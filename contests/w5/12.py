import re

s = input()
digits = re.findall(r"\d+", s)
len_of_3 = list(filter(lambda x: len(x) >= 2, digits))
print(*len_of_3)