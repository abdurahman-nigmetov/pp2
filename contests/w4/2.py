def all_even_numbers_to_n(n):
    for i in range(0, n + 1):
        if i % 2 == 0 or i == 0:
            yield i

n = int(input())
for number in all_even_numbers_to_n(n):
    if number == n or number == n - 1:
        print(number, end="")
    else:        
        print(number, end=",")