def limited_cycle(nums: list, n):
    for i in range(n):
        for num in nums:
            yield num

a = list(input().split())
k = int(input())

for number in limited_cycle(a, k):
    print(number, end=" ")
