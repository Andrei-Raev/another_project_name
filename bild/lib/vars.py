"""Собирает базовые значения, используемые в игре и подготавливает ее к запуску, что бы не нагружать основной код"""
from json import load

from lib.fps_clock import pygame, display_fps

# ---------- SETTINGS ----------
with open('settings.json', 'r') as settings_file:
    settings = load(settings_file)

SCALE_COF = settings['scale']
FULLSCREEN = settings['fullscreen']
SHOW_FPS = settings['show_fps']

# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
WORLD_NOISE_SIZE = 50

# ---------- VARIABLES ----------
fps = 60
clock = pygame.time.Clock()
map_cords = [0, 0]

# ---------- FPS CLOCK ----------
