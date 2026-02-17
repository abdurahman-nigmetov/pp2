nums = {
        "ONE": 1,
        "TWO": 2,
        "THR": 3,
        "FOU": 4,
        "FIV": 5,
        "SIX": 6,
        "SEV": 7,
        "EIG": 8,
        "NIN": 9,
        "ZER": 0
    }

def from_string(s):
    result = 0
    for i in range(0, len(s), 3):
        part = s[i:i+3]
        result = result * 10 + nums[part]
    return result

def to_statemant(s: str):
    if "+" in s:
        parts = s.split("+")
        return from_string(parts[0]) + from_string(parts[1])
    elif "-" in s:
        parts = s.split("-")
        return from_string(parts[0]) - from_string(parts[1])
    elif "*" in s:
        parts = s.split("*")
        return from_string(parts[0]) * from_string(parts[1])
    elif "/" in s:
        parts = s.split("/")
        return from_string(parts[0]) // from_string(parts[1])
    
def from_statemant(n: int) -> str:
    if n == 0:
        return "ZER"
    result = ""
    while n > 0:
        digit = n % 10
        for key, value in nums.items():
            if value == digit:
                result = key + result
                break
        n //= 10
    return result

s = input()
print(from_statemant(to_statemant(s)))
    