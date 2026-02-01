n = int(input())
a = list(map(int, input().split()))
a.sort()
a.reverse()
for i in range(n):
    print(a[i], end=' ')