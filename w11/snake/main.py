import pygame
from worm import Worm
from food import Food
from wall import Wall


WIDTH = 400
HEIGHT = 300
TILE = 20
BASE_FPS = 5
FOODS_PER_LEVEL = 3
FOOD_LIFETIME_MS = 5000


def create_background(screen, width, height):
    colors = [(255, 255, 255), (212, 212, 212)]
    tile_width = TILE
    y = 0
    while y < height:
        x = 0
        while x < width:
            row = y // tile_width
            col = x // tile_width
            pygame.draw.rect(screen, colors[(row + col) % 2], pygame.Rect(x, y, tile_width, tile_width))
            x += tile_width
        y += tile_width


def draw_hud(screen, font, score, level):
    # Display current progress in the top-left corner.
    text = font.render(f"Score: {score}  Level: {level}", True, (0, 0, 0))
    screen.blit(text, (10, 10))


def draw_game_over_overlay(screen, font, score, level):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    title = font.render("Game Over", True, (255, 255, 255))
    details = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    controls = font.render("R - Restart    Q - Quit", True, (255, 255, 255))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(details, (WIDTH // 2 - details.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2 + 10))


def init_game_state():
    worm = Worm(TILE)
    food = Food(TILE)
    wall = Wall(TILE)
    score = 0
    eaten_food = 0
    fps = BASE_FPS

    # Spawn first food so it does not overlap snake or walls.
    food.respawn(worm.get_occupied_positions() | wall.get_occupied_positions(), WIDTH, HEIGHT)
    return worm, food, wall, score, eaten_food, fps


done = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

worm, food, wall, score, eaten_food, fps = init_game_state()
game_over = False

while not done:
    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                worm, food, wall, score, eaten_food, fps = init_game_state()
                game_over = False
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                done = True
        else:
            filtered_events.append(event)

    if not game_over:
        worm.process_input(filtered_events)
        worm.move()

        head = worm.get_head()

        # Enter game-over state on border, wall, or self collision.
        if head.X < 0 or head.Y < 0 or head.X >= WIDTH or head.Y >= HEIGHT:
            game_over = True

        if wall.is_collision(head) or worm.is_self_collision():
            game_over = True

        if food.can_eat(head):
            worm.increase()
            score += food.weight
            eaten_food += 1

            # New food must be on an empty cell.
            food.respawn(worm.get_occupied_positions() | wall.get_occupied_positions(), WIDTH, HEIGHT)

            # Every N foods, move to next level and increase speed.
            if eaten_food % FOODS_PER_LEVEL == 0 and wall.next_level():
                fps += 2
                food.respawn(worm.get_occupied_positions() | wall.get_occupied_positions(), WIDTH, HEIGHT)
        elif food.is_expired(pygame.time.get_ticks(), FOOD_LIFETIME_MS):
            # If food was not eaten in time, move it to another free cell.
            food.respawn(worm.get_occupied_positions() | wall.get_occupied_positions(), WIDTH, HEIGHT)

    create_background(screen, WIDTH, HEIGHT)

    food.draw(screen)
    wall.draw(screen)
    worm.draw(screen)
    draw_hud(screen, font, score, wall.get_level_number())
    if game_over:
        draw_game_over_overlay(screen, font, score, wall.get_level_number())

    pygame.display.flip()
    clock.tick(10 if game_over else fps)