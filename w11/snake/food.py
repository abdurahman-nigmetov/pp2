import pygame
import random
from game_object import GameObject
from game_object import Point


class Food(GameObject):
    def __init__(self, tile_width):
        self.weight = random.randint(1, 3)
        color = self._set_color(self.weight)
        super().__init__([Point(120, 20)], color, tile_width)
        self.spawned_at = pygame.time.get_ticks()

    # Setting color to the food based on the weight
    def _set_color(self, color_num):
        if color_num == 1:
            self.color = (0, 255, 0)
        elif color_num == 2:
            self.color = (255, 255, 0)
        else:
            self.color = (255, 165, 0)
        return self.color

    def can_eat(self, head_location):
        point = self.points[0]
        return point.X == head_location.X and point.Y == head_location.Y

    def respawn(self, blocked_positions, width, height):
        available_positions = []

        # Build a list of free grid cells for food placement.
        for x in range(0, width, self.tile_width):
            for y in range(0, height, self.tile_width):
                if (x, y) not in blocked_positions:
                    available_positions.append((x, y))

        if not available_positions:
            return False

        x, y = random.choice(available_positions)
        self.points = [Point(x, y)]
        self.weight = random.randint(1, 3)
        self._set_color(self.weight)
        self.spawned_at = pygame.time.get_ticks()
        return True

    def is_expired(self, current_ticks, lifetime_ms):
        return current_ticks - self.spawned_at >= lifetime_ms