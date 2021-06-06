from copy import copy

import pygame
from PIL import Image

fps = 60
MAP_COF = 1.3
BLOCK_SIZE = MAP_COF * 32


def get_relative_coordinates(x: int, y: int):
    x = (x % 16, x // 16)
    y = (y % 16, y // 16)
    return (x[0], y[0]), (x[1], y[1])


def split_sprites(path):
    res = []
    im = Image.open(path)
    for i in range(im.size[0] // 80):
        tmp_im = im.crop((i * 80, 0, (i + 1) * 80, im.size[1]))

        res.append(pygame.image.fromstring(tmp_im.tobytes("raw", 'RGBA'), tmp_im.size, 'RGBA').convert_alpha())
    return res




# class Enemy(pygame.sprite.Sprite):

class Entity(pygame.sprite.Sprite):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):  #: pygame.AbstractGroup):
        super().__init__(*groups)

        self.hp = 100

        self.cords = cords
        self.image = texture['stand']
        self.textures = texture
        self.move_anim = 0
        self.rect = self.image.get_rect(center=self.cords)
        self.speed = ((32 * MAP_COF) * speed)
        self.isgoing = False
        self.rotate = False
        self.fly = False
        self.main_speed = ((32 * MAP_COF) * speed)
        self.counter = 0

    def move(self, delta_cords):
        self.cords = [self.cords[0] + delta_cords[0], self.cords[1] + delta_cords[1]]
        self.rect = self.image.get_rect(center=self.cords)

    def go(self, direct: int in [1, 2, 3, 4]):
        if direct == 1:
            self.move((0, self.speed // fps))
        elif direct == 2:
            self.move((0, -(self.speed // fps)))
        elif direct == 3:
            self.move((self.speed // fps, 0))
        elif direct == 4:
            self.move((-(self.speed // fps), 0))

    def get_cord(self, relative=True):
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        if relative:
            return get_relative_coordinates(x, y)
        else:
            return x, y

    def print_cord(self):
        global map_cords
        # print(tmp.center_chunk_cord)
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        return 'x = ' + str(x) + ', ' + 'y = ' + str(y)


class Player(Entity):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):

        super().__init__(texture, cords, speed, *groups)
        self.wear_clothes = [Dress('Стандартный визер', TEXTURES['clothes']['viser'])]
        self.mode = 'stand'

    def tick(self):
        self.fly = False
        self.isgoing = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotate = True
            if self.cords[0] > width - width // 5:
                map_cords[0] -= self.speed // fps
            else:
                self.go(3)

            self.isgoing = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotate = False
            if self.cords[0] < width // 5:
                map_cords[0] += self.speed // fps
            else:
                self.go(4)

            self.isgoing = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.cords[1] > height - height // 5:
                map_cords[1] -= self.speed // fps
            else:
                self.go(1)

            self.isgoing = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.cords[1] < height // 5:
                map_cords[1] += self.speed // fps
            else:
                self.go(2)

            self.isgoing = True

        if keys[pygame.K_LSHIFT]:
            self.fly = True

        if self.fly:
            self.mode = 'stand'

            self.hp -= 1
            self.speed = self.main_speed * 1.3

            if self.move_anim > 9:
                self.move_anim = 0
            self.image = self.textures['fly'][self.move_anim]

            if self.counter > 3:
                self.move_anim += 1
                self.counter = 0
            self.counter += 1
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)

        elif not self.isgoing:
            self.mode = 'stand'

            self.hp += 1
            if self.hp > 100:
                self.hp = 100

            self.image = self.textures['stand']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.mode = 'move'
            self.speed = self.main_speed

            self.counter += 1
            if self.counter == 2:
                self.move_anim += 1
                self.counter = 0
            elif self.counter > 3:
                self.counter = 0

            if self.rotate:
                self.image = pygame.transform.flip(self.textures['go'][self.move_anim - 1], True, False)
            else:
                self.image = self.textures['go'][self.move_anim - 1]

            if self.move_anim > 15:
                self.move_anim = 0
                self.isgoing = False

        if tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Water' and not self.fly:
            self.mode = 'swim'
            self.speed = self.main_speed * 0.6
            self.image = self.textures['swim']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        elif tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Stone':
            pass
        self.image = copy(self.image)
        for item in self.wear_clothes:
            item.render(self.image, self.mode, self.move_anim, self.rotate)
