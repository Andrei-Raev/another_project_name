"""Функции, использующиеся в работе игры"""

import pygame
from PIL import Image


def get_relative_coordinates(x: int, y: int) -> tuple:
    """Принимает абсолютные координаты и преобразует их в относительные

    Аргументы:
    x (int) - абсолютная коорджината по x
    Y (int) - абсолютная координата по y

    Возвращает кортеж кортежей (координата внутри чанка), (координата чанка)"""

    x = (x % 16, x // 16)
    y = (y % 16, y // 16)
    return (x[0], y[0]), (x[1], y[1])


def split_gorisontal_sprites(path: str, sprite_width=80) -> list:
    """Разделяет линейный спрайтлист на отдельные спрайты

    Аргументы:
    path (str) - путь к спрайтлисту
    sprite_width (int) - ширина одного спрайта в пикселях"""

    res = []
    im = Image.open(path)
    for i in range(im.size[0] // sprite_width):
        tmp_im = im.crop((i * sprite_width, 0, (i + 1) * sprite_width, im.size[1]))

        res.append(pygame.image.fromstring(tmp_im.tobytes("raw", 'RGBA'), tmp_im.size, 'RGBA').convert_alpha())
    return res


def gradient(val1: int, val2: int, cof: float) -> int:
    """Ищет значение по градиенту между двумя числами

    Аргументы:
    val1 (int) - минимальное значение градиента
    val2 (int) - максимальное значение градиента
    cof (float) - смещение по градиенту

    Возвращает получанное значение в виду целого числа"""

    return round(val1 * cof + val2 * (1 - cof))
