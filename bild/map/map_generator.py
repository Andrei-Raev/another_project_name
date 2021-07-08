import math
import time
from math import cos, sin, radians, pi
from pprint import pprint
from random import randint, seed

import pygame

from lib.perlin_noise import PerlinNoiseFactory, smoothstep, lerp


# Функции
def get_biome(cof):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        if -0.3 < cof <= 0:
            return 0, 60, 151  # Тайга
        elif -0.8 < cof <= -0.3:
            return 0, 30, 101  # тундра
        elif cof <= -0.8:
            return 0, 30, 101  # Ледяные пустоши
    else:
        if 0 <= cof < 0.05:
            return 250, 254, 100  # Пляж
        elif 0.05 <= cof < 0.35:
            return 0, 151, 20  # Луга
        elif 0.35 <= cof < 0.5:
            return 1, 120, 48  # Равнины
        elif 0.5 <= cof < 0.85:
            return 121, 119, 120  # Горы
        else:
            return 255, 255, 255  # Снег в горах
    return 0, 0, 0  # На всякий случай


def color_asian(cof):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        if -0.1 < cof <= 0:
            return 0, 60, 151  # Мелководье
        elif cof <= -0.1:
            return 0, 30, 101  # Вода
    else:
        if 0 <= cof < 0.05:
            return 250, 254, 100  # Пляж
        elif 0.05 <= cof < 0.35:
            return 0, 151, 20  # Луга
        elif 0.35 <= cof < 0.5:
            return 1, 120, 48  # Равнины
        elif 0.5 <= cof < 0.85:
            return 121, 119, 120  # Горы
        else:
            return 255, 255, 255  # Снег в горах
    return 0, 0, 0  # На всякий случай


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.biome = 0

    def get_cords(self) -> list:
        return self.x, self.y

    def __repr__(self) -> str:
        return 'Point(x=%s, y=%s)' % (self.x, self.y)


def move_by_angle(x: int, y: int, angle: float, speed) -> tuple:
    x += speed * cos(angle)
    y += speed * sin(angle)
    return [x, y]


def inPolygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i - 1]) or (yp[i - 1] <= y < yp[i])) and
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c
    return bool(c)


def dist(p1: tuple, p2: Point):
    p2 = p2.get_cords()
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def boarder_dist(point: tuple, shape):
    dists = []
    for i in range(len(shape)):
        p1 = shape[i]

        try:
            p2 = shape[i + 1]
        except IndexError:
            p2 = shape[0]

        x_diff = p2.x - p1.x
        y_diff = p2.y - p1.y
        num = abs(y_diff * point[0] - x_diff * point[1] + p2.x * p1.y - p2.y * p1.x)
        den = math.sqrt(y_diff ** 2 + x_diff ** 2)
        dists.append(num / den)
    return min(dists)


def find_nearest(coordinate, matrix):
    return min(matrix, key=lambda x: dist(coordinate, x))


# НАЧАЛО АЛГОРИТМА ГЕНЕРАЦИИ МИРА

size = truth_size = 400
res = 120

frames = 1
world_noise = [list()]

start_time = time.time()

seed(int(input('Сид >>>\t')))

woronoi = []
for _ in range(200):
    woronoi.append(Point(randint(0, 400), randint(0, 400)))

island_coords = [[], []]

for angel in range(14):
    if angel < 3:
        continue
    angel = (angel * pi * 32) / 180
    if .5 < angel < 1.5:
        island_coords[0].append(cos(angel) * -180 + 200)
    else:
        island_coords[0].append(cos(angel) * 180 + 200)

    if angel < 1:
        island_coords[1].append(sin(angel) * 180 + 200)
    else:
        island_coords[1].append(sin(angel) * -180 + 200)

'''angle = 1.5
for i in range(50):
    island_coords[0].append(coords[0])
    island_coords[1].append(coords[1])
    angle -= randint(-11, 30) / 100
    coords = move_by_angle(coords[0], coords[1], angle, 20)
print(len(island_coords[0]), len(island_coords[1]))'''

# убираем лишний вороной
for num, point in enumerate(woronoi):
    if not inPolygon(*point.get_cords(), island_coords[0], island_coords[1]):
        del woronoi[num]

