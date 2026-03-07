import math

R = float(input().strip())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
seg_len = math.hypot(dx, dy)

r2 = R * R
in1 = x1 * x1 + y1 * y1 <= r2
in2 = x2 * x2 + y2 * y2 <= r2

a = dx * dx + dy * dy
b = 2.0 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - r2

disc = b * b - 4.0 * a * c

ans = 0.0

if disc < 0.0:
    ans = seg_len if (in1 and in2) else 0.0
else:
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2.0 * a)
    t2 = (-b + sqrt_disc) / (2.0 * a)
    lo = max(0.0, min(t1, t2))
    hi = min(1.0, max(t1, t2))
    if hi <= lo:
        ans = seg_len if (in1 and in2) else 0.0
    else:
        ans = seg_len * (hi - lo)

print(f"{ans:.10f}")