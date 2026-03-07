def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

n = int(input())
for i, number in enumerate(fibonacci(n)):
    if i == n - 1:
        print(number)
    else:
        print(number, end=",")