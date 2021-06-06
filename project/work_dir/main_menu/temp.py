import time
from copy import copy
from screeninfo import get_monitors

import pygame
from math import sin, cos

pygame.init()

fullscreen = bool(input())

if fullscreen:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('test')

fps = 60
clock = pygame.time.Clock()


def gradient(col, col2, cof):
    return round(col * cof + col2 * (1 - cof))


def render_scale(val: int):
    return round(val * COF)


class MainMenuButton:
    def __init__(self, num: int, text: str):
        global height, width

        self.color = (32, 61, 97)
        self.border_color = (60, 147, 202)
        self.text_color = (118, 185, 226)
        self.padding = render_scale(5)
        self.border_width = render_scale(5)
        self.text = str(text)
        self.font = pygame.font.Font('font.ttf', render_scale(50))
        self.anim_hover = 0
        self.cords = (0, 0)
        self.on_click_set = [[False], [False], [False]]

        self.num = num
        tmp = self.font.render(self.text, True, self.text_color)

        self.height = render_scale(15) + tmp.get_height()
        self.width = render_scale(100)

        tmp_height = round(height * 0.25)

        self.y = round((height - tmp_height) / 3 * num - 1) + tmp_height - self.height
        self.x = width - round(width / 100 * 30) - render_scale((3 - num) * 20)
        self.f_x = width - round(width / 100 * 30)

    def draw(self, ev):
        for event in ev:
            if event.type == pygame.MOUSEMOTION:
                self.cords = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.x <= self.cords[0] <= width and self.y < self.cords[1] < self.y + self.height:
                    if event.button == 1 and self.on_click_set[0][0]:
                        self.on_click_set[0][1](*self.on_click_set[0][2])
                    elif event.button == 2 and self.on_click_set[1][0]:
                        self.on_click_set[1][1](*self.on_click_set[1][2])
                    elif event.button == 3 and self.on_click_set[2][0]:
                        self.on_click_set[2][1](*self.on_click_set[2][2])

        if self.x <= self.cords[0] <= width and self.y < self.cords[1] < self.y + self.height:
            tmp = self.font.render(self.text, True, tuple(
                [min(255, gradient(i[1], i[0], self.anim_hover / 45)) for i in zip(self.text_color, self.color)]))

            pygame.draw.polygon(screen, tuple(
                [min(255, gradient(i[1], i[0], self.anim_hover / 45)) for i in zip(self.color, self.border_color)]), (
                                    [self.x - self.height * sin(45) - self.anim_hover, self.y], [width, self.y],
                                    [width, self.y + self.height], [self.x - self.anim_hover, self.y + self.height]), 0)
            screen.blit(tmp, (self.f_x - tmp.get_width() + self.width + render_scale(40), self.y + self.padding))

            self.anim_hover += 3
            if self.anim_hover >= 45:
                self.anim_hover = 45
        else:
            tmp = self.font.render(self.text, True, tuple(
                [min(255, gradient(i[1], i[0], self.anim_hover / 45)) for i in zip(self.text_color, self.color)]))

            pygame.draw.polygon(screen, tuple(
                [min(255, gradient(i[1], i[0], self.anim_hover / 45)) for i in zip(self.color, self.border_color)]), (
                                    [self.x - self.height * sin(45) - self.anim_hover, self.y], [width, self.y],
                                    [width, self.y + self.height], [self.x - self.anim_hover, self.y + self.height]), 0)
            screen.blit(tmp, (self.f_x - tmp.get_width() + self.width + render_scale(40), self.y + self.padding))
            self.anim_hover -= 2
            if self.anim_hover <= 1:
                self.anim_hover = 1

    def set_on_click(self, func, but: int, *args):
        self.on_click_set[but - 1] = [True, func, args]


in_menu = True


def main_menu():
    global running, in_menu

    def exits():
        global in_menu
        in_menu = False

    title_font = pygame.font.Font('font.ttf', render_scale(100))
    tmp = title_font.render('Spatium altum', True, (250, 250, 250))

    a = MainMenuButton(1, 'Играть')
    b = MainMenuButton(2, 'Настройки')
    c = MainMenuButton(3, 'Выход')
    c.set_on_click(exits, 1)
    bg_surf = pygame.image.load("bg-mainmenu.png").convert_alpha()
    # bg_surf.set_colorkey((0, 0, 0))
    bg_surf.set_alpha(200)
    bg_surf = pygame.transform.scale(bg_surf, (int(1000 * COF), int(1000 * COF)))

    bg_surf2 = pygame.image.load("bg-mainmenu.png").convert_alpha()
    bg_surf2 = pygame.transform.scale(bg_surf2, (int(1000 * COF), int(1000 * COF)))
    bg_surf2.set_alpha(100)

    move = [width // 2 - render_scale(100), width // 2 + width - render_scale(100)]
    move2 = [width // 2, width // 2 + width]
    start = None
    count = 0
    while in_menu:


        screen.fill((0, 0, 0))
        bg_rect = bg_surf.get_rect(center=(move[0], height // 2))
        bg_rect2 = bg_surf.get_rect(center=(move[1], height // 2))
        bg_rect1_1 = bg_surf2.get_rect(center=(move2[0], height // 2 - render_scale(6)))
        bg_rect1_2 = bg_surf2.get_rect(center=(move2[1], height // 2 + render_scale(6)))

        start_time = time.time()
        screen.blit(bg_surf2, bg_rect1_1)
        screen.blit(bg_surf2, bg_rect1_2)
        screen.blit(bg_surf, bg_rect)
        screen.blit(bg_surf, bg_rect2)
        print("--- %s seconds ---" % (time.time() - start_time))
        print(COF)
        count += 1
        if count >= 1000000:
            count = 0
        if count % 2 == 0:
            move = [i - render_scale(1) for i in move]

            for i, j in enumerate(move):
                if j < -(width // 2):
                    move[i] = width // 2 + width

        if count % 5 == 0:
            move2 = [i - render_scale(1) for i in move2]

            for i, j in enumerate(move2):
                if j < -(width // 2):
                    move2[i] = width // 2 + width

        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                in_menu = False
                running = False

        screen.blit(tmp, (width // 2 - render_scale(290), height // 2 - render_scale(170)))

        a.draw(ev)
        b.draw(ev)
        c.draw(ev)

        clock.tick(fps)
        pygame.display.flip()



aa = False
if __name__ == '__main__':

    running = False
    main_menu()
    while running:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos
                    aa = True

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
