import pygame
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((840, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 15
    color = (0, 0, 255)
    tool = "brush"

    drawing = False
    start_pos = None
    last_pos = None

    canvas = pygame.Surface((840, 480))
    canvas.fill((0, 0, 0))

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # colors
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

                # tools
                elif event.key == pygame.K_p:
                    tool = "brush"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_t:
                    tool = "rect"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_v:
                    tool = "right_triangle"
                elif event.key == pygame.K_i:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_d:
                    tool = "rhombus"

                # clear screen
                elif event.key == pygame.K_x:
                    canvas.fill((0, 0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                    if tool == "brush":
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 2:
                    radius = min(200, radius + 1)

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == "brush":
                    draw_line(canvas, last_pos, event.pos, radius, color)
                    last_pos = event.pos
                elif tool == "eraser":
                    draw_line(canvas, last_pos, event.pos, radius, (0, 0, 0))
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    end_pos = event.pos

                    if tool == "rect" and start_pos:
                        draw_rectangle(canvas, start_pos, end_pos, color)

                    elif tool == "circle" and start_pos:
                        draw_circle(canvas, start_pos, end_pos, color)

                    elif tool == "square" and start_pos:
                        draw_square(canvas, start_pos, end_pos, color)
                    elif tool == "right_triangle" and start_pos:
                        draw_right_triangle(canvas, start_pos, end_pos, color)
                    elif tool == "equilateral_triangle" and start_pos:
                        draw_equilateral_triangle(canvas, start_pos, end_pos, color)
                    elif tool == "rhombus" and start_pos:
                        draw_rhombus(canvas, start_pos, end_pos, color)

                drawing = False
                start_pos = None
                last_pos = None

        screen.blit(canvas, (0, 0))

        # preview for shape tools while dragging
        if drawing and tool in ("rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus") and start_pos:
            current_pos = pygame.mouse.get_pos()
            preview = canvas.copy()

            if tool == "rect":
                draw_rectangle(preview, start_pos, current_pos, color)
            elif tool == "circle":
                draw_circle(preview, start_pos, current_pos, color)
            elif tool == "square":
                draw_square(preview, start_pos, current_pos, color)
            elif tool == "right_triangle":
                draw_right_triangle(preview, start_pos, current_pos, color)
            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(preview, start_pos, current_pos, color)
            elif tool == "rhombus":
                draw_rhombus(preview, start_pos, current_pos, color)

            screen.blit(preview, (0, 0))

        draw_ui(screen, tool, color, radius)

        pygame.display.flip()
        clock.tick(60)


def draw_line(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations + 1):
        progress = i / iterations
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)
        pygame.draw.circle(screen, color, (x, y), width)


def draw_rectangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    pygame.draw.rect(screen, color, (left, top, width, height), 2)

def draw_square(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    left = x1 if x2 >= x1 else x1 - size
    top = y1 if y2 >= y1 else y1 - size

    pygame.draw.rect(screen, color, (left, top, size, size), 2)

def draw_circle(screen, start, end, color):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    radius = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2

    if radius > 0:
        pygame.draw.circle(screen, color, (center_x, center_y), radius, 2)

def draw_right_triangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    side = math.hypot(dx, dy)
    if side <= 1:
        return

    # Keep V behavior exactly as before: build regular triangle via 60-degree rotation.
    cos60 = 0.5
    sin60 = math.sqrt(3) / 2
    rx = dx * cos60 - dy * sin60
    ry = dx * sin60 + dy * cos60

    points = [
        (x1, y1),
        (x2, y2),
        (int(x1 + rx), int(y1 + ry)),
    ]

    pygame.draw.polygon(screen, color, points, 2)


def draw_equilateral_triangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    drag_len = math.hypot(dx, dy)
    if drag_len <= 1:
        return

    # Build an isosceles triangle in local space, then rotate it toward drag direction.
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

    pygame.draw.polygon(screen, color, points, 2)


def draw_rhombus(screen, start, end, color):
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

    # Rhombus via diagonal midpoints inside the drag box.
    points = [
        (center_x, top),
        (right, center_y),
        (center_x, bottom),
        (left, center_y),
    ]
    pygame.draw.polygon(screen, color, points, 2)

def draw_ui(screen, tool, color, radius):
    font = pygame.font.SysFont("Arial", 18)

    pygame.draw.rect(screen, (40, 40, 40), (0, 0, 840, 55))

    line1 = f"Tool: {tool} | Radius: {radius}"
    line2 = "Keys: P-brush E-eraser T-rect C-circle S-square V-right_triangle I-equilateral D-rhombus R/G/B/Y/W-color X-clear"

    label1 = font.render(line1, True, (255, 255, 255))
    label2 = font.render(line2, True, (255, 255, 255))

    screen.blit(label1, (10, 5))
    screen.blit(label2, (10, 28))

    pygame.draw.rect(screen, color, (790, 12, 30, 25))


main()