n = int(input())
a = {}
for i in range(n):
    s, c = input().split()
    c = int(c)
    if s not in a:
        a[s] = c
    else:
        a[s] += c
for k, v in sorted(a.items()):
    print(k, v, sep=' ')


