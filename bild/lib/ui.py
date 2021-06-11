"""Элементы интерфейса игры"""

import pygame


class UI:
    def __init__(self, max_hp):
        self.indicator = Indicator(pl)

        self.curs = [CursObj()]

    def render(self, surf: pygame.surface.Surface, _):
        # self.hp_bar.set_progress(hp)
        # self.hp_bar.draw()
        # surf.blit(self.hp_bar.surf, (width - width // 4.5, height // 30))

        self.indicator.update(pl)
        self.indicator.render(surf)

        for obj in self.curs:
            obj.render(surf)


class Indicator(pygame.sprite.Sprite):
    def __init__(self, player: Player, *groups):
        super().__init__(*groups)

        tmp_im = Image.open('res/image/entities/player/main.png').transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image = Image.new("RGBA", tmp_im.size, (255, 255, 250, 255))
        image.alpha_composite(tmp_im)
        image = image.crop((round(image.size[0] * .35), round(image.size[1] * .3),
                            round(image.size[0] * .75), round(image.size[1] * .7)))
        # Рисование
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, *image.size), outline=(0, 22, 87, 255), width=2)

        image = (pygame.image.fromstring(image.tobytes("raw", "RGBA"), image.size, "RGBA"))
        self.avator = pygame.transform.scale(image, [i * 2 for i in image.get_size()])
        self.main_image = pygame.surface.Surface((self.avator.get_size()[0] * 3, self.avator.get_size()[1]))
        self.main_image.fill((10, 0, 0))
        self.main_image.set_colorkey((10, 0, 0))
        self.main_image.convert_alpha()
        self.main_image.fill((0, 22, 87, 100))

    def update(self, player: Player, *args, **kwargs) -> None:
        self.image = copy(self.main_image)
        self.image.blit(self.avator, (0, 0))

        pygame.draw.rect(self.image, (200, 10, 10),
                         (self.image.get_width() - self.avator.get_width() * 2, self.image.get_height() / 3 - 7,
                          self.image.get_width() + self.image.get_width() * (player.hp / player.max_hp) * 0 - 130, 15))
        pygame.draw.rect(self.image, (224, 220, 0),
                         (self.image.get_width() - self.avator.get_width() * 2,
                          self.image.get_height() - self.image.get_height() / 3 - 7,
                          self.image.get_width() * (player.vitality / player.max_vitality) - 130,
                          15))
        # print(player.vitality / player.max_vitality, player.vitality)

    def render(self, surf):
        surf.blit(self.image, (width * .06, height * .06))

    def save_s(self):
        save_s(self.image)


class ProgressBar:
    def __init__(self, surf: pygame.surface.Surface, border: int, border_radius: int, progress: int, max_progress=100):
        self.color = (243, 246, 250)
        self.border_radius = border_radius
        self.border_color = (0, 22, 87)
        self.x = 0
        self.y = 0
        self.height = surf.get_height()
        self.width = surf.get_width()
        self.surf = surf
        self.border_width = border
        self.progress = progress
        self.max_progress = max_progress
        self.bg_color = (0, 0, 34)

        # self.cords = (0, 0)

        # self.anim_hover = 0

        # self.on_click_set = [[False], [False], [False]]

    def draw(self, *_):
        pygame.draw.rect(self.surf, self.border_color,
                         (0, 0, self.surf.get_width(), self.surf.get_height()), 0, self.border_radius)
        pygame.draw.rect(self.surf, self.bg_color,
                         (self.border_width, self.border_width, self.width - self.border_width * 2,
                          self.height - self.border_width * 2), 0, self.border_radius)
        len_prog = (self.width + self.border_width * 2) // self.max_progress * self.progress  # Хрень
        if self.progress == self.max_progress:
            len_prog = self.width - self.border_width * 2
        if self.progress:
            pygame.draw.rect(self.surf, self.color,
                             (self.border_width, self.border_width, len_prog, self.height - self.border_width * 2), 0,
                             self.border_radius)

    def set_progress(self, val: int):
        if self.max_progress < val:
            raise ValueError(f'value ({val}) > max progress ({self.max_progress})')
        elif val < 0:
            raise ValueError(f'value less than zero ({val})')

        self.progress = val

    def add_progress(self, val: int):
        self.progress += val
        if self.progress < 0:
            self.progress = 0
        elif self.progress > self.max_progress:
            self.progress = self.max_progress
