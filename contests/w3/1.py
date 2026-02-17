number = int(input())
def is_valid(num):
    while num > 0:
        digit = num % 10
        if digit % 2 != 0:
            return False
        num = num // 10
    return True
if is_valid(number):
    print("Valid")
else:
    print("Not valid")