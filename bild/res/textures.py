"""Загрузка текстур игры
Импортировать отсюда константу с текстурами TEXTURES"""

# ---------- TEXTURES ----------
# Загрузка текстур фундаментальных блоков
import os

import pygame
from PIL import Image
from screeninfo import get_monitors

from lib.base_func import split_gorisontal_sprites
from lib.vars import FULLSCREEN, SCALE_COF

os.chdir('res')
pygame.init()

if FULLSCREEN:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    render_screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    SCALE_COF = width / 320
else:
    size = width, height = 320 * SCALE_COF, 180 * SCALE_COF
    render_screen = pygame.display.set_mode(size)


def load_textures(direct):
    textures = {}
    for im in os.listdir(direct):
        if im == 'item.png':
            tmp_el = pygame.image.load(direct + '/' + im)
            textures.update({im[:-4]: [tmp_el]})
        else:
            textures.update({im[:-4]: split_gorisontal_sprites(direct + '/' + im)})
    return textures


tmp_block_textures = [pygame.image.load('textures/block/none.jpg').convert(), pygame.image.load(
    'textures/block/grass.png').convert(),
                      pygame.image.load('textures/block/stone.png').convert(),
                      pygame.image.load('textures/block/sand.png').convert(), pygame.image.load(
        'textures/block/water.png').convert()]
"""
# Загрузка текстур сущьностей
tttt = Image.open('res/image/entities/player/main.png')
tmp_player_textures = {
    "stand": pygame.transform.scale(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
                                    [round(x * MAP_COF * 1.3) for x in tttt.size])}

tttt = Image.open('res/image/entities/player/swim.png')
tmp_player_textures.update({
    "swim": pygame.transform.c(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
                                   [round(x * MAP_COF * 1.3) for x in tttt.size])})

tmp_player_move_textures = {"go": []}
for num, el in enumerate(split_sprites('res/image/entities/player/move.png')):
    tmp_player_move_textures['go'].append(pygame.transform.scale(el, [round(x * MAP_COF * 1.3) for x in el.get_size()]))
tmp_player_textures.update(tmp_player_move_textures)

tmp_player_move_textures = {"fly": []}
for num, el in enumerate(split_sprites('res/image/entities/player/fly.png')):
    tmp_player_move_textures['fly'].append(
        pygame.transform.scale(el, [round(x * MAP_COF * 1.3) for x in el.get_size()]))
tmp_player_textures.update(tmp_player_move_textures)
"""
tmp_clothes_textures = {}

for texture in os.listdir(r'textures\clothes'):
    tmp_clothes_textures.update({texture: load_textures(r"textures/clothes/" + texture)})

tmp_ui_textures = {}
tmp_ui_textures.update({'hud': pygame.image.load('textures/gui/hud.png').convert()})

# Общая сборка
TEXTURES = {'block': tmp_block_textures,
            'ui': tmp_ui_textures,
            # 'player': tmp_player_textures,
            'none': pygame.image.load('textures/block/none.jpg').convert(),
            'clothes': tmp_clothes_textures}

os.chdir('..')
