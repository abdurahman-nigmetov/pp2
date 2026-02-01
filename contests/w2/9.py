n = int(input())
a = list(map(int, input().split()))
max_a = max(a)
min_a = min(a)
for i in range(n):
    if a[i] == max_a:
        a[i] = min_a
    print(a[i], end=' ')
