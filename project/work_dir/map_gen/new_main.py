import numpy as np
import random
from math import tan, sqrt
# import pygame
import pygame
from numba import njit

SIZE = 25
SCALE = 21

random.seed(1)

world = (
    [[[round(random.uniform(-1, 1), 10), round(random.uniform(-1, 1), 10)] for _ in range(SIZE)] for _ in range(SIZE)])

for i in enumerate(world):
    for j in enumerate(i[1]):
        v = tuple(j[1])
        world[i[0]][j[0]] = list([v[0] / sqrt(v[0] ** 2 + v[1] ** 2), v[1] / sqrt(v[0] ** 2 + v[1] ** 2)])
del v

world_noise = []
world_noise.append(list())

for i in range(SIZE - 1):
    for j in range(SIZE - 1):
        vect = list([world[i][j], world[i][j + 1], world[i + 1][j], world[i + 1][j + 1]])
        for i_t in range(SCALE):
            for j_t in range(SCALE):
                coss = list()
                tmp_vect = (i_t, -(j_t))
                if not all(tmp_vect):
                    continue
                coss.append((vect[0][0] * vect[0][1] + tmp_vect[0] * tmp_vect[1]) / (
                        sqrt(vect[0][0] ** 2 + tmp_vect[0] ** 2) * sqrt(vect[0][1] ** 2 + tmp_vect[1] ** 2)))

                tmp_vect = (i_t - SCALE, -(j_t))
                if not all(tmp_vect):
                    continue
                coss.append((vect[0][0] * vect[0][1] + tmp_vect[0] * tmp_vect[1]) / (
                        sqrt(vect[0][0] ** 2 + tmp_vect[0] ** 2) * sqrt(vect[0][1] ** 2 + tmp_vect[1] ** 2)))

                tmp_vect = (i_t, SCALE - j_t)
                if not all(tmp_vect):
                    continue
                coss.append((vect[0][0] * vect[0][1] + tmp_vect[0] * tmp_vect[1]) / (
                        sqrt(vect[0][0] ** 2 + tmp_vect[0] ** 2) * sqrt(vect[0][1] ** 2 + tmp_vect[1] ** 2)))

                tmp_vect = (i_t - SCALE, SCALE - j_t)
                if not all(tmp_vect):
                    continue
                coss.append((vect[0][0] * vect[0][1] + tmp_vect[0] * tmp_vect[1]) / (
                        sqrt(vect[0][0] ** 2 + tmp_vect[0] ** 2) * sqrt(vect[0][1] ** 2 + tmp_vect[1] ** 2)))

                world_noise[-1].append(coss[:3])

                if len(world_noise[-1]) == 500:
                    world_noise.append(list())
            # print()
        # print('\n\n')

# print(*world_noise, sep='\n')
del world
print('GENERATED!')

if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    # ...
    screen.fill((0, 0, 0))

    for num, el in enumerate(world_noise):
        for num_2, el_2 in enumerate(el):
            pygame.draw.rect(screen, ((el_2[0] + 1) * 100, (el_2[1] + 1) * 100, (el_2[2] + 1) * 100),
                             (num, num_2, num, num_2))
    # ...
    print('DONE!')
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
