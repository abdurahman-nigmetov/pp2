import re

text = input()

match = re.search(r'^Name:\s*(.+),\s*Age:\s*(.+)$', text)

if match:
    print(match.group(1), match.group(2))