import pygame
import os
from game_object import GameObject
from game_object import Point


class Wall(GameObject):
    def __init__(self, tile_width):
        super().__init__([], (255, 0, 0), tile_width)
        self.level_files = self._collect_level_files()
        self.level = 0
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
        self.points = []
        if not self.level_files:
            return

        with open(self.level_files[self.level], "r", encoding="utf-8") as level_file:
            for row, line in enumerate(level_file):
                for col, c in enumerate(line.rstrip("\n")):
                    # "#" marks a wall cell in level text files.
                    if c == '#':
                        self.points.append(Point(col * self.tile_width, row * self.tile_width))

    def next_level(self):
        if self.level >= len(self.level_files) - 1:
            return False

        self.level += 1
        self.load_level()
        return True

    def get_level_number(self):
        return self.level + 1

    def is_collision(self, point):
        return any(point.X == wall.X and point.Y == wall.Y for wall in self.points)

    def get_occupied_positions(self):
        return {(point.X, point.Y) for point in self.points}