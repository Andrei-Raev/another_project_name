from json import load

from lib.fps_clock import pygame, display_fps

# ---------- SETTINGS ----------
with open('settings.json', 'r') as settings_file:
    settings = load(settings_file)

SCALE_COF = 2
FULLSCREEN = False

# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
WORLD_NOISE_SIZE = 50

# ---------- VARIABLES ----------
fps = 60
clock = pygame.time.Clock()
map_cords = [0, 0]

# ---------- FPS CLOCK ----------
