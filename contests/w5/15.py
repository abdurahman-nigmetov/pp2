import re

text = input()

print(re.sub(r'\d', lambda match: match.group() * 2, text))