# ---------- CONSTANTS ----------
TYPE_BLOCKS = {1: 'grass', 2: 'stone', 3: 'sand'}
FULLSCREEN = False
MAP_COF = 1.3
WORLD_SIZE = {'small': 100, 'medium': 250, 'large': 500}
WORLD_NOISE_SIZE = 50
BLOCK_SIZE = MAP_COF * 32

# ---------- VARIABLES ----------
fonts = create_fonts([32, 16, 14, 8])
map_cords = [0, 0]
fps = 60
clock = pygame.time.Clock()

# ---------- INIT ----------
if FULLSCREEN:
    size = width, height = get_monitors()[0].width, get_monitors()[0].height
    COF = width / 640
    screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    COF = 2
    size = width, height = int(640 * COF), int(360 * COF)
    screen = pygame.display.set_mode(size)

pygame.display.set_caption('World')
pygame.mouse.set_cursor((16, 16), (0, 0), (
    135, 135, 135, 135, 135, 41, 41, 41, 41, 41, 41, 41, 41, 135, 122, 135, 41, 41, 41, 41, 41, 41, 41, 41, 135, 110,
    116,
    41, 41, 41, 41, 41), (64, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 128, 254, 0,
                          239,
                          0, 79, 0, 7, 128, 7, 128, 3, 0))

# ---------- TEXTURES ----------
# Загрузка текстур фундаментальных блоков
tmp_block_textures = [pygame.image.load('res/image/block/none.jpg').convert(), pygame.image.load(
    'res/image/block/grass.png').convert(),
                      pygame.image.load('res/image/block/stone.png').convert(),
                      pygame.image.load('res/image/block/sand.png').convert(), pygame.image.load(
        'res/image/block/water.png').convert()]
for num, el in enumerate(tmp_block_textures):
    tmp_block_textures[num] = pygame.transform.scale(el, (map_scale(32), map_scale(32)))

# Загрузка текстур сущьностей
tttt = Image.open('res/image/entities/player/main.png')
tmp_player_textures = {
    "stand": pygame.transform.scale(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
                                    [round(x * MAP_COF * 1.3) for x in tttt.size])}

tttt = Image.open('res/image/entities/player/swim.png')
tmp_player_textures.update({
    "swim": pygame.transform.scale(pygame.image.fromstring(tttt.tobytes("raw", 'RGBA'), tttt.size, 'RGBA'),
                                   [round(x * MAP_COF * 1.3) for x in tttt.size])})

tmp_player_move_textures = {"go": []}
for num, el in enumerate(split_sprites('res/image/entities/player/move.png')):
    tmp_player_move_textures['go'].append(pygame.transform.scale(el, [round(x * MAP_COF * 1.3) for x in el.get_size()]))
tmp_player_textures.update(tmp_player_move_textures)

tmp_player_move_textures = {"fly": []}
for num, el in enumerate(split_sprites('res/image/entities/player/fly.png')):
    tmp_player_move_textures['fly'].append(
        pygame.transform.scale(el, [round(x * MAP_COF * 1.3) for x in el.get_size()]))
tmp_player_textures.update(tmp_player_move_textures)

tmp_clothes_textures = {}

for texture in os.listdir(r'res\image\clothes'):
    tmp_clothes_textures.update({texture: load_textures(r"res/image/clothes/" + texture, MAP_COF)})
# Общая сборка
TEXTURES = {'block': tmp_block_textures,
            'player': tmp_player_textures,
            'none': pygame.image.load('res/image/block/none.jpg').convert(),
            'clothes': tmp_clothes_textures}
# save_s(TEXTURES['player']['stand'])
# ---------- WORK SPASE ----------
pl = Player(TEXTURES['player'], (width // 2, height // 2), 7)
frame_pass, frame_counter = True, False

start_time_m = time.time()
tmp = World(0, (0, 0), 10)
# noise_random.seed(10)

# pprint(TEXTURES['clothes']["viser"])
# hren = list()
# for i in pygame.image.tostring(pygame.image.load('res/image/clothes/viser/item.png').convert(), "RGB", False)[::3]:
#     hren.append(i)
#     print(pygame.image.load('res/image/clothes/viser/item.png').convert().get_size())
# from pyperclip import copy as cop
# cop(str(tuple(hren)))
tmp.init()
tmp.add_item(Item(pygame.image.load(r'res\image\items\0025.jpg').convert_alpha(), (10, 10), 0, ['fsdf', 'afsdf']))
ui = UI(100)
# tmp.save_world()
print("--- %s seconds --- MAIN" % (time.time() - start_time_m))
print(len(tmp.get_world()))
for i in tmp.get_world():
    print(i)
if __name__ == '__main__':

    player_state = Indicator(pl)
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
                    pause_break.pause()
                    # tmp.move_visible_area(3)
                elif event.key == pygame.K_TAB:
                    inventory.inventory([it.get_item() for it in pl.wear_clothes])
            elif event.type == pygame.MOUSEMOTION:
                pass
                # pl.move(event.rel)
        xx = pl.cords[0]
        yy = pl.cords[1]

        if map_cords[0] < -map_scale(510):
            tmp.move_visible_area(1)
            map_cords[0] += map_scale(510)

        elif map_cords[0] > map_scale(510):
            tmp.move_visible_area(2)
            map_cords[0] -= map_scale(510)

        if map_cords[1] < -map_scale(510):
            tmp.move_visible_area(3)
            map_cords[1] += map_scale(510)

        elif map_cords[1] > map_scale(510):
            tmp.move_visible_area(4)
            map_cords[1] -= map_scale(510)

        pl.tick()

        # Рендер основного окна
        if frame_pass:
            if frame_counter:
                screen.fill((47, 69, 56))
                tmp.render(screen)
                screen.blit(pl.image, pl.rect)
                display_fps()
                # a = pygame.font.Font(None, 35)
                # a = a.render(str(pl.print_cord()), True, (250, 255, 255))
                # screen.blit(a, (10, 690))
                ui.render(screen, pl.hp)
                pygame.display.flip()
            frame_counter = not frame_counter
            clock.tick(fps)

    pygame.quit()  # Завершение работы
