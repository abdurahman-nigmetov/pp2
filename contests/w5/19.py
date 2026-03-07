import re

text = input()

pattern = re.compile(r'\b\w+\b')
print(len(pattern.findall(text)))