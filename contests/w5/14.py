import re

text = input()

pattern = re.compile(r'^\d+$')

if pattern.fullmatch(text):
    print("Match")
else:
    print("No match")