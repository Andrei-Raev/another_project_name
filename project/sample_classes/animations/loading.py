from copy import copy
from time import sleep

import pygame
from math import sin, cos, radians, atan, degrees

from PIL import Image

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
a = 700
size = a, a
screen = pygame.display.set_mode(size)

screen.fill(BLACK)


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


def draw_arrow(surf, color, start_cords, end_cords, width):
    rad_ar = width * 2.3

    points = []

    tmp_x = start_cords[0] - end_cords[0]
    tmp_y = start_cords[1] - end_cords[1]

    try:
        rotate = tmp_x / tmp_y
    except ZeroDivisionError:
        rotate = 0

    if not tmp_x:
        rotate = 180
    else:
        rotate = degrees(atan(rotate))

    for iters in range(3):

        if tmp_x * tmp_y < 0:
            tmp = radians(120 * iters - rotate + 30)
        else:
            tmp = radians(120 * iters - rotate - 30)

        if tmp_x > 0:
            tmp -= 1

        points.append((cos(tmp) * rad_ar + end_cords[0], sin(tmp) * rad_ar + end_cords[1]))

    main_points = []

    tmp = radians(-rotate)
    main_points.append((cos(tmp) * width / 2 + start_cords[0], sin(tmp) * width / 2 + start_cords[1]))

    tmp = radians(180 - rotate)
    main_points.append((cos(tmp) * width / 2 + start_cords[0], sin(tmp) * width / 2 + start_cords[1]))

    main_points.append((cos(tmp) * width / 2 + end_cords[0], sin(tmp) * width / 2 + end_cords[1]))

    tmp = radians(-rotate)
    main_points.append((cos(tmp) * width / 2 + end_cords[0], sin(tmp) * width / 2 + end_cords[1]))

    pygame.draw.polygon(surf, color, main_points, 0)
    pygame.draw.polygon(surf, color, points, 0)


def draw_circle_lines(surf, rads, center, width, rotate=False):
    for iters in range(3):
        if rotate:
            tmp = radians(120 * iters)
            draw_arrow(surf, WHITE,
                       ((sin(tmp) * rads[1] + center[0]), (cos(tmp) * rads[1] + center[1])),
                       ((sin(tmp) * rads[0] + center[0]), (cos(tmp) * rads[0] + center[1])), width)
        else:
            tmp = radians(120 * iters + 60)
            draw_arrow(surf, WHITE,
                       ((sin(tmp) * rads[0] + center[0]), (cos(tmp) * rads[0] + center[1])),
                       ((sin(tmp) * rads[1] + center[0]), (cos(tmp) * rads[1] + center[1])), width)


