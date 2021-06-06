import pygame
from pyperclip import copy

pygame.init()
surface = pygame.image.load(r'C:\Users\andre\OneDrive\Рабочий стол\bomb2.png')
raw_str = pygame.image.tostring(surface, "RGBA", False)

copy(f'pygame.image.fromstring({str(raw_str)}, {surface.get_size()}, "RGBA")')
