import pygame

WHITE = (245, 245, 245)
BLACK = (18, 18, 18)
BG = (26, 29, 35)
PANEL = (44, 49, 60)
ACCENT = (244, 196, 48)
ACCENT_HOVER = (255, 213, 88)
MUTED = (188, 194, 205)


class Button:
    def __init__(self, rect, text, font, bg=ACCENT, fg=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg
        self.fg = fg

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        color = ACCENT_HOVER if hovered else self.bg
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=10)

        label = self.font.render(self.text, True, self.fg)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_panel(screen, rect):
    pygame.draw.rect(screen, PANEL, rect, border_radius=14)
    pygame.draw.rect(screen, (70, 76, 90), rect, width=2, border_radius=14)


def draw_center_text(screen, text, font, color, y):
    label = font.render(text, True, color)
    rect = label.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(label, rect)


def draw_left_text(screen, text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))