from PIL import Image
from pygame.sprite import Sprite
from pygame import image
from pygame.mouse import get_pos, get_pressed
from pygame.transform import scale2x, scale, flip
import os

from sample_classes.inventory import Item


def split_sprites(path, SCALE):
    res = []
    im = Image.open(path)
    for i in range(im.size[0] // 80):
        tmp_im = im.crop((i * 80, 0, (i + 1) * 80, im.size[1]))
        tmp_el = image.fromstring(tmp_im.tobytes("raw", 'RGBA'), tmp_im.size, 'RGBA').convert_alpha()
        res.append(scale(tmp_el, [round(x * SCALE * 1.3) for x in tmp_el.get_size()]))

    return res


def load_textures(direct, SCALE):
    textures = {}
    for im in os.listdir(direct):
        if im == 'item.png':
            tmp_el = image.load(direct + '/' + im)
            textures.update({im[:-4]: [scale(tmp_el, [round(x * SCALE * 1.3) for x in tmp_el.get_size()])]})
        else:
            textures.update({im[:-4]: split_sprites(direct + '/' + im, SCALE)})
    return textures


class Clothes(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def render(self, surf, mode, anim):
        surf.blit(self.image, self)


class CursObj(Sprite):
    def __init__(self, *groups):  #: pygame.AbstractGroup):
        super().__init__(*groups)
        self.image = image.load('res/image/gui/curs.png')
        self.textures = {'def': scale2x(scale2x(image.load('res/image/gui/curs.png'))),
                         'l': scale2x(scale2x(image.load('res/image/gui/curs_l.png'))),
                         'r': scale2x(scale2x(image.load('res/image/gui/curs_r.png')))}

        self.rect = self.image.get_rect(center=get_pos())

    def render(self, surf):
        if get_pressed()[0]:
            self.image = self.textures['l']
        elif get_pressed()[2]:
            self.image = self.textures['r']
        else:
            self.image = self.textures['def']
        self.rect = self.image.get_rect(center=get_pos())

        surf.blit(self.image, self.rect)


class Dress(Sprite):
    def __init__(self, title, textures, *groups):
        super().__init__(*groups)
        self.title = title
        self.textures = textures
        self.inventory_cords = (0, 1)
        self.item = Item(self.textures['item'][0], self.title, '', self.inventory_cords)

    def render(self, surf, mode, anim, rotate):
        if mode in ['stand', 'swim']:
            anim = 0

        if anim > 9:
            anim = 9

        self.image = self.textures[mode][anim]

        if rotate:
            self.image = flip(self.image, True, False)
        surf.blit(self.image, (0, 0))

    def get_item(self):
        return self.item

