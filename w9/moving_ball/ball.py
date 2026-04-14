import pygame

class Ball:
    def __init__(self, x, y, radius=25, step=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step

    def move(self, direction, width, height):
        if direction == "RIGHT":
            if self.x + self.step + self.radius <= width:
                self.x += self.step

        elif direction == "LEFT":
            if self.x - self.step - self.radius >= 0:
                self.x -= self.step

        elif direction == "UP":
            if self.y - self.step - self.radius >= 0:
                self.y -= self.step

        elif direction == "DOWN":
            if self.y + self.step + self.radius <= height:
                self.y += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)