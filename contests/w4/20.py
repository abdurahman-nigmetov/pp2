g = 0

def outer():
    n = 0

    def inner():
        nonlocal n
        global g

        m = int(input().strip())
        for _ in range(m):
            scope, value = input().split()
            value = int(value)
            if scope == "global":
                g += value
            elif scope == "nonlocal":
                n += value
            else:
                x = value

    inner()
    return n

n_final = outer()
print(g, n_final)