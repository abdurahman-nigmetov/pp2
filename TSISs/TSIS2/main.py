from pathlib import Path

import pygame

from tools import (
    draw_circle,
    draw_equilateral_triangle,
    draw_rectangle,
    draw_rhombus,
    draw_right_triangle,
    draw_square,
    flood_fill,
    save_canvas,
)

WIDTH = 840
HEIGHT = 480
TOP_BAR_HEIGHT = 72
BG_COLOR = (0, 0, 0)

SMALL = 2
MEDIUM = 5
LARGE = 10

BASE_DIR = Path(__file__).resolve().parent
SAVES_DIR = BASE_DIR / "assets" / "saves"


def draw_ui(screen, font, tool, color, stroke_width, typing):
    panel = pygame.Surface((WIDTH, TOP_BAR_HEIGHT), pygame.SRCALPHA)
    panel.fill((40, 40, 40, 220))
    screen.blit(panel, (0, 0))

    line1 = f"Tool: {tool} | Size: {stroke_width}px"
    line2 = "Tools: P-pencil E-eraser L-line T-rect C-circle S-square V-right I-equilateral D-rhombus F-fill U-text"
    line3 = "Colors: R/G/B/Y/W | Size keys: 1/2/3 | Ctrl+S save | X clear"
    if typing:
        line3 = "Typing: Enter confirm, Esc cancel, Backspace delete"

    label1 = font.render(line1, True, (255, 255, 255))
    label2 = font.render(line2, True, (255, 255, 255))
    label3 = font.render(line3, True, (255, 255, 255))

    screen.blit(label1, (10, 5))
    screen.blit(label2, (10, 25))
    screen.blit(label3, (10, 45))

    pygame.draw.rect(screen, color, (WIDTH - 48, 20, 30, 25))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    tool = "pencil"
    stroke_width = MEDIUM

    drawing = False
    start_pos = None
    last_pos = None
    typing = False
    text_pos = (0, 0)
    text_buffer = ""

    ui_font = pygame.font.SysFont("Arial", 16)
    text_font = pygame.font.SysFont("Arial", 26)

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BG_COLOR)

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        if text_buffer:
                            text_surface = text_font.render(text_buffer, True, color)
                            canvas.blit(text_surface, text_pos)
                        typing = False
                        text_buffer = ""
                        continue
                    if event.key == pygame.K_ESCAPE:
                        typing = False
                        text_buffer = ""
                        continue
                    if event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                        continue
                    if event.unicode and event.unicode.isprintable() and not ctrl_held:
                        text_buffer += event.unicode
                        continue

                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_s and ctrl_held:
                    save_canvas(canvas, SAVES_DIR)
                    continue
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_1:
                    stroke_width = SMALL
                elif event.key == pygame.K_2:
                    stroke_width = MEDIUM
                elif event.key == pygame.K_3:
                    stroke_width = LARGE

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
                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_l:
                    tool = "line"
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
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_u:
                    tool = "text"
                elif event.key == pygame.K_x:
                    canvas.fill(BG_COLOR)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tool == "fill":
                    flood_fill(canvas, event.pos, color)
                    continue

                if tool == "text":
                    typing = True
                    text_pos = event.pos
                    text_buffer = ""
                    continue

                drawing = True
                start_pos = event.pos
                last_pos = event.pos

                if tool == "pencil":
                    pygame.draw.circle(canvas, color, event.pos, max(1, stroke_width // 2))
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, event.pos, max(1, stroke_width // 2))

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, event.pos, stroke_width)
                    last_pos = event.pos
                elif tool == "eraser":
                    pygame.draw.line(canvas, BG_COLOR, last_pos, event.pos, stroke_width)
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    end_pos = event.pos

                    if tool == "line" and start_pos:
                        pygame.draw.line(canvas, color, start_pos, end_pos, stroke_width)
                    if tool == "rect" and start_pos:
                        draw_rectangle(canvas, start_pos, end_pos, color, stroke_width)
                    elif tool == "circle" and start_pos:
                        draw_circle(canvas, start_pos, end_pos, color, stroke_width)
                    elif tool == "square" and start_pos:
                        draw_square(canvas, start_pos, end_pos, color, stroke_width)
                    elif tool == "right_triangle" and start_pos:
                        draw_right_triangle(canvas, start_pos, end_pos, color, stroke_width)
                    elif tool == "equilateral_triangle" and start_pos:
                        draw_equilateral_triangle(canvas, start_pos, end_pos, color, stroke_width)
                    elif tool == "rhombus" and start_pos:
                        draw_rhombus(canvas, start_pos, end_pos, color, stroke_width)

                drawing = False
                start_pos = None
                last_pos = None

        screen.blit(canvas, (0, 0))

        if drawing and tool in (
            "line",
            "rect",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus",
        ) and start_pos:
            current_pos = pygame.mouse.get_pos()
            preview = canvas.copy()

            if tool == "line":
                pygame.draw.line(preview, color, start_pos, current_pos, stroke_width)
            elif tool == "rect":
                draw_rectangle(preview, start_pos, current_pos, color, stroke_width)
            elif tool == "circle":
                draw_circle(preview, start_pos, current_pos, color, stroke_width)
            elif tool == "square":
                draw_square(preview, start_pos, current_pos, color, stroke_width)
            elif tool == "right_triangle":
                draw_right_triangle(preview, start_pos, current_pos, color, stroke_width)
            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(preview, start_pos, current_pos, color, stroke_width)
            elif tool == "rhombus":
                draw_rhombus(preview, start_pos, current_pos, color, stroke_width)

            screen.blit(preview, (0, 0))

        if typing:
            preview_text = text_buffer + ("|" if (pygame.time.get_ticks() // 400) % 2 == 0 else "")
            text_surface = text_font.render(preview_text, True, color)
            screen.blit(text_surface, text_pos)

        draw_ui(screen, ui_font, tool, color, stroke_width, typing)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()