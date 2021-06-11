# ---------- IMPORTS ----------
from screeninfo import get_monitors

from lib.vars import *
from res.textures import TEXTURES

# ---------- INIT ----------
screen = pygame.surface.Surface((640, 360))
frame_pass, frame_counter = True, False

if FULLSCREEN:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    render_screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    size = width, height = 640 * SCALE_COF, 360 * SCALE_COF
    render_screen = pygame.display.set_mode(size)

pygame.display.set_caption('Game')

# ---------- WORK SPACE ----------
# pl = Player(TEXTURES['player'], (width // 2, height // 2), 7)

# start_time_m = time.time()
# tmp = World(0, (0, 0), 10)
# noise_random.seed(10)

# pprint(TEXTURES['clothes']["viser"])
# hren = list()
# for i in pygame.image.tostring(pygame.image.load('res/image/clothes/viser/item.png').convert(), "RGB", False)[::3]:
#     hren.append(i)
#     print(pygame.image.load('res/image/clothes/viser/item.png').convert().get_size())
# from pyperclip import copy as cop
# cop(str(tuple(hren)))
# tmp.init()
# tmp.add_item(Item(pygame.image.load(r'res\image\items\0025.jpg').convert_alpha(), (10, 10), 0, ['fsdf', 'afsdf']))
# ui = UI(100)
# tmp.save_world()
# print("--- %s seconds --- MAIN" % (time.time() - start_time_m))
# print(len(tmp.get_world()))
# for i in tmp.get_world():
#    print(i)

# player_state = Indicator(pl)
# player_state.save_s()

main_running = True
while main_running:
    # pl.print_cord()
    # world_noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=random.randint(1, 55))
    # tmp = World(0, (0, 0))
    # tmp.init()
    # raise Exception("hui")

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            main_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cords = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_ESCAPE:
                # pause_break.pause()
                # tmp.move_visible_area(3)
                pass
            elif event.key == pygame.K_TAB:
                # inventory.inventory([it.get_item() for it in pl.wear_clothes])
                pass
        elif event.type == pygame.MOUSEMOTION:
            pass
            # pl.move(event.rel)

    if map_cords[0] < -256:
        # tmp.move_visible_area(1)
        map_cords[0] += 256

    elif map_cords[0] > 256:
        # tmp.move_visible_area(2)
        map_cords[0] -= 256

    if map_cords[1] < -256:
        # tmp.move_visible_area(3)
        map_cords[1] += 256

    elif map_cords[1] > 256:
        # tmp.move_visible_area(4)
        map_cords[1] -= 256

    # pl.tick()

    # Рендер основного окна
    if frame_pass:
        if frame_counter:
            render_screen.fill((47, 69, 56))
            # tmp.render(screen)
            # screen.blit(pl.image, pl.rect)
            display_fps(render_screen, clock)
            # a = pygame.font.Font(None, 35)
            # a = a.render(str(pl.print_cord()), True, (250, 255, 255))
            # screen.blit(a, (10, 690))
            # ui.render(screen, pl.hp)
            pygame.display.flip()
        frame_counter = not frame_counter
        clock.tick(fps)

pygame.quit()  # Завершение работы

# Таймер для подсчета работы кода
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))
