import pygame
from clock import load_images, draw_clock

pygame.init()

WIDTH = 1400
HEIGHT = 950

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

clock_img, mickey_img, left_hand, right_hand = load_images()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_clock(screen, clock_img, mickey_img, left_hand, right_hand)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()