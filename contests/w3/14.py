n = int(input())
nums = list(map(int, input().split()))
operations = int(input())
for _ in range(operations):
    operation, *x = input().split()
    match operation:
        case "add":
            nums = list(map(lambda num: num + int(x[0]), nums))
        case "multiply":
            nums = list(map(lambda num: num * int(x[0]), nums))
        case "power":
            nums = list(map(lambda num: num ** int(x[0]), nums))
        case "abs":
            nums = list(map(lambda num: abs(num), nums))
print(*nums, sep=" ")
        