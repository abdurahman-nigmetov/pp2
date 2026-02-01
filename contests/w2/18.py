n = int(input())
a = [input() for _ in range(n)]
entries = {}
for i in range(n):
    if a[i] not in entries:
        entries[a[i]] = i + 1
for key in sorted(entries.keys()):
    print(key, entries[key], sep=' ')