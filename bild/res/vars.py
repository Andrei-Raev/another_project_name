from json import load

from lib.fps_clock import pygame, draw_fps_clock

# ---------- SETTINGS ----------
with open('settings.json', 'r') as settings_file:
    settings = load(settings_file)

# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
FULLSCREEN = False
MAP_COF = 1.3
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
WORLD_NOISE_SIZE = 50
BLOCK_SIZE = MAP_COF * 32

# ---------- VARIABLES ----------

fps = 60
clock = pygame.time.Clock()

# ---------- FPS CLOCK ----------
