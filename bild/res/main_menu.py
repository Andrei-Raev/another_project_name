from lib.vars import *
from res.textures import TEXTURES, render_screen, size, height, width, SCALE_COF
from lib.ui import Button


def main_menu():
    frame_pass, frame_counter = True, False
    buttons = [Button('default_big', 'Новая игра', (10, 146), 140),
               Button('default_big', 'Загрузить игру', (170, 146), 140)]

    render_screen = pygame.display.get_surface()
    background = pygame.transform.scale(pygame.image.load('res/textures/gui/main_menu/backgrounds/0.png').convert(),
                                        (320, 180))

    screen = pygame.surface.Surface((320, 180))

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
