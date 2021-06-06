# ---------- IMPORTS ----------
# Импорт системных библиотек
import os
import sys
import math
import time
import importlib.util
# from copy import copy
from copy import copy
from itertools import product

# Импорт сторонних библиотек
# from threading import Thread
from pprint import pprint

import PIL
from PIL import Image, ImageDraw, ImageColor
# from pygame.threads import Thread
from screeninfo import get_monitors

# Импорт элементов игры
from typing import List

from sample_classes import pause_break, inventory

import pygame

from work_dir.world_class.classes import CursObj, load_textures, Dress

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
# Генерация градиента
def gradient(col: int, col2: int, cof: float) -> int:
    return round(col * cof + col2 * (1 - cof))


# Масштабирование элементов интерфейса
def render_scale(val: int) -> int:
    return round(val * COF)


# Масштабирование карты
def map_scale(val: int) -> int:
    return round(val * MAP_COF)


# Собирает блок по координатам и весу точки: [-1, 1]
def block_constructor(cof: float, c_cords: tuple):
    if -0.5 <= cof <= 0.5:  # ----------------| Нормализует веса
        cof = cof * 1.8  # -------------------|
    else:  # ---------------------------------|
        if cof > 0:  # -----------------------|
            cof = (cof - 0.5) * 0.2 + 0.9  # -|
        else:  # -----------------------------|
            cof = (cof + 0.5) * 0.2 - 0.9  # -|

    cof += .25  # Осушает мир

    # Алгоритм генерации блока
    if cof <= 0:  # Уровень воды - 0. Если что-то ниже, это считается водой
        return Water(c_cords, round(20000 * abs(cof)))
    else:
        if 0 <= cof < 0.1:
            return Sand(c_cords)  # Пляж
        elif 0.1 <= cof < 0.35:
            return Grass(c_cords)  # Луга
        elif 0.35 <= cof < 0.5:
            return Grass(c_cords)  # Равнины
        elif 0.5 <= cof < 0.85:
            return Stone(c_cords)  # Горы
        else:
            return Stone(c_cords)  # Снег в горах


# Генерирует "случайный" сид, исходя из координат
def seed_from_cord(x: int, y: int) -> int:
    tmp = x << abs(y)
    if tmp.bit_length() < 16:
        return tmp
    else:
        while tmp.bit_length() > 16:
            tmp = round(tmp / 1000)
        return tmp


def save_s(surface):
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)
    image.show()  # save(f'saved.png')
    del strFormat, raw_str, image


def bright(surf: pygame.surface.Surface, brightness):
    image = Image.frombytes('RGBA', surf.get_size(), pygame.image.tostring(surf, 'RGBA', False))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))

            red = int(r * brightness)
            red = min(255, max(0, red))

            green = int(g * brightness)
            green = min(255, max(0, green))

            blue = int(b * brightness)
            blue = min(255, max(0, blue))

            image.putpixel((x, y), (red, green, blue, a))
    del r, g, b, a, red, green, blue, brightness
    return pygame.image.fromstring(image.tobytes("raw", 'RGBA'), image.size, 'RGBA')


