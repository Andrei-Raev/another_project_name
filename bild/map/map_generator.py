import time

import pygame

from lib.perlin_noise import PerlinNoiseFactory, smoothstep, lerp


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


size = 400
res = 70
frames = 1



world_noise = [list()]
start_time = time.time()

print('GENERATED!')

pnf = PerlinNoiseFactory(seed=23, octaves=4, unbias=True)

if __name__ == '__main__':
    pygame.init()
    size = width, height = size * 2, size * 2
    screen2 = pygame.display.set_mode(size)
    screen2.fill((99, 2, 34))
    # ...
    screen = pygame.surface.Surface((400, 400))
    screen.fill((30, 30, 0))

    for num in range(400):
        screen2.blit(pygame.transform.scale(screen, size), (0, 0))
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                exit()

        for num_2 in range(400):
            try:
                pygame.draw.rect(screen, color_asian(pnf(num_2 / res, num / res, 0)),
                                 pygame.rect.Rect(num_2, num, 1, 1))
            except Exception as e:
                print(e)
    # ...
    screen2.blit(pygame.transform.scale2x(screen), (0, 0))
    print('DONE!')
    pygame.display.flip()
    print("--- %s seconds ---" % (time.time() - start_time))
    r = True
    while r:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                r = False

    pygame.quit()
