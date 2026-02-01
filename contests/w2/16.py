n = int(input())
a = list(map(int, input().split()))
elements = set()
for i in range(n):
    if a[i] not in elements:
        elements.add(a[i])
        print("YES")
        continue
    print("NO")
    