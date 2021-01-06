import pygame
from script_dir import script_dir
class Settings:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.music_on = True
        self.bg = pygame.image.load(script_dir + 'images\Bg\Bg.png')

