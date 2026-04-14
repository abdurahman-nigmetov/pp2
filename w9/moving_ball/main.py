import pygame
from ball import Ball

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

ball = Ball(25, 25)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ball.move("RIGHT", WIDTH, HEIGHT)
            elif event.key == pygame.K_LEFT:
                ball.move("LEFT", WIDTH, HEIGHT)
            elif event.key == pygame.K_UP:
                ball.move("UP", WIDTH, HEIGHT)
            elif event.key == pygame.K_DOWN:
                ball.move("DOWN", WIDTH, HEIGHT)

    screen.fill((255, 255, 255))
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()