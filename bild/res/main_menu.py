from lib.vars import *
from res.textures import TEXTURES, render_screen, size, height, width, SCALE_COF
from lib.ui import Button, TitleLossButton, submit_window


def main_menu():
    frame_pass, frame_counter = True, False
    buttons = [Button('default_big', 'Выйти', (10, 146), 130),
               Button('default_big', 'Новая игра', (180, 146), 130),
               TitleLossButton('play_button', (145, 146)),
               TitleLossButton('settings_button', (280, 10))]

    render_screen = pygame.display.get_surface()
    background = pygame.image.load('res/textures/gui/main_menu/backgrounds/1.png').convert()

    screen = pygame.surface.Surface((320, 180))
    buttons[0].set_on_click(submit_window, 1, screen, "Вы действительно хотите выйти?", exit, "Выход")

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