def dark(surf: pygame.surface.Surface, brightness):
    image = Image.frombytes('RGBA', surf.get_size(), pygame.image.tostring(surf, 'RGBA', False))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))

            red = int(r // brightness)
            red = min(255, max(0, red))

            green = int(g // brightness)
            green = min(255, max(0, green))

            blue = int(b // brightness)
            blue = min(255, max(0, blue))

            image.putpixel((x, y), (red, green, blue, a))
    del r, g, b, a, red, green, blue, brightness
    return pygame.image.fromstring(image.tobytes("raw", 'RGBA'), image.size, 'RGBA')


def simple_chunk_texture_generation(chunk):
    tmp_ground = pygame.Surface((map_scale(510), map_scale(510)))
    tmp_ground.fill((0, 0, 0, 0))
    tmp_textures = []
    for i in chunk.board['landscape']:
        if type(i) == Water:
            tmp_textures.append([pygame.image.tostring(i.get_texture(), "RGBA", False),
                                 i.get_texture().get_rect(topleft=(tuple([j * 32 * MAP_COF for j in i.get_cord()]))),
                                 (2 * (i.water_level + 16000) / 20000)])
    if not len(tmp_textures):
        return
    for num, el in enumerate(tmp_textures):
        tmp_img = Image.frombytes("RGBA", (32, 32), el[0])
        tmp_img = dark(tmp_img, el[2])

    chunk.ground = tmp_ground


def get_relative_coordinates(x: int, y: int):
    x = (x % 16, x // 16)
    y = (y % 16, y // 16)
    return (x[0], y[0]), (x[1], y[1])


def split_sprites(path):
    res = []
    im = Image.open(path)
    for i in range(im.size[0] // 80):
        tmp_im = im.crop((i * 80, 0, (i + 1) * 80, im.size[1]))

        res.append(pygame.image.fromstring(tmp_im.tobytes("raw", 'RGBA'), tmp_im.size, 'RGBA').convert_alpha())
    return res


# ---------- PERLIN NOISE ----------
# Магия!!!
def smoothstep(t):
    return t * t * (3. - 2. * t)


def lerp(t, a, b):
    return a + t * (b - a)


class PerlinNoiseFactory(object):
    def __init__(self, dimension, octaves=1, seed=1, tile=(), unbias=False):
        self.dimension = dimension
        self.octaves = octaves
        self.tile = tile + (0,) * dimension
        self.unbias = unbias
        self.scale_factor = 2 * dimension ** -0.5
        self.random = noise_random
        self.seed = seed

        self.gradient = {}

    def _generate_gradient(self):
        if self.dimension == 1:
            return (self.random.uniform(-1, 1),)
        random_point = [self.random.gauss(0, 1) for _ in range(self.dimension)]
        scale = sum(n * n for n in random_point) ** -0.5
        return tuple(coord * scale for coord in random_point)

    def get_plain_noise(self, *point):
        if len(point) != self.dimension:
            raise ValueError("Expected {} values, got {}".format(
                self.dimension, len(point)))
        grid_coords = []
        for coord in point:
            min_coord = math.floor(coord)
            max_coord = min_coord + 1
            grid_coords.append((min_coord, max_coord))
        dots = []
        for grid_point in product(*grid_coords):
            if grid_point not in self.gradient:
                self.gradient[grid_point] = self._generate_gradient()
            gradient = self.gradient[grid_point]

            dot = 0
            for i in range(self.dimension):
                dot += gradient[i] * (point[i] - grid_point[i])
            dots.append(dot)
        dim = self.dimension
        while len(dots) > 1:
            dim -= 1
            s = smoothstep(point[dim] - grid_coords[dim][0])
            next_dots = []
            while dots:
                next_dots.append(lerp(s, dots.pop(0), dots.pop(0)))
            dots = next_dots
        return dots[0] * self.scale_factor

    def __call__(self, *point):
        ret = 0
        for o in range(self.octaves):
            o2 = 1 << o
            new_point = []
            for i, coord in enumerate(point):
                coord *= o2
                if self.tile[i]:
                    coord %= self.tile[i] * o2
                new_point.append(coord)
            ret += self.get_plain_noise(*new_point) / o2
        ret /= 2 - 2 ** (1 - self.octaves)

        if self.unbias:
            r = (ret + 1) / 2
            for _ in range(int(self.octaves / 2 + 0.5)):
                r = smoothstep(r)
            ret = r * 2 - 1

        return ret


# ---------- FPS CLOCK ----------
# Создание шрифта для счетчика fps
def create_fonts(font_sizes_list):
    fonts = []
    for size in font_sizes_list:
        fonts.append(pygame.font.SysFont("Arial", size))
    return fonts


# Рендер четчика fps
def render(fnt, what, color, where):
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


# Отображение четчика fps
def display_fps():
    render(fonts[0], what=str(int(clock.get_fps())), color="white", where=(0, 0))


# ---------- BLOCKS ----------

# -------------
# |   Блоки   |
# -------------

class Obekt:
    def __init__(self, cord: tuple, preor=0):
        self.cord = cord
        self.importance = preor

    def get_x(self) -> int:
        return int(self.cord[0])

    def get_y(self) -> int:
        return int(self.cord[1])

    def get_preor(self) -> int:
        return int(self.importance)

    def get_cord(self) -> tuple:
        return tuple(self.cord)


class Landscape(Obekt):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 0

    def get_texture(self):
        return TEXTURES['block'][self.get_type()]

    def get_super_texture(self):
        return TEXTURES['block'][self.get_type()]


class Grass(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 1


class Stone(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 2


class Sand(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 3


class Water(Landscape):
    def __init__(self, cord: tuple, water_level: int, importance=1):
        super().__init__(cord, importance)
        self.water_level = water_level

    @staticmethod
    def get_type() -> int:
        return 4

    def get_super_texture(self):
        cof = (2 * (self.water_level + 16000) / 20000)
        return dark(TEXTURES['block'][4], cof)


# -------------------
# |   Конец Блоки   |
# -------------------

# ---------- ENTITIES ----------
class Entity(pygame.sprite.Sprite):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):  #: pygame.AbstractGroup):
        super().__init__(*groups)

        self.hp = 100

        self.cords = cords
        try:
            self.image = texture['stand']
        except:
            self.image = texture
        self.textures = texture
        self.move_anim = 0
        self.rect = self.image.get_rect(center=self.cords)
        self.speed = ((32 * MAP_COF) * speed)
        self.isgoing = False
        self.rotate = False
        self.fly = False
        self.main_speed = ((32 * MAP_COF) * speed)
        self.counter = 0

    def move(self, delta_cords):
        self.cords = [self.cords[0] + delta_cords[0], self.cords[1] + delta_cords[1]]
        self.rect = self.image.get_rect(center=self.cords)

    def go(self, direct: int in [1, 2, 3, 4]):
        if direct == 1:
            self.move((0, self.speed // fps))
        elif direct == 2:
            self.move((0, -(self.speed // fps)))
        elif direct == 3:
            self.move((self.speed // fps, 0))
        elif direct == 4:
            self.move((-(self.speed // fps), 0))

    def get_cord(self, relative=True):
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        if relative:
            return get_relative_coordinates(x, y)
        else:
            return x, y

    def print_cord(self):
        global map_cords
        # print(tmp.center_chunk_cord)
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        return 'x = ' + str(x) + ', ' + 'y = ' + str(y)


class Item(Entity):
    def __init__(self, texture: list, cords: tuple, speed: float, item_info: list, *groups):
        super().__init__(texture, cords, speed, *groups)
        self.title = item_info[0]
        self.info = item_info

    def get_world_item(self):
        return self.textures, self.cords

    def render(self, surf, ccc):
        ccc1 = copy(ccc)
        ccc = ccc1[0] + 1, ccc1[1] + 1
        pygame.draw.circle(surf,(0,0,0), ((self.rect.x + ccc[0] * map_scale(510)), (self.rect.y + ccc[1] * map_scale(510))), 100)
        surf.blit(self.image, self.rect)
        print(self.rect)
        # save_s(surf)


class Player(Entity):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):

        super().__init__(texture, cords, speed, *groups)

        self.hp = 150
        self.max_hp = self.hp

        self.vitality = 500
        self.max_vitality = self.vitality

        self.vitality = 100
        self.wear_clothes = [Dress('Стандартный визер', TEXTURES['clothes']['viser'])]
        self.mode = 'stand'

    def tick(self):
        if self.vitality > self.max_vitality:
            self.vitality = self.max_vitality
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        self.fly = False
        self.isgoing = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotate = True
            if self.cords[0] > width - width // 5:
                map_cords[0] -= self.speed // fps
            else:
                self.go(3)

            self.isgoing = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotate = False
            if self.cords[0] < width // 5:
                map_cords[0] += self.speed // fps
            else:
                self.go(4)

            self.isgoing = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.cords[1] > height - height // 5:
                map_cords[1] -= self.speed // fps
            else:
                self.go(1)

            self.isgoing = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.cords[1] < height // 5:
                map_cords[1] += self.speed // fps
            else:
                self.go(2)

            self.isgoing = True

        if keys[pygame.K_LSHIFT]:
            self.fly = True

        if self.fly:
            self.mode = 'fly'

            self.vitality -= 1
            self.speed = self.main_speed * 1.3

            if self.move_anim > 9:
                self.move_anim = 0
            self.image = self.textures['fly'][self.move_anim]

            if self.counter > 3:
                self.move_anim += 1
                self.counter = 0
            self.counter += 1
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)

        elif not self.isgoing:
            self.mode = 'stand'

            self.vitality += 1
            if self.hp > 100:
                self.hp = 100

            self.image = self.textures['stand']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.vitality += 1
            self.mode = 'move'
            self.speed = self.main_speed

            self.counter += 1
            if self.counter == 2:
                self.move_anim += 1
                self.counter = 0
            elif self.counter > 3:
                self.counter = 0

            if self.rotate:
                self.image = pygame.transform.flip(self.textures['go'][self.move_anim - 1], True, False)
            else:
                self.image = self.textures['go'][self.move_anim - 1]

            if self.move_anim > 15:
                self.move_anim = 0
                self.isgoing = False

        if tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Water' and not self.fly:
            self.mode = 'swim'
            self.speed = self.main_speed * 0.6
            self.image = self.textures['swim']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        elif tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Stone':
            pass
        self.image = copy(self.image)
        for item in self.wear_clothes:
            item.render(self.image, self.mode, self.move_anim, self.rotate)
        # else:
        #    self.speed = 7
        # self.image.fill((0, 0, 0))

    def get_texture(self) -> pygame.surface.Surface:
        image = self.textures['stand']

        image = copy(image)
        for item in self.wear_clothes:
            item.render(image, self.mode, self.move_anim, self.rotate)

        return image


class ProgressBar:
    def __init__(self, surf: pygame.surface.Surface, border: int, border_radius: int, progress: int, max_progress=100):
        self.color = (243, 246, 250)
        self.border_radius = border_radius
        self.border_color = (0, 22, 87)
        self.x = 0
        self.y = 0
        self.height = surf.get_height()
        self.width = surf.get_width()
        self.surf = surf
        self.border_width = border
        self.progress = progress
        self.max_progress = max_progress
        self.bg_color = (0, 0, 34)

        # self.cords = (0, 0)

        # self.anim_hover = 0

        # self.on_click_set = [[False], [False], [False]]

    def draw(self, *_):
        pygame.draw.rect(self.surf, self.border_color,
                         (0, 0, self.surf.get_width(), self.surf.get_height()), 0, self.border_radius)
        pygame.draw.rect(self.surf, self.bg_color,
                         (self.border_width, self.border_width, self.width - self.border_width * 2,
                          self.height - self.border_width * 2), 0, self.border_radius)
        len_prog = (self.width + self.border_width * 2) // self.max_progress * self.progress  # Хрень
        if self.progress == self.max_progress:
            len_prog = self.width - self.border_width * 2
        if self.progress:
            pygame.draw.rect(self.surf, self.color,
                             (self.border_width, self.border_width, len_prog, self.height - self.border_width * 2), 0,
                             self.border_radius)

    def set_progress(self, val: int):
        if self.max_progress < val:
            raise ValueError(f'value ({val}) > max progress ({self.max_progress})')
        elif val < 0:
            raise ValueError(f'value less than zero ({val})')

        self.progress = val

    def add_progress(self, val: int):
        self.progress += val
        if self.progress < 0:
            self.progress = 0
        elif self.progress > self.max_progress:
            self.progress = self.max_progress


#
#
#
#


class Indicator(pygame.sprite.Sprite):
    def __init__(self, player: Player, *groups):
        super().__init__(*groups)

        tmp_im = Image.open('res/image/entities/player/main.png').transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image = Image.new("RGBA", tmp_im.size, (255, 255, 250, 255))
        image.alpha_composite(tmp_im)
        image = image.crop((round(image.size[0] * .35), round(image.size[1] * .3),
                            round(image.size[0] * .75), round(image.size[1] * .7)))
        # Рисование
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, *image.size), outline=(0, 22, 87, 255), width=2)

        image = (pygame.image.fromstring(image.tobytes("raw", "RGBA"), image.size, "RGBA"))
        self.avator = pygame.transform.scale(image, [i * 2 for i in image.get_size()])
        self.main_image = pygame.surface.Surface((self.avator.get_size()[0] * 3, self.avator.get_size()[1]))
        self.main_image.fill((10, 0, 0))
        self.main_image.set_colorkey((10, 0, 0))
        self.main_image.convert_alpha()
        self.main_image.fill((0, 22, 87, 100))

    def update(self, player: Player, *args, **kwargs) -> None:
        self.image = copy(self.main_image)
        self.image.blit(self.avator, (0, 0))

        pygame.draw.rect(self.image, (200, 10, 10),
                         (self.image.get_width() - self.avator.get_width() * 2, self.image.get_height() / 3 - 7,
                          self.image.get_width() + self.image.get_width() * (player.hp / player.max_hp) * 0 - 130, 15))
        pygame.draw.rect(self.image, (224, 220, 0),
                         (self.image.get_width() - self.avator.get_width() * 2,
                          self.image.get_height() - self.image.get_height() / 3 - 7,
                          self.image.get_width() * (player.vitality / player.max_vitality) - 130,
                          15))
        print(player.vitality / player.max_vitality, player.vitality)

    def render(self, surf):
        surf.blit(self.image, (width * .06, height * .06))

    def save_s(self):
        save_s(self.image)


# ---------- WORLD ----------
class UI:
    def __init__(self, max_hp):
        self.indicator = Indicator(pl)

        self.curs = [CursObj()]

    def render(self, surf: pygame.surface.Surface, _):
        # self.hp_bar.set_progress(hp)
        # self.hp_bar.draw()
        # surf.blit(self.hp_bar.surf, (width - width // 4.5, height // 30))

        self.indicator.update(pl)
        self.indicator.render(surf)

        for obj in self.curs:
            obj.render(surf)


class World:  # Класс мира
    def __init__(self, world_seed, center_chunk_cord, seed):
        self.world_seed = world_seed
        self.chunks = set()
        self.center_chunk_cord = center_chunk_cord
        noise_random.seed(seed)
        self.noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=seed)

    def init(self):
        for y in range(-1, 2):
            for x in range(-1, 3):
                self.chunks.add(
                    Chunk(seed_from_cord(x, y), (x + self.center_chunk_cord[0], y + self.center_chunk_cord[1])))

        for i in self.chunks:
            i.generate_chunk(self.noise)
            # i.load()
            i.render_chunk()

    def add_chunk(self, cord):
        self.chunks.add(Chunk(seed_from_cord(*cord), cord))

    def del_chunk(self, cord):
        for i in self.chunks:
            if i.get_cord() == cord:
                self.chunks.remove(i)
                break

    def render(self, surf):
        wid = 510 * MAP_COF
        tmp_world_surf = pygame.Surface((map_scale(510) * 4, map_scale(510) * 3))
        tmp_items = list()

        for y in range(-1 + self.center_chunk_cord[1], 3 + self.center_chunk_cord[1]):
            for x in range(-1 + self.center_chunk_cord[0], 2 + self.center_chunk_cord[0]):
                chunk_cord = tuple([x, y])
                try:
                    chunk_surf = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_s()
                    tmp_items += list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_items()
                except IndexError:
                    # raise ValueError(f'Chunk ({chunk_cord}) not found!')
                    self.chunks.add(Chunk(seed_from_cord(*chunk_cord), chunk_cord))
                    tmp_chunk = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0]
                    tmp_chunk.generate_chunk(self.noise)
                    tmp_chunk.render_chunk()
                    chunk_surf = tmp_chunk.get_s()
                    # save_s(chunk_surf)

                tmp_world_surf.blit(chunk_surf, ((chunk_cord[1] - self.center_chunk_cord[1]) * wid + wid,
                                                 (chunk_cord[0] - self.center_chunk_cord[0]) * wid + wid))

        for item in tmp_items:
            item.render(tmp_world_surf, self.center_chunk_cord)
            #print(item)
            #tmp_world_surf.fill((0,0,0))

        surf.blit(tmp_world_surf, [i - map_scale(510) for i in map_cords])

    def get_block(self, cords):
        try:
            block_cord, chunk_cord = get_relative_coordinates(*cords)
            tmp_chunk = list(filter(lambda x: x.get_cord() == chunk_cord[::-1], self.chunks))[0]
            tmp_block = list(filter(lambda x: x.get_cord() == block_cord, tmp_chunk.board['landscape']))[0]
            return tmp_block
        except IndexError:
            return None

    def add_item(self, item: Item):
        chunk_cord = item.get_cord()[1]
        tmp_chunk = list(filter(lambda x: x.get_cord() == chunk_cord, self.chunks))[0]
        tmp_chunk.board['entities']['items'].add(item)

    def move_visible_area(self, direction: int):  # 1 - вверх, 2 - вниз, 3 - влево, 4 - вправо
        if direction == 1:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] + 1)
        elif direction == 2:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] - 1)
        elif direction == 3:
            self.center_chunk_cord = (self.center_chunk_cord[0] + 1, self.center_chunk_cord[1])
        elif direction == 4:
            self.center_chunk_cord = (self.center_chunk_cord[0] - 1, self.center_chunk_cord[1])

    def load_world(self, file):
        pass

    def save_world(self):
        for i in self.chunks:
            i.save(f'save_data/{i.get_cord()}.ch')

    def get_world(self):
        q = []
        for i in range(len(self.chunks) * 2):
            q.append([])
        for i in self.chunks:
            i = str(i)
            for g in range(16):
                for j in range(16):
                    if 'Water' in i.split(', ')[g * j]:
                        q[g].append(1)
                    else:
                        q[g].append(0)
        return q


class Chunk:  # Класс чанка мира
    def __init__(self, seed: int, cord: (int, int)):
        self.seed = seed
        self.cord = cord

        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {'items': {}}}
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))

    def generate_chunk(self, world_noise) -> None:
        del self.board
        self.board = {'landscape': set(), 'buildings': set(), 'mechanisms': {}, 'entities': {'items': set()}}
        for y in range(16):
            for x in range(16):
                tmp_noise = world_noise((x + (self.cord[1]) * 16) / WORLD_NOISE_SIZE,
                                        (y + (self.cord[0]) * 16) / WORLD_NOISE_SIZE)
                self.board['landscape'].add(block_constructor(tmp_noise, (x, y)))

    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))
        self.ground.fill((55, 5, 4))
        for i in self.board['landscape']:
            cord = i.get_cord()
            tmp_texture = i.get_texture()
            block_rect = tmp_texture.get_rect(topleft=(tuple([j * 32 * MAP_COF for j in cord])))
            self.ground.blit(tmp_texture, block_rect)
            del cord, i, block_rect
        # simple_chunk_texture_generation(self)

        # f = pygame.font.Font(None, 100)
        # r = f.render(f'{self.cord}', True,(255,255,255))
        # self.ground.blit(r, (50,50))

        # f = pygame.font.Font(None, 250)
        # t = f.render(f'{self.cord}', True, (255, 255, 255))
        # self.ground.blit(t, (25, 25))

    def get_items(self) -> list:
        return self.board['entities']['items']

    def get_s(self):
        return self.ground

    def get_cord(self):
        return tuple(self.cord)

    def __str__(self):
        return str(self.board['landscape'])

    def load(self):
        self.board = decode_chunk(self.cord)

    def update(self, data):
        pass

    def save(self, name_f):
        raw = b''

        for i in self.board['landscape']:
            raw += i.get_type().to_bytes(1, byteorder="little")
            raw += cord_codec(i.get_cord())

        with open(name_f, 'wb') as byte_file:
            byte_file.write(raw)


def cord_codec(cors: tuple) -> bytes:
    raw = b''
    for i in cors:
        raw += i.to_bytes(1, byteorder="little")
    return raw


def decode_chunk(file_path):
    board = {'landscape': set()}
    with open(f'save_data/{file_path}.ch', 'rb') as byte_file:
        chunk_raw = byte_file.read()
        for i in range(len(chunk_raw) // 3):
            tmp_type = chunk_raw[i * 3]
            tmp_cord_x = int.from_bytes(chunk_raw[i * 3 + 1:i * 3 + 2], 'little')
            tmp_cord_y = int.from_bytes(chunk_raw[i * 3 + 2:i * 3 + 3], 'little')
            if tmp_type == 1:
                board['landscape'].add(Grass((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 2:
                board['landscape'].add(Stone((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 3:
                board['landscape'].add(Sand((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 4:
                board['landscape'].add(Water((tmp_cord_x, tmp_cord_y), 20000))
    return board


# Таймер для подсчета работы кода
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
FULLSCREEN = False
MAP_COF = 1.3
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
WORLD_NOISE_SIZE = 50
BLOCK_SIZE = MAP_COF * 32

# ---------- VARIABLES ----------
fonts = create_fonts([32, 16, 14, 8])
map_cords = [0, 0]
fps = 60
clock = pygame.time.Clock()

# ---------- INIT ----------
if FULLSCREEN:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('World')
pygame.mouse.set_cursor((16, 16), (0, 0), (
    135, 135, 135, 135, 135, 41, 41, 41, 41, 41, 41, 41, 41, 135, 122, 135, 41, 41, 41, 41, 41, 41, 41, 41, 135, 110,
    116,
    41, 41, 41, 41, 41), (64, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 128, 254, 0,
                          239,
                          0, 79, 0, 7, 128, 7, 128, 3, 0))

# ---------- TEXTURES ----------
# Загрузка текстур фундаментальных блоков
tmp_block_textures = [pygame.image.load('res/image/block/none.jpg').convert(), pygame.image.load(
    'res/image/block/grass.png').convert(),
                      pygame.image.load('res/image/block/stone.png').convert(),
                      pygame.image.load('res/image/block/sand.png').convert(), pygame.image.load(
        'res/image/block/water.png').convert()]
for num, el in enumerate(tmp_block_textures):
    tmp_block_textures[num] = pygame.transform.scale(el, (map_scale(32), map_scale(32)))

# Загрузка текстур сущьностей
tttt = Image.open('res/image/entities/player/main.png')
tmp_player_textures = {
    "stand": pygame.transform.scale(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
                                    [round(x * MAP_COF * 1.3) for x in tttt.size])}

tttt = Image.open('res/image/entities/player/swim.png')
tmp_player_textures.update({
    "swim": pygame.transform.scale(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
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

tmp_clothes_textures = {}

for texture in os.listdir(r'res\image\clothes'):
    tmp_clothes_textures.update({texture: load_textures(r"res/image/clothes/" + texture, MAP_COF)})
# Общая сборка
TEXTURES = {'block': tmp_block_textures,
            'player': tmp_player_textures,
            'none': pygame.image.load('res/image/block/none.jpg').convert(),
            'clothes': tmp_clothes_textures}
# save_s(TEXTURES['player']['stand'])
# ---------- WORK SPASE ----------
pl = Player(TEXTURES['player'], (width // 2, height // 2), 7)
frame_pass, frame_counter = True, False

start_time_m = time.time()
tmp = World(0, (0, 0), 10)
# noise_random.seed(10)

# pprint(TEXTURES['clothes']["viser"])
# hren = list()
# for i in pygame.image.tostring(pygame.image.load('res/image/clothes/viser/item.png').convert(), "RGB", False)[::3]:
#     hren.append(i)
#     print(pygame.image.load('res/image/clothes/viser/item.png').convert().get_size())
# from pyperclip import copy as cop
# cop(str(tuple(hren)))
tmp.init()
tmp.add_item(Item(pygame.image.load(r'res\image\items\0025.jpg').convert_alpha(), (10, 10), 0, ['fsdf', 'afsdf']))
ui = UI(100)
# tmp.save_world()
print("--- %s seconds --- MAIN" % (time.time() - start_time_m))
print(len(tmp.get_world()))
for i in tmp.get_world():
    print(i)
if __name__ == '__main__':

    player_state = Indicator(pl)
    # player_state.save_s()

    main_running = True
    while main_running:
        # pl.print_cord()
        # world_noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=random.randint(1, 55))
        # tmp = World(0, (0, 0))
        # tmp.init()
        # raise Exception("hui")

        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                main_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    pause_break.pause()
                    # tmp.move_visible_area(3)
                elif event.key == pygame.K_TAB:
                    inventory.inventory([it.get_item() for it in pl.wear_clothes])
            elif event.type == pygame.MOUSEMOTION:
                pass
                # pl.move(event.rel)
        xx = pl.cords[0]
        yy = pl.cords[1]

        if map_cords[0] < -map_scale(510):
            tmp.move_visible_area(1)
            map_cords[0] += map_scale(510)

        elif map_cords[0] > map_scale(510):
            tmp.move_visible_area(2)
            map_cords[0] -= map_scale(510)

        if map_cords[1] < -map_scale(510):
            tmp.move_visible_area(3)
            map_cords[1] += map_scale(510)

        elif map_cords[1] > map_scale(510):
            tmp.move_visible_area(4)
            map_cords[1] -= map_scale(510)

        pl.tick()

        # Рендер основного окна
        if frame_pass:
            if frame_counter:
                screen.fill((47, 69, 56))
                tmp.render(screen)
                screen.blit(pl.image, pl.rect)
                display_fps()
                # a = pygame.font.Font(None, 35)
                # a = a.render(str(pl.print_cord()), True, (250, 255, 255))
                # screen.blit(a, (10, 690))
                ui.render(screen, pl.hp)
                pygame.display.flip()
            frame_counter = not frame_counter
            clock.tick(fps)

    pygame.quit()  # Завершение работы

# Эта версия
