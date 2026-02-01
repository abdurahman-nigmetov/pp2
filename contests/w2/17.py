n = int(input())
a = [input() for _ in range(n)]
count_map = {}
for num in a:
    if num in count_map:
        count_map[num] += 1
    else:
        count_map[num] = 1
count = 0
for num in count_map:
    if count_map[num] == 3:
        count += 1
print(count)