class LoadingAnim:
    def __init__(self, scr: pygame.surface.Surface, val):
        self.value = val
        self.size = scr.get_size()
        self.screen = pygame.surface.Surface(self.size)
        self.scr = scr
        self.fps = 60
        self.background = copy(scr)
        self.background_color = (0, 0, 0)
        self.color = (255, 255, 255)
        self.width = 10

        self.start()

    def start(self):
        self.screen.fill(self.background_color)
        for tmp_val in range(30):
            self.scr.blit(self.background, (0, 0))
            self.screen.set_alpha(255 * (tmp_val / 30))
            self.scr.blit(self.screen, (0, 0))

            clock.tick(self.fps)
            pygame.display.flip()

        self.screen.set_alpha(255)
        for tmp_val in range(20):
            self.screen.fill(self.background_color)
            self.scr.blit(self.screen, (0, 0))

            pygame.draw.circle(self.scr, self.color, [t // 2 for t in self.size], (self.size[1] // 4) * (tmp_val / 20),
                               self.width)

            clock.tick(self.fps)
            pygame.display.flip()

        for tmp_val in range(20):
            self.screen.fill(self.background_color)
            self.scr.blit(self.screen, (0, 0))

            pygame.draw.circle(self.scr, self.color, [t // 2 for t in self.size], (self.size[1] // 4), self.width)

            draw_circle_lines(self.scr, [(self.size[1] // 4) - tmp_val - 5, (self.size[1] // 4) - 5],
                              [t // 2 for t in self.size], self.width, True)
            draw_circle_lines(self.scr, [(self.size[1] // 4 - 5), (self.size[1] // 4) + tmp_val + 5],
                              [t // 2 for t in self.size], self.width)

            clock.tick(self.fps)
            pygame.display.flip()

    def change_value(self, new_val):
        if 0 <= self.value + new_val <= 100 and new_val != self.value:
            for tmp_val in range(new_val):
                self.value = tmp_val
                self.draw_screen()

                clock.tick(self.fps)
                pygame.display.flip()

    def draw_screen(self):
        self.screen.fill(self.background_color)
        self.scr.blit(self.screen, (0, 0))

        pygame.draw.circle(self.scr, self.color, [t // 2 for t in self.size], (self.size[1] // 4), self.width)

        draw_circle_lines(self.scr, [((self.size[1] // 4) - 25) - (((self.size[1] // 4) - 45) * self.value / 100),
                                     (self.size[1] // 4) - 5], [t // 2 for t in self.size], self.width, True)
        draw_circle_lines(self.scr,
                          [(self.size[1] // 4 - 5), (self.size[1] // 4) + 25 + self.value * self.size[1] / 1000],
                          [t // 2 for t in self.size], self.width)

        clock.tick(self.fps)
        pygame.display.flip()

    def end(self, new_surf):
        for tmp_val in range(20):
            self.screen.fill(self.background_color)
            self.scr.blit(self.screen, (0, 0))

            pygame.draw.circle(self.scr, self.color, [t // 2 for t in self.size], (self.size[1] // 4) + tmp_val * 20,
                               self.width)

            draw_circle_lines(self.scr, [((self.size[1] // 4) - 25) - (((self.size[1] // 4) - 45) * self.value / 100),
                                         (self.size[1] // 4) - 5 - ((self.size[1] // 4) - 32) * tmp_val / 20],
                              [t // 2 for t in self.size], self.width, True)
            draw_circle_lines(self.scr,
                              [(self.size[1] // 4 - 5) + (self.size[1] // 4 - 5) * tmp_val / 15,
                               ((self.size[1] // 4) + 25 + self.value * self.size[1] / 1000) + (
                                       (self.size[1] // 4) + 25 + self.value * self.size[1] / 1000) * tmp_val / 15],
                              [t // 2 for t in self.size], self.width)

            clock.tick(self.fps)
            pygame.display.flip()

        for tmp_val in range(20):
            self.scr.blit(new_surf, (0, 0))
            self.screen.set_alpha(255 - 255 * (tmp_val / 20))
            self.scr.blit(self.screen, (0, 0))

            clock.tick(self.fps)
            pygame.display.flip()

        self.scr.blit(new_surf, (0, 0))
        pygame.display.flip()


clock = pygame.time.Clock()

'''for i in range(80):
    t = pygame.surface.Surface((1200, 1200))
    screen.fill((0, 0, 0))
    draw_circle_lines(t, [100 - i, 98])
    draw_circle_lines(t, [100, 100 + i], True)
    pygame.draw.circle(t, WHITE, (600, 600), 200, 20)
    screen.blit(antialiasing(t, 2), (0, 0))
    clock.tick(60)
    pygame.display.flip()
'''

screen.fill((15, 99, 66))
pygame.display.flip()
sleep(1)
ttt = LoadingAnim(screen, 0)

ttt.change_value(100)
# ttt.change_value(-50)
ttt.end(pygame.transform.scale(pygame.image.load('im.png'), (700, 700)))

'''
for i in range(30):
    t = pygame.surface.Surface((1200, 1200))
    screen.fill((0, 0, 0))
    draw_circle_lines(t, [20 - i * .9, 98 - i * 2.95],[t // 2 for t in size],20)
    draw_circle_lines(t, [100 + i * 10, 180 + i * 8],[t // 2 for t in size],20, True)
    pygame.draw.circle(t, WHITE, [t // 2 for t in size], 200 + i * 25, 20)
    screen.blit(antialiasing(t, 4), (0, 0))
    clock.tick(60)
    pygame.display.flip()
'''
while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
