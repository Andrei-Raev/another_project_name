"""Отображает значение fps

Доработать!"""

# ---------- FPS CLOCK ----------
import pygame

pygame.init()

# Создание шрифта для счетчика fps
font = pygame.font.SysFont(None, 50)


# Рендер четчика fps
def render(surface, value):
    global font
    text_to_show = font.render(value, False, pygame.Color("white"))
    surface.blit(text_to_show, (0, 0))


# Отображение четчика fps
def display_fps(surface, clock):
    render(surface, str(int(clock.get_fps())))
