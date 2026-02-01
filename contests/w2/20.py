n = int(input())
db = {}
results = ""
for _ in range(n):
    line = input().split()
    comand, key = line[:2]
    if comand == "set":
        value = line[2]
        db[key] = value
    elif comand == "get":
        results += f"{db.get(key, f'KE: no key {key} found in the document')}\n"
print(results, end='')