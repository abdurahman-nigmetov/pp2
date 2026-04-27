import pygame
import random
from game_object import GameObject
from game_object import Point


def _choose_free_cell(blocked_positions, width, height, tile_width):
    available_positions = []

    for x in range(0, width, tile_width):
        for y in range(0, height, tile_width):
            if (x, y) not in blocked_positions:
                available_positions.append((x, y))

    if not available_positions:
        return None

    return random.choice(available_positions)


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
        cell = _choose_free_cell(blocked_positions, width, height, self.tile_width)
        if not cell:
            return False

        x, y = cell
        self.points = [Point(x, y)]
        self.weight = random.randint(1, 3)
        self._set_color(self.weight)
        self.spawned_at = pygame.time.get_ticks()
        return True

    def is_expired(self, current_ticks, lifetime_ms):
        return current_ticks - self.spawned_at >= lifetime_ms


class PoisonFood(GameObject):
    def __init__(self, tile_width):
        super().__init__([], (139, 0, 0), tile_width)

    def can_eat(self, head_location):
        if not self.points:
            return False

        point = self.points[0]
        return point.X == head_location.X and point.Y == head_location.Y

    def respawn(self, blocked_positions, width, height):
        cell = _choose_free_cell(blocked_positions, width, height, self.tile_width)
        if not cell:
            self.points = []
            return False

        x, y = cell
        self.points = [Point(x, y)]
        return True


class PowerUp(GameObject):
    COLORS = {
        "speed": (75, 221, 255),
        "slow": (129, 199, 132),
        "shield": (255, 202, 40),
    }

    def __init__(self, tile_width):
        super().__init__([], (255, 255, 255), tile_width)
        self.kind = None
        self.spawned_at = 0

    def clear(self):
        self.points = []
        self.kind = None
        self.spawned_at = 0

    def can_collect(self, head_location):
        if not self.points:
            return False

        point = self.points[0]
        return point.X == head_location.X and point.Y == head_location.Y

    def is_on_field(self):
        return bool(self.points)

    def is_expired(self, current_ticks, lifetime_ms):
        if not self.points:
            return False
        return current_ticks - self.spawned_at >= lifetime_ms

    def spawn(self, blocked_positions, width, height, current_ticks):
        cell = _choose_free_cell(blocked_positions, width, height, self.tile_width)
        if not cell:
            self.clear()
            return False

        self.kind = random.choice(["speed", "slow", "shield"])
        self.color = self.COLORS[self.kind]
        x, y = cell
        self.points = [Point(x, y)]
        self.spawned_at = current_ticks
        return True