"""Элементы интерфейса игры"""
from json import load

import pygame
from random import randint

from lib.image_processing import blur
from lib.vars import *
from res.textures import TEXTURES, render_screen, size, height, width, SCALE_COF


def collidepoint(rect: pygame.rect.Rect, point: tuple):
    coords = [rect.x, rect.y, rect.x + rect.w, rect.y + rect.h]
    if coords[0] <= point[0] <= coords[2] and coords[1] <= point[1] <= coords[3]:
        return True
    else:
        return False


class BaseGuiObject:
    def __init__(self, position, layer):
        self.surface = pygame.surface.Surface((0, 0))
        self.position = position
        self.layer = layer


class Font:
    def __init__(self):
        pass

    def render(self, text):
        pass


class Button(BaseGuiObject):
    def __init__(self, texture_type, text, position, width=0):
        super().__init__(position, 5)
        self.text = str(text)

        with open(f'res/textures/gui/buttons/{texture_type}/data.json', 'r') as data_file:
            tmp_dict = load(data_file)
            order = tmp_dict['order']
            self.text_color = tmp_dict['text_color']
            self.font = pygame.font.Font(r'D:\temp\game\bild\res\textures\gui\font.ttf', tmp_dict['font_size'])

        self.textures = {'side': [], 'center': []}
        self.textures_hover = {'side': [], 'center': []}
        self.textures_pressed = {'side': [], 'center': []}

        tmp_surface = pygame.image.load(f'res/textures/gui/buttons/{texture_type}/texture.png').convert_alpha()
        tmp_surface_hover = pygame.image.load(
            f'res/textures/gui/buttons/{texture_type}/texture_hover.png').convert_alpha()
        tmp_surface_pressed = pygame.image.load(
            f'res/textures/gui/buttons/{texture_type}/texture_pressed.png').convert_alpha()

        count = 0

        for texture_type in order:
            if texture_type == 'side':
                self.textures['side'].append(tmp_surface.subsurface(count, 0, 3, tmp_surface.get_height()))
                self.textures_hover['side'].append(
                    tmp_surface_hover.subsurface(count, 0, 3, tmp_surface.get_height()))
                self.textures_pressed['side'].append(
                    tmp_surface_pressed.subsurface(count, 0, 3, tmp_surface.get_height()))
                count += 3
            elif texture_type == 'center':
                self.textures['center'].append(tmp_surface.subsurface(count, 0, 2, tmp_surface.get_height()))
                self.textures_hover['center'].append(
                    tmp_surface_hover.subsurface(count, 0, 2, tmp_surface.get_height()))
                self.textures_pressed['center'].append(
                    tmp_surface_pressed.subsurface(count, 0, 2, tmp_surface.get_height()))
                count += 2

        self.on_click = [[False], [False], [False]]
        self.surfaces = []
        self.width = (self.font.render(self.text, False, self.text_color).get_width() + 6) if not width else width

        self.draw()

    def draw(self):
        text_surface = self.font.render(self.text, False, self.text_color)

        sides = [self.textures['side'][randint(0, len(self.textures['side']) - 1)],
                 pygame.transform.flip(self.textures['side'][randint(0, len(self.textures['side']) - 1)], True, False)]
        sides_hover = [self.textures_hover['side'][randint(0, len(self.textures['side']) - 1)],
                       pygame.transform.flip(self.textures_hover['side'][randint(0, len(self.textures['side']) - 1)],
                                             True, False)]
        sides_pressed = [self.textures_pressed['side'][randint(0, len(self.textures['side']) - 1)],
                         pygame.transform.flip(
                             self.textures_pressed['side'][randint(0, len(self.textures['side']) - 1)],
                             True, False)]

        self.surfaces = [pygame.surface.Surface((self.width, self.textures_pressed['side'][0].get_height())),
                         pygame.surface.Surface((self.width, self.textures_pressed['side'][0].get_height())),
                         pygame.surface.Surface((self.width, self.textures_pressed['side'][0].get_height()))]

        for surf in self.surfaces:
            surf.fill((0, 0, 0))
            surf.set_colorkey((0, 0, 0))
            surf.convert_alpha()

        self.surfaces[0].blit(sides[0], (0, 0))
        self.surfaces[1].blit(sides_hover[0], (0, 0))
        self.surfaces[2].blit(sides_pressed[0], (0, 0))

        for i in range(self.width // 2 - 2):
            ran = randint(0, len(self.textures['center']) - 1)
            self.surfaces[0].blit(self.textures['center'][ran], (i * 2 + 3, 0))
            self.surfaces[1].blit(self.textures_hover['center'][ran], (i * 2 + 3, 0))
            self.surfaces[2].blit(self.textures_pressed['center'][ran], (i * 2 + 3, 0))

        self.surfaces[0].blit(sides[1], (self.surfaces[0].get_width() - 3, 0))
        self.surfaces[1].blit(sides_hover[1], (self.surfaces[0].get_width() - 3, 0))
        self.surfaces[2].blit(sides_pressed[1], (self.surfaces[0].get_width() - 3, 0))

        self.surfaces[0].blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, 0))
        self.surfaces[1].blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, 0))
        self.surfaces[2].blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, 0))

    def render(self, surface, event):
        rect = self.surfaces[0].get_rect(topleft=self.position)
        if rect.collidepoint(pygame.mouse.get_pos()[0] / SCALE_COF, pygame.mouse.get_pos()[1] / SCALE_COF):
            if pygame.mouse.get_pressed(3)[0]:
                self.surface = self.surfaces[2]
            else:
                self.surface = self.surfaces[1]
        else:
            self.surface = self.surfaces[0]

        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if collidepoint(rect, (ev.pos[0] / SCALE_COF, ev.pos[1] / SCALE_COF)):
                    if ev.button == 1:
                        if self.on_click[0][0]:
                            self.on_click[0][1](*self.on_click[0][2])
                    if ev.button == 2:
                        if self.on_click[1][0]:
                            self.on_click[1][1](*self.on_click[1][2])
                    if ev.button == 3:
                        if self.on_click[2][0]:
                            self.on_click[2][1](*self.on_click[2][2])

        # if not randint(0, 15):
        #     self.draw()

        surface.blit(self.surface, self.position)

    def set_on_click(self, func, but: int, *args):
        self.on_click[but - 1] = [True, func, args]


