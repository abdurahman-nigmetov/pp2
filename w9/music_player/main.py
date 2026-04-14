import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 700
HEIGHT = 300
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (100, 200, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

tracks = [
    "music/sample_tracks/sample-6s.mp3",
    "music/sample_tracks/sample-9s.mp3",
    "music/sample_tracks/sample-12s.mp3",
]

player = MusicPlayer(tracks)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                running = False

    screen.fill(BG_COLOR)

    title_text = font.render("Music Player", True, ACCENT_COLOR)
    track_text = small_font.render(
        f"Current track: {player.get_current_track_name()}",
        True,
        TEXT_COLOR
    )
    status_text = small_font.render(
        f"Status: {player.get_status()}",
        True,
        TEXT_COLOR
    )
    position_text = small_font.render(
        f"Position: {player.get_position_seconds()} sec",
        True,
        TEXT_COLOR
    )
    controls_text = small_font.render(
        "P=Play  S=Stop  N=Next  B=Back  Q=Quit",
        True,
        TEXT_COLOR
    )

    screen.blit(title_text, (40, 30))
    screen.blit(track_text, (40, 100))
    screen.blit(status_text, (40, 140))
    screen.blit(position_text, (40, 180))
    screen.blit(controls_text, (40, 230))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()