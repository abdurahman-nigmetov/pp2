import os
import pygame


class MusicPlayer:
    def __init__(self, tracks):
        self.tracks = tracks
        self.current_index = 0
        self.is_playing = False

        if not self.tracks:
            raise ValueError("Playlist is empty")

        self.load_current_track()

    def load_current_track(self):
        pygame.mixer.music.load(self.tracks[self.current_index])

    def play(self):
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.load_current_track()
        self.play()

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.load_current_track()
        self.play()

    def get_current_track_name(self):
        return os.path.basename(self.tracks[self.current_index])

    def get_status(self):
        return "Playing" if self.is_playing else "Stopped"

    def get_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms // 1000