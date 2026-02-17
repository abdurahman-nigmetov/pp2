numbers = list(map(int, input().split()))
prime_numbers = list(filter(lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)), numbers))
if not prime_numbers:
    print("No primes")
else:
    print(*prime_numbers, sep=" ")