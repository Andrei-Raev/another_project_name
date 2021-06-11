import pygame


# ---------- BLOCKS ----------

# -------------
# |   Блоки   |
# -------------


class Obekt:
    def __init__(self, cord: tuple, preor=0):
        self.cord = cord
        self.importance = preor

    def get_x(self) -> int:
        return int(self.cord[0])

    def get_y(self) -> int:
        return int(self.cord[1])

    def get_preor(self) -> int:
        return int(self.importance)

    def get_cord(self) -> tuple:
        return tuple(self.cord)


class Landscape(Obekt):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 0

    def get_texture(self):
        return TEXTURES['block'][self.get_type()]

    def get_super_texture(self):
        return TEXTURES['block'][self.get_type()]


class Grass(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 1


class Stone(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 2


class Sand(Landscape):
    def __init__(self, cord: tuple, importance=1):
        super().__init__(cord, importance)

    @staticmethod
    def get_type() -> int:
        return 3


class Water(Landscape):
    def __init__(self, cord: tuple, water_level: int, importance=1):
        super().__init__(cord, importance)
        self.water_level = water_level

    @staticmethod
    def get_type() -> int:
        return 4

    def get_super_texture(self):
        cof = (2 * (self.water_level + 16000) / 20000)
        return dark(TEXTURES['block'][4], cof)


# -------------------
# |   Конец Блоки   |
# -------------------

# ---------- ENTITIES ----------
class Entity(pygame.sprite.Sprite):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):  #: pygame.AbstractGroup):
        super().__init__(*groups)

        self.hp = 100

        self.cords = cords
        try:
            self.image = texture['stand']
        except:
            self.image = texture
        self.textures = texture
        self.move_anim = 0
        self.rect = self.image.get_rect(center=self.cords)
        self.speed = ((32 * MAP_COF) * speed)
        self.isgoing = False
        self.rotate = False
        self.fly = False
        self.main_speed = ((32 * MAP_COF) * speed)
        self.counter = 0

    def move(self, delta_cords):
        self.cords = [self.cords[0] + delta_cords[0], self.cords[1] + delta_cords[1]]
        self.rect = self.image.get_rect(center=self.cords)

    def go(self, direct: int in [1, 2, 3, 4]):
        if direct == 1:
            self.move((0, self.speed // fps))
        elif direct == 2:
            self.move((0, -(self.speed // fps)))
        elif direct == 3:
            self.move((self.speed // fps, 0))
        elif direct == 4:
            self.move((-(self.speed // fps), 0))

    def get_cord(self, relative=True):
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        if relative:
            return get_relative_coordinates(x, y)
        else:
            return x, y

    def print_cord(self):
        global map_cords
        # print(tmp.center_chunk_cord)
        x = round((self.cords[0] - map_cords[0]) / BLOCK_SIZE) + tmp.center_chunk_cord[1] * 16
        y = round((self.cords[1] - map_cords[1]) / BLOCK_SIZE) + tmp.center_chunk_cord[0] * 16
        return 'x = ' + str(x) + ', ' + 'y = ' + str(y)


class Item(Entity):
    def __init__(self, texture: list, cords: tuple, speed: float, item_info: list, *groups):
        super().__init__(texture, cords, speed, *groups)
        self.title = item_info[0]
        self.info = item_info

    def get_world_item(self):
        return self.textures, self.cords

    def render(self, surf, ccc):
        ccc1 = copy(ccc)
        ccc = ccc1[0] + 1, ccc1[1] + 1
        pygame.draw.circle(surf, (0, 0, 0),
                           ((self.rect.x + ccc[0] * map_scale(510)), (self.rect.y + ccc[1] * map_scale(510))), 100)
        surf.blit(self.image, self.rect)
        print(self.rect)
        # save_s(surf)


class Player(Entity):
    def __init__(self, texture: list, cords: tuple, speed: float, *groups):

        super().__init__(texture, cords, speed, *groups)

        self.hp = 150
        self.max_hp = self.hp

        self.vitality = 500
        self.max_vitality = self.vitality

        self.vitality = 100
        self.wear_clothes = [Dress('Стандартный визер', TEXTURES['clothes']['viser'])]
        self.mode = 'stand'

    def tick(self):
        if self.vitality > self.max_vitality:
            self.vitality = self.max_vitality
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        self.fly = False
        self.isgoing = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotate = True
            if self.cords[0] > width - width // 5:
                map_cords[0] -= self.speed // fps
            else:
                self.go(3)

            self.isgoing = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotate = False
            if self.cords[0] < width // 5:
                map_cords[0] += self.speed // fps
            else:
                self.go(4)

            self.isgoing = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.cords[1] > height - height // 5:
                map_cords[1] -= self.speed // fps
            else:
                self.go(1)

            self.isgoing = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.cords[1] < height // 5:
                map_cords[1] += self.speed // fps
            else:
                self.go(2)

            self.isgoing = True

        if keys[pygame.K_LSHIFT]:
            self.fly = True

        if self.fly:
            self.mode = 'fly'

            self.vitality -= 1
            self.speed = self.main_speed * 1.3

            if self.move_anim > 9:
                self.move_anim = 0
            self.image = self.textures['fly'][self.move_anim]

            if self.counter > 3:
                self.move_anim += 1
                self.counter = 0
            self.counter += 1
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)

        elif not self.isgoing:
            self.mode = 'stand'

            self.vitality += 1
            if self.hp > 100:
                self.hp = 100

            self.image = self.textures['stand']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.vitality += 1
            self.mode = 'move'
            self.speed = self.main_speed

            self.counter += 1
            if self.counter == 2:
                self.move_anim += 1
                self.counter = 0
            elif self.counter > 3:
                self.counter = 0

            if self.rotate:
                self.image = pygame.transform.flip(self.textures['go'][self.move_anim - 1], True, False)
            else:
                self.image = self.textures['go'][self.move_anim - 1]

            if self.move_anim > 15:
                self.move_anim = 0
                self.isgoing = False

        if tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Water' and not self.fly:
            self.mode = 'swim'
            self.speed = self.main_speed * 0.6
            self.image = self.textures['swim']
            if self.rotate:
                self.image = pygame.transform.flip(self.image, True, False)
        elif tmp.get_block(self.get_cord(False)).__class__.__name__ == 'Stone':
            pass
        self.image = copy(self.image)
        for item in self.wear_clothes:
            item.render(self.image, self.mode, self.move_anim, self.rotate)
        # else:
        #    self.speed = 7
        # self.image.fill((0, 0, 0))

    def get_texture(self) -> pygame.surface.Surface:
        image = self.textures['stand']

        image = copy(image)
        for item in self.wear_clothes:
            item.render(image, self.mode, self.move_anim, self.rotate)

        return image


#
#
#
#


# ---------- WORLD ----------


class World:  # Класс мира
    def __init__(self, world_seed, center_chunk_cord, seed):
        self.world_seed = world_seed
        self.chunks = set()
        self.center_chunk_cord = center_chunk_cord
        noise_random.seed(seed)
        self.noise = PerlinNoiseFactory(2, octaves=4, unbias=False, seed=seed)

    def init(self):
        for y in range(-1, 2):
            for x in range(-1, 3):
                self.chunks.add(
                    Chunk(seed_from_cord(x, y), (x + self.center_chunk_cord[0], y + self.center_chunk_cord[1])))

        for i in self.chunks:
            i.generate_chunk(self.noise)
            # i.load()
            i.render_chunk()

    def add_chunk(self, cord):
        self.chunks.add(Chunk(seed_from_cord(*cord), cord))

    def del_chunk(self, cord):
        for i in self.chunks:
            if i.get_cord() == cord:
                self.chunks.remove(i)
                break

    def render(self, surf):
        wid = 510 * MAP_COF
        tmp_world_surf = pygame.Surface((map_scale(510) * 4, map_scale(510) * 3))
        tmp_items = list()

        for y in range(-1 + self.center_chunk_cord[1], 3 + self.center_chunk_cord[1]):
            for x in range(-1 + self.center_chunk_cord[0], 2 + self.center_chunk_cord[0]):
                chunk_cord = tuple([x, y])
                try:
                    chunk_surf = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_s()
                    tmp_items += list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0].get_items()
                except IndexError:
                    # raise ValueError(f'Chunk ({chunk_cord}) not found!')
                    self.chunks.add(Chunk(seed_from_cord(*chunk_cord), chunk_cord))
                    tmp_chunk = list(filter(lambda i: i.get_cord() == chunk_cord, self.chunks))[0]
                    tmp_chunk.generate_chunk(self.noise)
                    tmp_chunk.render_chunk()
                    chunk_surf = tmp_chunk.get_s()
                    # save_s(chunk_surf)

                tmp_world_surf.blit(chunk_surf, ((chunk_cord[1] - self.center_chunk_cord[1]) * wid + wid,
                                                 (chunk_cord[0] - self.center_chunk_cord[0]) * wid + wid))

        for item in tmp_items:
            item.render(tmp_world_surf, self.center_chunk_cord)
            # print(item)
            # tmp_world_surf.fill((0,0,0))

        surf.blit(tmp_world_surf, [i - map_scale(510) for i in map_cords])

    def get_block(self, cords):
        try:
            block_cord, chunk_cord = get_relative_coordinates(*cords)
            tmp_chunk = list(filter(lambda x: x.get_cord() == chunk_cord[::-1], self.chunks))[0]
            tmp_block = list(filter(lambda x: x.get_cord() == block_cord, tmp_chunk.board['landscape']))[0]
            return tmp_block
        except IndexError:
            return None

    def add_item(self, item: Item):
        chunk_cord = item.get_cord()[1]
        tmp_chunk = list(filter(lambda x: x.get_cord() == chunk_cord, self.chunks))[0]
        tmp_chunk.board['entities']['items'].add(item)

    def move_visible_area(self, direction: int):  # 1 - вверх, 2 - вниз, 3 - влево, 4 - вправо
        if direction == 1:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] + 1)
        elif direction == 2:
            self.center_chunk_cord = (self.center_chunk_cord[0], self.center_chunk_cord[1] - 1)
        elif direction == 3:
            self.center_chunk_cord = (self.center_chunk_cord[0] + 1, self.center_chunk_cord[1])
        elif direction == 4:
            self.center_chunk_cord = (self.center_chunk_cord[0] - 1, self.center_chunk_cord[1])

    def load_world(self, file):
        pass

    def save_world(self):
        for i in self.chunks:
            i.save(f'save_data/{i.get_cord()}.ch')

    def get_world(self):
        q = []
        for i in range(len(self.chunks) * 2):
            q.append([])
        for i in self.chunks:
            i = str(i)
            for g in range(16):
                for j in range(16):
                    if 'Water' in i.split(', ')[g * j]:
                        q[g].append(1)
                    else:
                        q[g].append(0)
        return q


class Chunk:  # Класс чанка мира
    def __init__(self, seed: int, cord: (int, int)):
        self.seed = seed
        self.cord = cord

        self.board = {'landscape': set(), 'buildings': {}, 'mechanisms': {}, 'entities': {'items': {}}}
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))

    def generate_chunk(self, world_noise) -> None:
        del self.board
        self.board = {'landscape': set(), 'buildings': set(), 'mechanisms': {}, 'entities': {'items': set()}}
        for y in range(16):
            for x in range(16):
                tmp_noise = world_noise((x + (self.cord[1]) * 16) / WORLD_NOISE_SIZE,
                                        (y + (self.cord[0]) * 16) / WORLD_NOISE_SIZE)
                self.board['landscape'].add(block_constructor(tmp_noise, (x, y)))

    def render_chunk(self) -> None:
        del self.ground
        self.ground = pygame.Surface((map_scale(510), map_scale(510)))
        self.ground.fill((55, 5, 4))
        for i in self.board['landscape']:
            cord = i.get_cord()
            tmp_texture = i.get_texture()
            block_rect = tmp_texture.get_rect(topleft=(tuple([j * 32 * MAP_COF for j in cord])))
            self.ground.blit(tmp_texture, block_rect)
            del cord, i, block_rect
        # simple_chunk_texture_generation(self)

        # f = pygame.font.Font(None, 100)
        # r = f.render(f'{self.cord}', True,(255,255,255))
        # self.ground.blit(r, (50,50))

        # f = pygame.font.Font(None, 250)
        # t = f.render(f'{self.cord}', True, (255, 255, 255))
        # self.ground.blit(t, (25, 25))

    def get_items(self) -> list:
        return self.board['entities']['items']

    def get_s(self):
        return self.ground

    def get_cord(self):
        return tuple(self.cord)

    def __str__(self):
        return str(self.board['landscape'])

    def load(self):
        self.board = decode_chunk(self.cord)

    def update(self, data):
        pass

    def save(self, name_f):
        raw = b''

        for i in self.board['landscape']:
            raw += i.get_type().to_bytes(1, byteorder="little")
            raw += cord_codec(i.get_cord())

        with open(name_f, 'wb') as byte_file:
            byte_file.write(raw)


def cord_codec(cors: tuple) -> bytes:
    raw = b''
    for i in cors:
        raw += i.to_bytes(1, byteorder="little")
    return raw


def decode_chunk(file_path):
    board = {'landscape': set()}
    with open(f'save_data/{file_path}.ch', 'rb') as byte_file:
        chunk_raw = byte_file.read()
        for i in range(len(chunk_raw) // 3):
            tmp_type = chunk_raw[i * 3]
            tmp_cord_x = int.from_bytes(chunk_raw[i * 3 + 1:i * 3 + 2], 'little')
            tmp_cord_y = int.from_bytes(chunk_raw[i * 3 + 2:i * 3 + 3], 'little')
            if tmp_type == 1:
                board['landscape'].add(Grass((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 2:
                board['landscape'].add(Stone((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 3:
                board['landscape'].add(Sand((tmp_cord_x, tmp_cord_y)))
            elif tmp_type == 4:
                board['landscape'].add(Water((tmp_cord_x, tmp_cord_y), 20000))
    return board


def simple_chunk_texture_generation(chunk):
    tmp_ground = pygame.Surface((map_scale(510), map_scale(510)))
    tmp_ground.fill((0, 0, 0, 0))
    tmp_textures = []
    for i in chunk.board['landscape']:
        if type(i) == Water:
            tmp_textures.append([pygame.image.tostring(i.get_texture(), "RGBA", False),
                                 i.get_texture().get_rect(topleft=(tuple([j * 32 * MAP_COF for j in i.get_cord()]))),
                                 (2 * (i.water_level + 16000) / 20000)])
    if not len(tmp_textures):
        return
    for num, el in enumerate(tmp_textures):
        tmp_img = Image.frombytes("RGBA", (32, 32), el[0])
        tmp_img = dark(tmp_img, el[2])

    chunk.ground = tmp_ground

# Собирает блок по координатам и весу точки: [-1; 1]
def block_constructor(cof: float, c_cords: tuple):
    if -0.5 <= cof <= 0.5:  # ----------------| Нормализует веса
        cof = cof * 1.8  # -------------------|
    else:  # ---------------------------------|
        if cof > 0:  # -----------------------|
            cof = (cof - 0.5) * 0.2 + 0.9  # -|
        else:  # -----------------------------|
            cof = (cof + 0.5) * 0.2 - 0.9  # -|

    cof += .25  # Осушает мир

    # Алгоритм генерации блока
    if cof <= 0:  # Уровень воды - 0. Если что-то ниже, это считается водой
        return Water(c_cords, round(20000 * abs(cof)))
    else:
        if 0 <= cof < 0.1:
            return Sand(c_cords)  # Пляж
        elif 0.1 <= cof < 0.35:
            return Grass(c_cords)  # Луга
        elif 0.35 <= cof < 0.5:
            return Grass(c_cords)  # Равнины
        elif 0.5 <= cof < 0.85:
            return Stone(c_cords)  # Горы
        else:
            return Stone(c_cords)  # Снег в горах