class WithoutTextureButton(BaseGuiObject):
    def __init__(self, text, position):
        super().__init__(position, 5)
        self.text = str(text)

        self.font = pygame.font.Font(r'D:\temp\game\bild\res\textures\gui\font.ttf', 25)

        self.on_click = [[False], [False], [False]]
        self.surface = self.font.render(self.text, False, (32, 19, 7))

    def render(self, surface, event):
        rect = self.surface.get_rect(topleft=self.position)
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if collidepoint(rect, (ev.pos[0] / SCALE_COF, ev.pos[1] / SCALE_COF)):
                    if ev.button == 1:
                        if self.on_click[0][0]:
                            self.on_click[0][1](*self.on_click[0][2])
                    if ev.button == 2:
                        if self.on_click[1][0]:
                            self.on_click[1][1](*self.on_click[1][2])
                    if ev.button == 3:
                        if self.on_click[2][0]:
                            self.on_click[2][1](*self.on_click[2][2])

        surface.blit(self.surface, self.position)

    def set_on_click(self, func, but: int, *args):
        self.on_click[but - 1] = [True, func, args]


class TitleLossButton(BaseGuiObject):
    def __init__(self, texture_type, position):
        super().__init__(position, 5)
        self.surfaces = [pygame.image.load(f'res/textures/gui/buttons/{texture_type}/texture.png').convert_alpha(),
                         pygame.image.load(
                             f'res/textures/gui/buttons/{texture_type}/texture_hover.png').convert_alpha(),
                         pygame.image.load(
                             f'res/textures/gui/buttons/{texture_type}/texture_pressed.png').convert_alpha()]

        self.on_click = [[False], [False], [False]]

    def render(self, surface, event):
        rect = self.surfaces[0].get_rect(topleft=self.position)
        if rect.collidepoint(pygame.mouse.get_pos()[0] / SCALE_COF, pygame.mouse.get_pos()[1] / SCALE_COF):
            if pygame.mouse.get_pressed(3)[0]:
                self.surface = self.surfaces[2]
            else:
                self.surface = self.surfaces[1]
        else:
            self.surface = self.surfaces[0]

        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if collidepoint(rect, (ev.pos[0] / SCALE_COF, ev.pos[1] / SCALE_COF)):
                    if ev.button == 1:
                        if self.on_click[0][0]:
                            self.on_click[0][1](*self.on_click[0][2])
                    if ev.button == 2:
                        if self.on_click[1][0]:
                            self.on_click[1][1](*self.on_click[1][2])
                    if ev.button == 3:
                        if self.on_click[2][0]:
                            self.on_click[2][1](*self.on_click[2][2])

        surface.blit(self.surface, self.position)

    def set_on_click(self, func, but: int, *args):
        self.on_click[but - 1] = [True, func, args]


class Window(BaseGuiObject):
    def __init__(self, texture_type, position):
        super().__init__(position, 4)


def submit_window(screen, title: str, on_confirm, *args):
    def close():
        global running
        running = False
        return

    frame_pass, frame_counter = True, False
    buttons = [WithoutTextureButton('Подтвердить', (34, 146)),
               WithoutTextureButton('Отмена', (214, 146))]
    buttons[0].set_on_click(on_confirm, 1, *args)
    buttons[1].set_on_click(close, 1)

    render_screen = pygame.display.get_surface()

    background = blur(screen, 2)
    # tmp_background = pygame.image.load('res/textures/gui/windows/submit/background.png').convert()
    # background.blit(tmp_background,
    #                 tmp_background.get_rect(center=(render_screen.get_width() // 2, render_screen.get_height() // 2)))

    title = pygame.font.Font(r'D:\temp\game\bild\res\textures\gui\font.ttf', 25).render(title, False, (32, 19, 7))
    background.blit(title,
                    title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos[0] / SCALE_COF, event.pos[1] / SCALE_COF
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    pass
                elif event.key == pygame.K_TAB:
                    pass
            elif event.type == pygame.MOUSEMOTION:
                pass

        # Рендер основного окна
        if frame_counter:
            screen.blit(background, (0, 0))

            for bt in buttons:
                bt.render(screen, events)

            render_screen.blit(pygame.transform.scale(screen, size), (0, 0))
            if SHOW_FPS:
                display_fps(render_screen, clock)
            pygame.display.flip()
        if frame_pass:
            frame_counter = not frame_counter
        else:
            frame_counter = True
        clock.tick(fps)


'''
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
'''
