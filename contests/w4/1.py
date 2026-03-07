def square_numbers_to_n(n):
  for i in range(1, n + 1):
    yield i ** 2

n = int(input())

for number in square_numbers_to_n(n):
    print(number)