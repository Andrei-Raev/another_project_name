"""Библиотека для обработки изображений и поверхностей"""

import pygame
from PIL import Image


def save_surface(surface: pygame.surface.Surface, save=False) -> None:
    """Сохраняет поверхность как изображение или показывает ее в стандартном просмоторщике Windows

    Аргументы:
    surface (pygame.surface.Surface) - поверхность pygame.surface.Surface, над которой будут производится манипуляции
    save (bool) - сохранять ли поверхность (True) или просто показать (False)"""

    strFormat = 'RGBA'

    raw_str = pygame.image.tostring(surface, strFormat, False)
    image = Image.frombytes(strFormat, surface.get_size(), raw_str)

    if save:
        image.save(f'surface.png')
    else:
        image.show()


def bright(surface: pygame.surface.Surface, brightness: int) -> pygame.surface.Surface:
    """Увеличивает яркость изображения на определенную велечину

    Аргументы:
    surface (pygame.surface.Surface) - исходная поверхность
    brightness (int) - значение, на которое надо увеличить яркость

    Возвращает поверхность

    Требуется оптимизация!"""

    image = Image.frombytes('RGBA', surface.get_size(), pygame.image.tostring(surface, 'RGBA', False))
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


def dark(surf: pygame.surface.Surface, darkness: int) -> pygame.surface.Surface:
    """Уменьшает яркость изображения на определенную велечину

        Аргументы:
        surface (pygame.surface.Surface) - исходная поверхность
        darkness (int) - значение, на которое надо уменьшить яркость

        Возвращает поверхность

        Требуется оптимизация!"""

    image = Image.frombytes('RGBA', surf.get_size(), pygame.image.tostring(surf, 'RGBA', False))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))

            red = int(r // darkness)
            red = min(255, max(0, red))

            green = int(g // darkness)
            green = min(255, max(0, green))

            blue = int(b // darkness)
            blue = min(255, max(0, blue))

            image.putpixel((x, y), (red, green, blue, a))
    del r, g, b, a, red, green, blue, darkness
    return pygame.image.fromstring(image.tobytes("raw", 'RGBA'), image.size, 'RGBA')
