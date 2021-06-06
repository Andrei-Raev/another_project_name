# ---------- IMPORTS ----------
# Импорт системных библиотек
import sys
import math
import time
import importlib.util

# Импорт сторонних библиотек
# from threading import Thread
from copy import copy
from datetime import datetime

from PIL import Image, ImageFilter
from pygame.threads import Thread
from screeninfo import get_monitors

import pygame

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
    image.save(f'test/{round(random.random(), 20)}.png')
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


def get_relative_coordinates(x: int, y: int):
    x = (x % 16, x // 16)
    y = (y % 16, y // 16)
    return (x[0], y[0]), (x[1], y[1])


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


def blur(surface, rad):
    size = surface.get_size()
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)

    image = image.filter(ImageFilter.BoxBlur(rad))

    raw_str = image.tobytes("raw", strFormat)
    result = pygame.image.fromstring(raw_str, image.size, strFormat)
    del size, strFormat, raw_str, image
    return result


def antialiasing(surface, size_cof):
    size = surface.get_size()
    size = [i // size_cof for i in size]
    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)

    image = image.resize(size, resample=Image.ANTIALIAS)

    raw_str = image.tobytes("raw", strFormat)
    result = pygame.image.fromstring(raw_str, image.size, strFormat)
    del size, strFormat, raw_str, image
    return result


class Item(pygame.sprite.Sprite):
    def __init__(self, texture: pygame.image, title: str, description: str, cords: tuple, *groups):
        super().__init__(*groups)
        self.title = title
        self.description = description
        self.cords = cords
        self.image = texture
        self.is_grab = False
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.speed = 3
        self.abs_cords = (0, 0)

    def move_to_cords(self, *cordss):
        distance = math.sqrt((cordss[0] - self.abs_cords[0]) ** 2 + (cordss[1] - self.abs_cords[1]) ** 2)

        tmp_x = self.abs_cords[0] - cordss[0]
        tmp_y = self.abs_cords[1] - cordss[1]
        try:
            angel = tmp_x / tmp_y
        except ZeroDivisionError:
            return cordss
        angel = math.degrees(math.atan(angel))

        if distance < 1:
            self.speed = 0
        elif 1 <= distance <= 30:
            if self.speed > 1:
                self.speed -= 0.5
        else:
            self.speed += 0.07

        if self.abs_cords[1] - cordss[1] < 0:
            x = self.abs_cords[0] + math.sin(angel * math.pi / 180) * self.speed
            y = self.abs_cords[1] + math.cos(angel * math.pi / 180) * self.speed
        else:
            x = self.abs_cords[0] - math.sin(angel * math.pi / 180) * self.speed
            y = self.abs_cords[1] - math.cos(angel * math.pi / 180) * self.speed

        self.abs_cords = [x, y]

        return self.abs_cords


# Таймер для подсчета работы кода
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

# ---------- CONSTANTS ----------
FULLSCREEN = False
MAP_COF = 1
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
WORLD_NOISE_SIZE = 50
BLOCK_SIZE = MAP_COF * 32
FONT_PATH = r'D:\temp\project_of_the_gods\work_dir\main_menu\font.ttf'

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

pygame.display.set_caption('Pause break')


class MenuButton:
    def __init__(self, x: int, y: int, button_size: tuple, border: int, text: str, text_size: int,
                 surf: pygame.surface.Surface):
        self.color = (0, 0, 34)
        self.surf = surf
        self.font = pygame.font.Font(FONT_PATH, text_size)

        self.border_color = (0, 22, 87)
        self.x = x
        self.y = y
        self.button_size = button_size
        self.text = str(text)
        self.text_color = (243, 246, 250)
        tmp = self.font.render(self.text, True, self.text_color)
        self.border_width = border
        self.cords = (0, 0)

        self.anim_hover = 0

        self.on_click_set = [[False], [False], [False]]
        self.width, self.height = self.button_size

        self.font_render = self.font.render(self.text, True, self.text_color)

        self.button_surf = pygame.surface.Surface((self.button_size[0], self.button_size[1]))
        self.button_surf.set_colorkey((0, 0, 0))
        self.button_surf.convert_alpha()
        pygame.draw.rect(self.button_surf, self.border_color, (0, 0, *self.button_size), 0, 20)

        pygame.draw.rect(self.button_surf, self.color, (
            self.border_width, self.border_width, self.button_size[0] - self.border_width * 2,
            self.button_size[1] - self.border_width * 2), 0, 30)
        self.button_surf.blit(self.font_render, ((self.width - self.font_render.get_width()) // 2,
                                                 (self.height - self.font_render.get_height()) // 2))

    def draw(self, event):
        rect = self.button_surf.get_rect(topleft=(self.x - self.anim_hover, self.y))
        if rect.collidepoint(pygame.mouse.get_pos()):

            if event:
                event = event[0]
                if event.button == 1 and self.on_click_set[0][0]:
                    self.on_click_set[0][1](*self.on_click_set[0][2])
                elif event.button == 2 and self.on_click_set[1][0]:
                    self.on_click_set[1][1](*self.on_click_set[1][2])
                elif event.button == 3 and self.on_click_set[2][0]:
                    self.on_click_set[2][1](*self.on_click_set[2][2])

            self.anim_hover += 2
            if self.anim_hover >= 50:
                self.anim_hover = 50
        else:
            self.anim_hover -= 1
            if self.anim_hover <= 1:
                self.anim_hover = 1

        self.surf.blit(pygame.transform.scale(self.button_surf,
                                              (self.button_surf.get_width() * 1,
                                               self.button_surf.get_height() * 1)),
                       (self.x, self.y))

    def set_on_click(self, func, but: int, *args):
        self.on_click_set[but - 1] = [True, func, args]


class Message:
    def __init__(self, label, text, background: pygame.surface.Surface):
        self.font = pygame.font.Font(FONT_PATH, 60)
        self.screen = pygame.surface.Surface(background.get_size())
        self.background = background
        self.margin = self.screen.get_size()[0] * 0.04

        self.main_label = pygame.font.Font(FONT_PATH, 200).render(label, True, (243, 246, 250))

        self.date_update(text)
        self.button = MenuButton(width // 2 - (width * .2) // 2,
                                 height // 2 + self.text[0].get_height() * len(self.text), (width * .2, height * .15),
                                 width // 80, "OK", width // 22, self.screen)

        self.button.set_on_click(lambda: exit(), 1)

    def render(self, surf: pygame.surface.Surface, events):

        self.screen = pygame.surface.Surface(size)
        self.screen.set_colorkey((0, 0, 0))
        self.screen = self.screen.convert_alpha()

        pygame.draw.rect(self.screen, (0, 0, 0), (width // 2 - 350, height // 2 - 300, 700, 600), 0, 15)

        tmp_r = pygame.rect.Rect(0, 0, self.max_text_width + self.margin * 2,
                                 self.text[0].get_height() * len(self.text) + self.margin * 2)
        tmp_r.center = (width // 2, height // 2)
        pygame.draw.rect(self.screen, (0, 0, 22), tmp_r, 0, 15)

        self.screen.blit(self.main_label, self.main_label.get_rect(
            center=(width // 2, height // 2 - self.margin - 20 - self.text[0].get_height() * len(self.text))))

        tmp_s = pygame.surface.Surface((self.max_text_width, self.text[0].get_height() * len(self.text)))
        for text in enumerate(self.text):
            tmp_s.blit(text[1], text[1].get_rect(topleft=(0, text[1].get_height() * text[0])))
        self.screen.blit(tmp_s, tmp_s.get_rect(center=(width // 2, height // 2)))

        self.button.surf = self.screen
        self.button.draw(list(filter(lambda xx: xx.type == pygame.MOUSEBUTTONUP, events)))

        surf.blit(self.background, (0, 0))
        surf.blit(self.screen, (0, 0))

    def date_update(self, text: str):
        tmp_text = ['']

        for word in text.strip().split():
            if len(word) + len(tmp_text[-1]) > 35:
                tmp_text.append(word)
            else:
                tmp_text[-1] += ' ' + word

        for tmp in enumerate(tmp_text):
            tmp_text[tmp[0]] = tmp[1].strip()

        self.text = []
        for string in tmp_text:
            self.text.append(self.font.render(string, True, (243, 246, 250)))

        self.max_text_width = list(sorted(self.text, key=lambda x: x.get_width(), reverse=True))[0].get_width()


def message(label, text):
    global main_running
    global screen
    is_open = True
    background = blur(screen, 15)
    # background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    pause_obj = Message(label, text, background)

    while is_open:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                main_running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    screen.blit(background, (0, 0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_ESCAPE:
                    is_open = False
            elif event.type == pygame.MOUSEMOTION:
                pass
                # pl.move(event.rel)

        # screen.blit(background, (0, 0))

        pause_obj.render(screen, events)

        display_fps()
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main_running = True
    im = pygame.transform.scale(pygame.image.load('im.png').convert(), (int(1280 / 1), int(1231 / 1)))

    while main_running:
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
            elif event.type == pygame.MOUSEMOTION:
                pass

        '''keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            map_cords[0] += 5
        if keys[pygame.K_LEFT]:
            map_cords[0] -= 5
        if keys[pygame.K_DOWN]:
            map_cords[1] += 5
        if keys[pygame.K_UP]:
            map_cords[1] -= 5

        if map_cords[0] < -map_scale(510):
            tmp.move_visible_area(1)
            map_cords[0] = 0
        elif map_cords[0] > map_scale(510):
            tmp.move_visible_area(2)
            map_cords[0] = 0
        if map_cords[1] < -map_scale(510):
            tmp.move_visible_area(3)
            map_cords[1] = 0
        elif map_cords[1] > map_scale(510):
            tmp.move_visible_area(4)
            map_cords[1] = 0
        pl.tick()
        print(pl.get_cord())'''

        # Рендер основного окна
        screen.fill((47, 69, 56))
        screen.blit(im, (0, -100))
        display_fps()
        message('Внимание!', 'Вставой, Норт, довай, времени в обрез, помогай нам!!!')
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()  # Завершение работы
