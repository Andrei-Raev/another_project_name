import pygame


class Button:
    def __init__(self, color: (int, int, int), border_color: (int, int, int), text_color: (int, int, int), x: int,
                 y: int, padding: int, border: int,
                 text: str, text_size, surf):
        self.color = color
        self.surf = surf
        self.font = pygame.font.SysFont('comic sans ms', text_size)

        self.border_color = border_color
        self.x = x
        self.y = y
        self.padding = padding
        self.text = str(text)
        self.text_color = text_color
        tmp = self.font.render(self.text, True, self.text_color)
        self.height = padding * 2 + tmp.get_height()
        self.width = padding * 2 + tmp.get_width()
        self.border_width = border
        self.cords = (0, 0)

        self.anim_hover = 0

        self.on_click_set = [[False], [False], [False]]

    def draw(self, ev):
        for event in ev:
            if event.type == pygame.MOUSEMOTION:
                self.cords = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.on_click_set[0][0]:
                    self.on_click_set[0][1](*self.on_click_set[0][2])
                elif event.button == 2 and self.on_click_set[1][0]:
                    self.on_click_set[1][1](*self.on_click_set[1][2])
                elif event.button == 3 and self.on_click_set[2][0]:
                    self.on_click_set[2][1](*self.on_click_set[2][2])

        if self.x <= self.cords[0] <= self.x + self.width and self.y < self.cords[1] < self.x + self.height:
            tmp = self.font.render(self.text, True, tuple(int(min(i + self.anim_hover, 255)) for i in self.text_color))
            pygame.draw.rect(self.surf, tuple(int(min(i + self.anim_hover, 255)) for i in self.border_color), (
                self.x - self.border_width, self.y - self.border_width, self.width + 2 * self.border_width,
                self.height + 2 * self.border_width), 0, 5)
            pygame.draw.rect(self.surf, tuple(min(i + self.anim_hover, 255) for i in self.color),
                             (self.x, self.y, self.width, self.height), 0, 5)
            self.surf.blit(tmp, (self.x + self.padding, self.y + self.padding))

            self.anim_hover += 3
            if self.anim_hover >= 45:
                self.anim_hover = 45
        else:
            tmp = self.font.render(self.text, True, tuple(int(min(i + self.anim_hover, 255)) for i in self.text_color))
            pygame.draw.rect(self.surf, tuple(int(i + self.anim_hover) for i in self.border_color), (
                self.x - self.border_width, self.y - self.border_width, self.width + 2 * self.border_width,
                self.height + 2 * self.border_width), 0, 5)
            pygame.draw.rect(self.surf, tuple(min(i + self.anim_hover, 255) for i in self.color),
                             (self.x, self.y, self.width, self.height), 0, 5)
            self.surf.blit(tmp, (self.x + self.padding, self.y + self.padding))

            self.anim_hover -= 1
            if self.anim_hover <= 1:
                self.anim_hover = 1

    def set_on_click(self, func, but: int, *args):
        self.on_click_set[but - 1] = [True, func, args]
