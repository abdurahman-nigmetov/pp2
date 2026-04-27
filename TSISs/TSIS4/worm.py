import pygame
from game_object import GameObject
from game_object import Point


class Worm(GameObject):
    def __init__(self, tile_width):
        super().__init__([Point(20, 20)], (0, 0, 255), tile_width)
        self.DX = 1
        self.DY = 0
        self.pending_growth = 0

    def move(self):
        old_tail = Point(self.points[-1].X, self.points[-1].Y)

        for i in range(len(self.points) - 1, 0, -1):
            self.points[i].X = self.points[i - 1].X
            self.points[i].Y = self.points[i - 1].Y

        self.points[0].X += self.DX * self.tile_width
        self.points[0].Y += self.DY * self.tile_width

        # Grow by adding previous tail position after moving forward.
        if self.pending_growth > 0:
            self.points.append(old_tail)
            self.pending_growth -= 1

    def increase(self):
        self.pending_growth += 1

    def decrease(self, amount=2):
        removable = min(max(0, int(amount)), max(0, len(self.points) - 1))

        if removable == 0:
            return len(self.points)

        self.pending_growth = max(0, self.pending_growth - removable)
        for _ in range(removable):
            self.points.pop()

        return len(self.points)

    def set_color(self, rgb):
        self.color = tuple(rgb)

    def get_head(self):
        return self.points[0]

    def get_occupied_positions(self):
        return {(point.X, point.Y) for point in self.points}

    def is_self_collision(self):
        head = self.get_head()
        return any(
            head.X == body_part.X and head.Y == body_part.Y
            for body_part in self.points[1:]
        )

    def process_input(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            new_dx, new_dy = self.DX, self.DY

            if event.key == pygame.K_UP:
                new_dx, new_dy = 0, -1
            elif event.key == pygame.K_DOWN:
                new_dx, new_dy = 0, 1
            elif event.key == pygame.K_RIGHT:
                new_dx, new_dy = 1, 0
            elif event.key == pygame.K_LEFT:
                new_dx, new_dy = -1, 0

            # Prevent direct 180-degree turn when snake has body.
            if len(self.points) > 1 and (new_dx, new_dy) == (-self.DX, -self.DY):
                continue

            self.DX, self.DY = new_dx, new_dy