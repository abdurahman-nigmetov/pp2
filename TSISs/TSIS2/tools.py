import math
from collections import deque
from datetime import datetime
from pathlib import Path

import pygame


def save_canvas(canvas, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_path / f"paint_{timestamp}.png"
    pygame.image.save(canvas, str(filename))
    return str(filename)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x0, y0 = start_pos
    if not (0 <= x0 < width and 0 <= y0 < height):
        return

    origin_color = surface.get_at((x0, y0))
    if origin_color == pygame.Color(*fill_color):
        return

    queue = deque([(x0, y0)])

    # Classic BFS fill using exact color match.
    while queue:
        x, y = queue.popleft()
        if x < 0 or y < 0 or x >= width or y >= height:
            continue
        if surface.get_at((x, y)) != origin_color:
            continue

        surface.set_at((x, y), fill_color)
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_rectangle(screen, start, end, color, line_width):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    rect_width = abs(x2 - x1)
    rect_height = abs(y2 - y1)

    pygame.draw.rect(screen, color, (left, top, rect_width, rect_height), max(1, line_width))


def draw_square(screen, start, end, color, line_width):
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    left = x1 if x2 >= x1 else x1 - size
    top = y1 if y2 >= y1 else y1 - size

    pygame.draw.rect(screen, color, (left, top, size, size), max(1, line_width))


def draw_circle(screen, start, end, color, line_width):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    radius = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2

    if radius > 0:
        pygame.draw.circle(screen, color, (center_x, center_y), radius, max(1, line_width))


def draw_right_triangle(screen, start, end, color, line_width):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    side = math.hypot(dx, dy)
    if side <= 1:
        return

    # Keep existing project behavior for V-tool.
    cos60 = 0.5
    sin60 = math.sqrt(3) / 2
    rx = dx * cos60 - dy * sin60
    ry = dx * sin60 + dy * cos60

    points = [
        (x1, y1),
        (x2, y2),
        (int(x1 + rx), int(y1 + ry)),
    ]

    pygame.draw.polygon(screen, color, points, max(1, line_width))


def draw_equilateral_triangle(screen, start, end, color, line_width):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    drag_len = math.hypot(dx, dy)
    if drag_len <= 1:
        return

    # Keep existing project behavior for I-tool.
    half_base = max(1.0, abs(dx))
    height = max(1.0, abs(dy))
    angle = math.atan2(dy, dx) - math.pi / 2
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    local_points = [
        (0.0, 0.0),
        (-half_base, height),
        (half_base, height),
    ]

    points = []
    for lx, ly in local_points:
        rx = lx * cos_a - ly * sin_a
        ry = lx * sin_a + ly * cos_a
        points.append((int(x1 + rx), int(y1 + ry)))

    pygame.draw.polygon(screen, color, points, max(1, line_width))


def draw_rhombus(screen, start, end, color, line_width):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    if right == left or bottom == top:
        return

    center_x = left + (right - left) // 2
    center_y = top + (bottom - top) // 2

    points = [
        (center_x, top),
        (right, center_y),
        (center_x, bottom),
        (left, center_y),
    ]
    pygame.draw.polygon(screen, color, points, max(1, line_width))
