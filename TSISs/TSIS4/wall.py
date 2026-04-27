import pygame
import os
import random
from game_object import GameObject
from game_object import Point


class Wall(GameObject):
    def __init__(self, tile_width):
        super().__init__([], (255, 0, 0), tile_width)
        self.level_files = self._collect_level_files()
        self.level = 0
        self.static_points = []
        self.dynamic_points = []
        self.load_level()

    def _collect_level_files(self):
        levels_dir = os.path.join(os.path.dirname(__file__), "levels")
        level_files = [
            filename
            for filename in os.listdir(levels_dir)
            if filename.startswith("level") and filename.endswith(".txt")
        ]
        # Sort files like level0.txt, level1.txt, level2.txt by numeric suffix.
        level_files.sort(key=lambda name: int("".join(ch for ch in name if ch.isdigit()) or 0))
        return [os.path.join(levels_dir, filename) for filename in level_files]

    def load_level(self):
        self.static_points = []
        self.dynamic_points = []

        if not self.level_files:
            self.points = []
            return

        file_index = min(self.level, len(self.level_files) - 1)
        with open(self.level_files[file_index], "r", encoding="utf-8") as level_file:
            for row, line in enumerate(level_file):
                for col, c in enumerate(line.rstrip("\n")):
                    # "#" marks a wall cell in level text files.
                    if c == '#':
                        self.static_points.append(Point(col * self.tile_width, row * self.tile_width))

        self._rebuild_points()

    def _rebuild_points(self):
        self.points = self.static_points + self.dynamic_points

    def _generate_dynamic_obstacles(self, snake_positions, snake_head, width, height):
        self.dynamic_points = []
        if self.get_level_number() < 3:
            self._rebuild_points()
            return

        target_count = min(14, 3 + (self.get_level_number() - 3) * 2)
        static_positions = {(point.X, point.Y) for point in self.static_points}

        protected = {
            (snake_head.X, snake_head.Y),
            (snake_head.X + self.tile_width, snake_head.Y),
            (snake_head.X - self.tile_width, snake_head.Y),
            (snake_head.X, snake_head.Y + self.tile_width),
            (snake_head.X, snake_head.Y - self.tile_width),
        }

        blocked = set(static_positions)
        blocked.update(snake_positions)
        blocked.update(protected)

        candidates = []
        for x in range(0, width, self.tile_width):
            for y in range(0, height, self.tile_width):
                if (x, y) not in blocked:
                    candidates.append((x, y))

        random.shuffle(candidates)
        chosen = candidates[:target_count]
        self.dynamic_points = [Point(x, y) for x, y in chosen]
        self._rebuild_points()

    def next_level(self, snake_positions, snake_head, width, height):
        self.level += 1
        self.load_level()
        self._generate_dynamic_obstacles(snake_positions, snake_head, width, height)
        return True

    def refresh_obstacles(self, snake_positions, snake_head, width, height):
        self._generate_dynamic_obstacles(snake_positions, snake_head, width, height)

    def get_level_number(self):
        return self.level + 1

    def is_collision(self, point):
        return any(point.X == wall.X and point.Y == wall.Y for wall in self.points)

    def get_occupied_positions(self):
        return {(point.X, point.Y) for point in self.points}