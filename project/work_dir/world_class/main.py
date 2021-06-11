# ---------- IMPORTS ----------
# Импорт библиотек
import os
import sys
import math
import time
import importlib.util
# from copy import copy
from copy import copy
from itertools import product
# from threading import Thread
from pprint import pprint
import PIL
from PIL import Image, ImageDraw, ImageColor
# from pygame.threads import Thread
from screeninfo import get_monitors
from typing import List
from project.sample_classes import pause_break, inventory
import pygame
from project.work_dir.world_class.classes import CursObj, load_textures, Dress

pygame.init()

# Создание 2 рандомов (для генерации шума и для прочих целей)
RAND = importlib.util.find_spec('random')
noise_random = importlib.util.module_from_spec(RAND)
RAND.loader.exec_module(noise_random)
sys.modules['noise_random'] = noise_random

random = importlib.util.module_from_spec(RAND)
RAND.loader.exec_module(random)
sys.modules['random'] = random
del RAND


# random.seed(1)

# ---------- FUNCTIONS ----------


# Масштабирование элементов интерфейса
def render_scale(val: int) -> int:
    return round(val * COF)


# Масштабирование карты
def map_scale(val: int) -> int:
    return round(val * MAP_COF)

# Эта версия
