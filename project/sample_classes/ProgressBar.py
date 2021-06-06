import pygame


class Game_error(Exception):
    pass


class Value_error(Game_error):
    pass


pygame.init()


class Progress_bar:
    def __init__(self, color: (int, int, int), border_color: (int, int, int), bg_color: (int, int, int), x: int, y: int,
                 height: int, width: int, border: int, border_radius: int, progress: int, max_progress=100):
        self.color = color
        self.border_radius = border_radius
        self.border_color = border_color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border_width = border
        self.progress = progress
        self.max_progress = max_progress
        self.bg_color = bg_color

        # self.cords = (0, 0)

        # self.anim_hover = 0

        # self.on_click_set = [[False], [False], [False]]

    def draw(self, *_):
        pygame.draw.rect(screen, self.border_color,
                         (self.x - self.border_width, self.y - self.border_width, self.width + 2 * self.border_width,
                          self.height + 2 * self.border_width), 0, self.border_radius)
        pygame.draw.rect(screen, self.bg_color,
                         (self.x, self.y, self.width, self.height), 0, self.border_radius)
        len_prog = self.width // self.max_progress * self.progress
        if self.progress == self.max_progress:
            len_prog = self.width
        if self.progress:
            pygame.draw.rect(screen, self.color,
                             (self.x, self.y, len_prog, self.height), 0, self.border_radius)

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


a = Progress_bar((124, 189, 224), (66, 154, 198), (34, 60, 94), 100, 100, 50, 300, 5, 7, 0)

if __name__ == '__main__':
    size = width, height = 500, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('test')

    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cords = event.pos
        a.add_progress(0.1)

        a.draw(ev)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
