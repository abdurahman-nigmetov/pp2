n, l, r = map(int, input().split())
a = list(map(int, input().split()))
a[l - 1:r:] = reversed(a[l - 1:r:]) 
for i in range(n):
    print(a[i], end=' ')