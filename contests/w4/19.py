import math

R = float(input().strip())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

def dist_to_segment_origin(ax, ay, bx, by):
    vx = bx - ax
    vy = by - ay
    denom = vx * vx + vy * vy
    if denom == 0.0:
        return math.hypot(ax, ay)
    t = -(ax * vx + ay * vy) / denom
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    cx = ax + t * vx
    cy = ay + t * vy
    return math.hypot(cx, cy)

straight = math.hypot(x2 - x1, y2 - y1)
dmin = dist_to_segment_origin(x1, y1, x2, y2)

if dmin >= R - 1e-12:
    ans = straight
else:
    a = math.hypot(x1, y1)
    b = math.hypot(x2, y2)

    angA = math.atan2(y1, x1) if a != 0.0 else 0.0
    angB = math.atan2(y2, x2) if b != 0.0 else 0.0

    alpha = 0.0 if a <= R else math.acos(R / a)
    beta = 0.0 if b <= R else math.acos(R / b)

    lenA = 0.0 if a <= R else math.sqrt(a * a - R * R)
    lenB = 0.0 if b <= R else math.sqrt(b * b - R * R)

    twopi = 2.0 * math.pi
    tA = [angA + alpha, angA - alpha]
    tB = [angB + beta, angB - beta]

    ans = float("inf")
    for u in tA:
        for v in tB:
            delta = (u - v) % twopi
            if delta > math.pi:
                delta = twopi - delta
            ans = min(ans, lenA + lenB + R * delta)

print(f"{ans:.10f}")