n = int(input())
while n > 1:
    if n % 2 != 0:
        print("NO")
        break
    n //= 2
else:
    print("YES")