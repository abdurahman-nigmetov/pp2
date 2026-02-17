def is_usual(num: int) -> bool:
    if num == 1:
        return True
    if num % 2 == 0:
        return is_usual(num // 2)
    elif num % 3 == 0:
        return is_usual(num // 3)
    elif num % 5 == 0:
        return is_usual(num // 5)
    return False

number = int(input())
if is_usual(number):
    print("Yes")
else:
    print("No")