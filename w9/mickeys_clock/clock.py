import datetime
import pygame


def load_images():
    clock_img = pygame.image.load("images/clock.png").convert_alpha()
    mickey_img = pygame.image.load("images/mickey.png").convert_alpha()
    left_hand = pygame.image.load("images/hand_left.png").convert_alpha()
    right_hand = pygame.image.load("images/hand_right.png").convert_alpha()

    clock_img = pygame.transform.smoothscale(clock_img, (800, 800))
    mickey_img = pygame.transform.smoothscale(mickey_img, (260, 360))
    left_hand = pygame.transform.smoothscale(left_hand, (180, 180))
    right_hand = pygame.transform.smoothscale(right_hand, (180, 180))

    return clock_img, mickey_img, left_hand, right_hand


def get_angles():
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = -((minutes + seconds / 60) * 6)
    second_angle = -(seconds * 6)

    return minute_angle, second_angle


def blit_rotate(screen, image, pivot_screen, pivot_image, angle):
    image_rect = image.get_rect(topleft=(pivot_screen[0] - pivot_image[0],
                                         pivot_screen[1] - pivot_image[1]))

    offset_center_to_pivot = pygame.math.Vector2(pivot_screen) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_center = (pivot_screen[0] - rotated_offset.x,
                      pivot_screen[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rotated_center)

    screen.blit(rotated_image, rotated_rect)


def draw_clock(screen, clock_img, mickey_img, left_hand, right_hand):
    screen.fill((255, 255, 255))

    screen_rect = screen.get_rect()
    center = screen_rect.center

    clock_rect = clock_img.get_rect(center=center)
    screen.blit(clock_img, clock_rect)

    minute_angle, second_angle = get_angles()

    pivot_screen = center

    left_pivot_image = (left_hand.get_width() // 2, left_hand.get_height() - 20)
    right_pivot_image = (right_hand.get_width() // 2, right_hand.get_height() - 20)

    left_offset = -90
    right_offset = -90

    blit_rotate(screen, right_hand, pivot_screen, right_pivot_image, minute_angle + right_offset)

    blit_rotate(screen, left_hand, pivot_screen, left_pivot_image, second_angle + left_offset)

    mickey_rect = mickey_img.get_rect(center=(center[0], center[1] + 0))
    screen.blit(mickey_img, mickey_rect)