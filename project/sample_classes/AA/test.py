import random
import time
from threading import Thread

import pygame

from PIL import Image, ImageFilter

pygame.init()


def init_screen_and_clock():
    global screen, display, clock
    pygame.init()
    WINDOW_SIZE = (1150, 640)
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    clock = pygame.time.Clock()


def create_fonts(font_sizes_list):
    "Creates different fonts with one list"
    fonts = []
    for size in font_sizes_list:
        fonts.append(
            pygame.font.SysFont("Arial", size))
    return fonts


def render(fnt, what, color, where):
    "Renders the fonts as passed from display_fps"
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


def display_fps():
    "Data that will be rendered and blitted in _display"
    render(
        fonts[0],
        what=str(int(clock.get_fps())),
        color="white",
        where=(0, 0))


init_screen_and_clock()
fonts = create_fonts([32, 16, 14, 8])


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


HEIGHT = 1280
WIDTH = 720

size = width, height = 700, 700

if __name__ == '__main__':
    fps = 60
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('None')

    COF = 4
    xx, yy = (300, 300)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # xx += event.rel[0]
                # yy += event.rel[1]
                pass

        start_time = time.time()
        tmp = pygame.Surface((600 * COF, 600 * COF))
        pygame.draw.circle(tmp, (255, 255, 255), (xx * COF, yy * COF), 270 * COF, 0)
        #f = pygame.font.Font(None, 150)
        #tt = f.render('fefef', False, (0,255, 0))
        #ss = tmp.get_size()
        #tmp.blit(tt, ([i // 2 for i in ss]))
        tmp = antialiasing(tmp, COF)

        screen.blit(tmp, (50, 50))
        display_fps()
        pygame.display.flip()
        print("--- %s seconds ---" % (time.time() - start_time))
        clock.tick(fps)
    pygame.quit()
