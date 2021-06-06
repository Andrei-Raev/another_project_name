import time

import pygame

from itertools import product
import math
import random as random_noise


def smoothstep(t):
    return t * t * (3. - 2. * t)


def lerp(t, a, b):
    return a + t * (b - a)


class PerlinNoiseFactory(object):
    def __init__(self, dimension, octaves=1, tile=(), unbias=False, seed=1):
        self.dimension = dimension
        self.octaves = octaves
        self.tile = tile + (0,) * dimension
        self.unbias = unbias
        self.scale_factor = 2 * dimension ** -0.5
        self.random = random_noise
        self.random.seed(seed)
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


from numba import njit

size = 400
res = 70
frames = 1

pnf = PerlinNoiseFactory(3, octaves=4, tile=(15, 15, 15), unbias=True)
pnf_bioms = PerlinNoiseFactory(3, octaves=1, tile=(10, 10, 10), unbias=False)

world_noise = [list()]


@njit()
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


@njit()
def color_asian(cof):
    if -0.5 <= cof <= 0.5:
        cof = cof * 1.8
    else:
        if cof > 0:
            cof = (cof - 0.5) * 0.2 + 0.9
        else:
            cof = (cof + 0.5) * 0.2 - 0.9

    if cof <= 0:
        if -0.05 < cof <= 0:
            return 0, 60, 151  # Мелководье
        elif cof <= -0.05:
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


start_time = time.time()

for x in range(size):
    for y in range(size):
        n = pnf(x / res, y / res, 0)
        world_noise[-1].append(n)
    world_noise.append(list())
# print(*world_noise)
print('GENERATED!')

if __name__ == '__main__':
    pygame.init()
    size = width, height = size, size
    screen = pygame.display.set_mode(size)
    # ...
    screen.fill((0, 0, 0))

    for num, el in enumerate(world_noise):
        for num_2, el_2 in enumerate(el):
            try:
                pygame.draw.rect(screen, color_asian(el_2), (num, num_2, num, num_2))
                # print(color_asian(el_2), (num, num_2, num, num_2), sep='\t')
            except Exception as e:
                print(e)
    # ...
    print('DONE!')
    pygame.display.flip()
    print("--- %s seconds ---" % (time.time() - start_time))
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
