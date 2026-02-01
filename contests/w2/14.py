n = int(input())
a = list(map(int, input().split()))
freq = {}
for num in a:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1
max_count = max(freq.values())
most_frequent_numbers = [num for num, count in freq.items() if count == max_count]
print(min(most_frequent_numbers))