biomes_color = [(162, 207, 255), (77, 165, 74), (221, 221, 36)]
biomes = []
for _ in range(10):
    tmp_point = Point(randint(0, 400), randint(0, 400))
    while not inPolygon(*tmp_point.get_cords(), island_coords[0], island_coords[1]):
        tmp_point = Point(randint(0, 400), randint(0, 400))
    tmp_point.biome = randint(-1, 1)
    biomes.append(tmp_point)

for point in woronoi:
    point.biome = find_nearest(point.get_cords(), biomes).biome

'''
matrix_size = 30
matrix = [list() for _ in range(matrix_size)]

for y in range(matrix_size):
    for x in range(matrix_size):
        matrix[y].append(Point((x + 1) * 10 + randint(-5, 5), (y + 1) * 10 + randint(-5, 5)))

pprint(matrix)'''

point_islands_coord = []

for i in zip(island_coords[0], island_coords[1]):
    point_islands_coord.append(Point(i[0], i[1]))

pnf = PerlinNoiseFactory(seed=0, octaves=4, unbias=True)
print('GENERATED!')


class Block:
    def __init__(self, height: tuple, biome: int, boarder_dist: float):
        self.height = height
        self.biome = biome
        self.boarder_dist = boarder_dist
        self.color = [0, 0, 0]

    def render_color(self):
        cof = self.height

        if self.boarder_dist < 100:
            if 0 > cof > -0.1:
                cof -= 1 / self.boarder_dist
            else:
                cof -= 2 / self.boarder_dist

        self.color = color_asian(cof)


def generate_point(x: int, y: int) -> Block:
    tmp_block = Block(pnf(x / res, y / res, 0), find_nearest((num_2, num), woronoi).biome,
                      boarder_dist((x, y), point_islands_coord))
    tmp_block.render_color()
    return tmp_block


# КОНЕЦ АЛГОРИТМА ГЕНЕРАЦИИ МИРА


if __name__ == '__main__':
    pygame.init()
    size = width, height = size * 2, size * 2
    screen2 = pygame.display.set_mode(size)
    screen2.fill((99, 2, 34))

    screen = pygame.surface.Surface((truth_size, truth_size))
    screen.fill((30, 30, 0))

    for num in range(truth_size):
        screen2.blit(pygame.transform.scale(screen, size), (0, 0))
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                exit()

        for num_2 in range(truth_size):
            try:
                a = False
                # pygame.draw.rect(screen, color_asian(pnf(num_2 / res, num / res, 0)),
                #                  pygame.rect.Rect(num_2, num, 1, 1))
                '''for point_y_coord in range(matrix_size - 1):
                    if a:
                        a = False
                        break
                    for point_x_coord in range(matrix_size - 1):
                        pp1 = matrix[point_y_coord][point_x_coord:point_x_coord + 2]
                        pp2 = matrix[point_y_coord + 1][point_x_coord:point_x_coord + 2][::-1]
                        pp = pp1 + pp2
                        x_coords = [p.get_cords()[0] for p in pp]
                        y_coords = [p.get_cords()[1] for p in pp]'''
                if inPolygon(num_2, num, island_coords[0][::-1], island_coords[1][::-1]):
                    pygame.draw.rect(screen, generate_point(num_2, num).color, pygame.rect.Rect(num_2, num, 1, 1))
                    # a = True
                    # break
                else:
                    pygame.draw.rect(screen, (0, 30, 101), pygame.rect.Rect(num_2, num, 1, 1))
                    # pygame.draw.rect(screen, (230, 50, 50), pygame.rect.Rect(num_2, num, 1, 1))

            except Exception as e:
                print(e)
                # exit(1)
    # ...
    screen2.blit(pygame.transform.scale2x(screen), (0, 0))

    '''aa = 0
    for x, y in zip(island_coords[0], island_coords[1]):
        pygame.draw.circle(screen2, (aa, aa, aa), (x*2, y*2), 3)
        aa += 1
        if aa > 255:
            aa = 110'''
    pygame.display.flip()
    print('DONE!')
    print("--- %s seconds ---" % (time.time() - start_time))
    r = True
    while r:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                r = False

    pygame.quit()
