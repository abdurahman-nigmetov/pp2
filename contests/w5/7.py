import re

text = input()
pattern = input()
replacement = input()

print(re.sub(pattern, replacement, text))