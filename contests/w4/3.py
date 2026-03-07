def divisible_check(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for number in divisible_check(n):
    print(number, end=" ")