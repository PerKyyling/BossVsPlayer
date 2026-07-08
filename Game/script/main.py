import astar_lib
import pygame
import math
import sys
from random import *

from drivers import GamepadDriver

from algor import *

gamepad = GamepadDriver()
pygame.mixer.init()
pygame.mixer.music.load('music/horror_music.mp3')
pygame.mixer.music.play(loops=-1, start=0.0)


#_______________________Настройки экрана и графики________________________
WIDTH = 960
HEIGHT = 960
FPS =  30
#_______________________Настройки экрана и графики________________________

# ____________________________Настройки лучей_____________________________
count = 140# Количество лучей (чем больше, тем выше качество 3D)
arch = 60  # Поле зрения в градусах
width = 1
# ____________________________Настройки лучей_____________________________

flag_zel = True
bl_visit = True
bl_not_visit = False
coord_exit_y = 7
coord_exit_x = 73

point_color = (0, 255, 21)

werx_rect_color = (50, 55, 70)
niz_rect_color = (35, 35, 35)

# (155, 155, 155)
# (25, 25, 25)

# (50, 55, 70)
# (35, 35, 35)
boss_speed = 6
mapa = 60
ang1 = 0.1
x_kv = 15
y_kv = 15

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ты убогий")
clock = pygame.time.Clock()

ang = 1.0
running = True

rect_mas = []
rect_mas1 = []
trig = []
boss = []

pror = 1500
boss_move_flag = 0
def reset_level():
    global map_new, map, rect_mas, rect_mas1, t_mas, boss, player
    global boss_x, boss_y, count_points, count_s_points, coord_exit_x, coord_exit_y
    global count_door, trig, boss_instruction, boss_step_index, boss_move_flag
    global bl_visit, bl_not_visit, boss_visible, boss_invisible, flag_for_event
    global player_tile, boss_tile, old_pl_pos, old_bs_pos, boss_target_x, boss_target_y
    global boss_is_walking, boss_action_timer
    
    # 1. Генерируем новую карту
    width = 74
    height = 17
    map_new = gen_map(width, height, 1, 1, width-2, height-2)
    
    map = map_new.copy()
    
    # 2. Обновляем координаты выхода
    coord_exit_y = None
    coord_exit_x = None
    for i in range(len(map_new)):
        for j in range(len(map_new[i])):
            if map_new[i][j] == 'V':
                coord_exit_y = i
                coord_exit_x = j
                break
        if coord_exit_x is not None:
            break
    
    # 3. Очищаем старые массивы
    rect_mas.clear()
    rect_mas1.clear()
    t_mas.clear()
    trig.clear()
    boss.clear()
    
    # 4. Заполняем новыми данными из map_new
    for y in range(len(map_new)):
        for x in range(len(map_new[y])):
            char = map_new[y][x]
            if char == '1':
                rect_mas.append(pygame.Rect(mapa * x, mapa * y, mapa, mapa))
            elif char == 'P':
                # Позиция игрока
                player.x = mapa * x + (mapa - x_kv) // 2
                player.y = mapa * y + (mapa - y_kv) // 2
            elif char == 'B':
                # Позиция босса
                boss_x = x * mapa + mapa // 2
                boss_y = y * mapa + mapa // 2
                boss.append(pygame.Rect(x * mapa, y * mapa, mapa, mapa))
            elif char == '.':
                # Добавляем тайлы для новой карты
                t_mas.append((x * mapa, y * mapa))
    
    # 5. Обновляем переменные тайлов
    player_tile = None
    boss_tile = None
    old_pl_pos = (player.x, player.y)
    old_bs_pos = (boss_x, boss_y)
    
    # 6. Обновляем счетчики
    count_points = len(rect_mas1)
    count_s_points = 0
    count_door = 0
    
    # 7. Сбрасываем флаги босса
    boss_move_flag = 0
    boss_visible = False
    boss_invisible = True
    bl_visit = True
    bl_not_visit = False
    flag_for_event = 0
    count_event = 0
    
        # 8. Сбрасываем состояние движения босса
    boss_target_x = boss_x
    boss_target_y = boss_y
    boss_is_walking = False
    boss_action_timer = 0
    boss_step_index = 0  # Добавьте эту строку
    boss_instruction = ""  # Добавьте эту строку
    
    # 9. Пересчитываем путь для босса
    find_path()

def gen_map(width = 74, height = 17, pi = 1, pj = 1, bi = 2 , bj = 2):
    stack = []
    start_maze_x = 1; start_maze_y = 1

    maze = [[1] * width for _ in range(height)]
    maze[start_maze_y][start_maze_x] = 0

    stack.append((start_maze_x, start_maze_y))
    mas = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        cx, cy = stack[-1]
        nb = []

        for dx, dy in mas:
            nx, ny = cx + dx, cy + dy

            if (0 < nx < (width - 1)) and (0 < ny < (height - 1)) and maze[ny][nx] == 1:
                nb.append((nx, ny, dx, dy))

        if nb:
            nx, ny, dx, dy = choice(nb)
            maze[cy + dy // 2][cx + dx // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    maze[1][1] = 'P'
    maze[height - 2][width - 2] = 'B'
    for i in range(height):
        if maze[i][width - 2] == 0:
            maze[i][width - 1] = "V"
            coord_exit_y = i
            coord_exit_x = width - 1

    new = []

    for row in maze:
        # print("".join(['1' if cell == 1 else str(cell) for cell in row]))
        new.append("".join(['1' if cell == 1 else str(cell) for cell in row]))
    return new



width = 74; height = 17; pi = 1; pj = 1;  bi = width - 2; bj = height - 2

map_new = gen_map(width , height, pi, pj, bi, bj)



map = [
    "11111111111111111111111111111111111111111111111111111111111111111111111111",
    "1..................................................1....................B1",
    "1.....111111111......111111111......111111111......1.....................1",
    "1.....111111111......111111111......111111111......1.....................1",
    "1.....111111111......111111111......111111111......1.....................1",
    "1..................................................1.....................1",
    "1..................................................1.....................1",
    "1.......P................................................................V",
    "1..................................................1.....................1",
    "1..................................................1.....................1",
    "1..................................................1.....................1",
    "1..................................................1.....................1",
    "1.....111111111......111111111...........11........1.....................1",
    "1.....111111111......111111111........11111........1.....................1",
    "1.....111111111......111111111........1111.........1.....................1",
    "1..................................................1.....................1",
    "11111111111111111111111111111111111111111111111111111111111111111111111111"
]





#передвижение босса________________________________________________________

def boss_Right(boss_x, boss_y):
    boss_x += mapa
    return boss_x, boss_y

def boss_Left(boss_x, boss_y):
    boss_x -= mapa
    return boss_x, boss_y

def boss_UP(boss_x, boss_y):
    boss_y -= mapa
    return boss_x, boss_y

def boss_DOWN(boss_x, boss_y):
    boss_y += mapa
    return boss_x, boss_y

# передвижение босса________________________________________________________

count_points = 0
count_door = 0
timer = 0
boss_x, boss_y = 0, 0

for x_map in range(len(map)):
    for y_map in range(len(map[x_map])):
        if map[x_map][y_map] == '1':
            rect_mas.append(pygame.Rect(mapa * y_map, mapa * x_map, mapa, mapa))
        elif map[x_map][y_map] == 'P':
            x11 = mapa * y_map + (mapa - x_kv) // 2
            y11 = mapa * x_map + (mapa - y_kv) // 2

for x_map in range(len(map)):
    for y_map in range(len(map[x_map])):
        if map[x_map][y_map] == 'B':
            boss_x = y_map * mapa + mapa // 2
            boss_y = x_map * mapa + mapa // 2
            boss.append(pygame.Rect(y_map * mapa, x_map * mapa, mapa, mapa))


# добавил массив с тайламис _____________________
t_mas = []
for y_map in range(len(map)):
    for x_map in range(len(map[y_map])):


        if map[y_map][x_map] == '.':

            t_mas.append( ( x_map * mapa, y_map * mapa ) )

#
# _________________________ ____________________
boss_step_index=0
boss_instruction=""
boss_target_x = boss_x
boss_target_y = boss_y
boss_is_walking = False
player_tile = None
boss_tile = None

for x_map in range(len(map)):
    for y_map in range(len(map[x_map])):
        if map[x_map][y_map] == '*':
            rect_mas1.append(pygame.Rect(mapa * y_map, mapa * x_map, mapa, mapa))
            count_points += 1

for x_map in range(len(map)):
    for y_map in range(len(map[x_map])):
        if map[x_map][y_map] == '&':
            trig.append(pygame.Rect(mapa * y_map, mapa * x_map, mapa, mapa))

if len(trig) == 0 and len(rect_mas1) > 0 or len(trig) > 0 and len(rect_mas1) == 0:
    running = False; print('нет нужных триггеров')



player = pygame.Rect(x11, y11, x_kv, y_kv)

DIST_TO_PROJ_PLANE = (WIDTH / 2) / math.tan(math.radians(arch) / 2)
SCALE = WIDTH / count

try:
    boss_img = pygame.image.load('foto/photo_5366311489326750229_x.png').convert_alpha()
except:
    boss_img = pygame.Surface((64, 64))
    boss_img.fill((255, 0, 100))

boss_move_flag = 1
walk_timer = 0
count_s_points = 0
old_rast = 0


#____________________________________________________________________________


boss_visible = False
boss_invisible=True


#____________________________________________________________________________



# для игрока___________________________________________________

old_pl_pos = player.x, player.y

# для игрока___________________________________________________
# для босса____________________________________________________

old_bs_pos = boss_x, boss_y

# для босса____________________________________________________


POLL_EVENT = pygame.USEREVENT + 1

# Запускаем таймр: 20000 мс = 20 секунд
pygame.time.set_timer(POLL_EVENT, 20000)




'''py, px = int(player.x//mapa), int(player.y//mapa)
bx, by = int(boss_x//mapa), int(boss_y//mapa)

print(py,px,by,bx)
boss_path=(astar_lib.astar(map, py, px, by, bx))
print(boss_path)
# _______________________________________________________________________


boss_instruction = boss_path
boss_step_index = 0    '''     # Индекс текущего шага в инструкции
boss_action_timer = 0       # Отдельный таймер для шагов босса

boss_step_index=0
boss_instruction=""
# _______________________________________________________________________

try:
    chat_font = pygame.font.Font("8bitfont.otf", 16)
except:
    chat_font = pygame.font.SysFont("Arial", 16)


def find_path():
    global boss_step_index, boss_instruction

    # Используем map_new вместо map, и правильный порядок координат
    px, py = int(player.x // mapa), int(player.y // mapa)
    bx, by = int(boss_x // mapa), int(boss_y // mapa)
    
    # Важно: to_inst ожидает (map, start_y, start_x, end_y, end_x)
    boss_path = to_inst(map, py, px, by, bx)
    
    boss_instruction = boss_path
    boss_step_index = 0

find_path()

boss_target_x = boss_x
boss_target_y = boss_y
boss_is_walking = False


def draw_minimap():
    # Настройки миникарты
    MAP_SIZE = 200  # Размер квадрата миникарты в пикселях
    MAP_X = WIDTH - MAP_SIZE - 20  # Отступ 20px от правого края
    MAP_Y = 20  # Отступ 20px от верхнего края

    # Создаем отдельную поверхность (холст) для карты с поддержкой прозрачности
    minimap_surf = pygame.Surface((MAP_SIZE, MAP_SIZE), pygame.SRCALPHA)
    minimap_surf.fill((30, 30, 30, 200))  # Темный полупрозрачный фон (RGBA)

    # Масштаб: сколько игровых пикселей помещается в 1 пиксель миникарты
    # (Показывает область примерно 6х6 блоков вокруг игрока)
    ZOOM = 11.0

    # Центр миникарты на самом холсте
    half_size = MAP_SIZE // 2

    # 1. Рисуем стены лабиринта, сдвинутые относительно игрока
    for rect in rect_mas:
        # Вычисляем позицию стены относительно центра игрока
        rel_x = half_size + (rect.x - player.centerx) // ZOOM
        rel_y = half_size + (rect.y - player.centery) // ZOOM
        rel_w = rect.width // ZOOM
        rel_h = rect.height // ZOOM

        # Рисуем только те стены, которые попадают в границы квадрата карты
        wall_rect = pygame.Rect(rel_x, rel_y, rel_w, rel_h)
        if minimap_surf.get_rect().colliderect(wall_rect):
            pygame.draw.rect(minimap_surf, (100, 100, 100), wall_rect)

    # 2. Рисуем зелёные квестовые точки
    for rect in rect_mas1:
        rel_x = half_size + (rect.centerx - player.centerx) // ZOOM
        rel_y = half_size + (rect.centery - player.centery) // ZOOM
        pygame.draw.circle(minimap_surf, point_color, (int(rel_x), int(rel_y)), int(4 // ZOOM))

    # 3. Рисуем Босса (Красный круг)
    if len(boss) > 0:
        rel_bx = half_size + (boss_x - player.centerx) // ZOOM
        rel_by = half_size + (boss_y - player.centery) // ZOOM
        boss_rect = pygame.Rect(rel_bx - 4, rel_by - 4, 8, 8)
        if minimap_surf.get_rect().colliderect(boss_rect):
            pygame.draw.circle(minimap_surf, (255, 0, 0), (int(rel_bx), int(rel_by)), 5)

    # 4. Рисуем игрока строго по центру холста (Желтый круг)
    pygame.draw.circle(minimap_surf, (255, 235, 59), (half_size, half_size), 4)

    # 5. Рисуем линию взгляда (куда смотрит игрок)
    line_end_x = half_size + math.cos(ang) * 15
    line_end_y = half_size + math.sin(ang) * 15
    pygame.draw.line(minimap_surf, (255, 235, 59), (half_size, half_size), (line_end_x, line_end_y), 2)

    # Рисуем аккуратную рамку вокруг миникарты
    pygame.draw.rect(minimap_surf, (255, 255, 255), (0, 0, MAP_SIZE, MAP_SIZE), 2)

    # Выводим готовую миникарту на основной экран игры
    screen.blit(minimap_surf, (MAP_X, MAP_Y))


def chat_cons(current_move, sg, boss_visible, obn):
    chat_x = 200
    chat_y = 400

    otst_x = WIDTH - 220
    otst_y = 240

    chat_cons_surf = pygame.Surface((chat_x, chat_y), pygame.SRCALPHA)
    chat_cons_surf.fill((128, 128, 128, 100))


    text_line1 = chat_font.render("        BOSS      ", True, (255, 255, 255))

    text_line2 = chat_font.render(f"st {current_move}", True, (255, 255, 255))

    text_line3 = chat_font.render(f"stc {sg}", True, (255, 255, 255))


    if boss_visible:
        text_line4_1 = chat_font.render(f"bsv", True, (255, 255, 255))
        text_line4 = chat_font.render(f" {boss_visible}", True, (0, 220, 128))
    else:
        text_line4_1 = chat_font.render(f"bsv", True, (255, 255, 255))
        text_line4 = chat_font.render(f"{boss_visible}", True, (200, 20, 60))



    if obn:
        text_line5_1 = chat_font.render(f"upd", True, (255, 255, 255))
        text_line5 = chat_font.render(f"{bool(obn)}", True, (0, 220, 128))
    else:
        text_line5_1 = chat_font.render(f"upd", True, (255, 255, 255))
        text_line5 = chat_font.render(f"{bool(obn)}", True, (200, 20, 60))


    chat_cons_surf.blit(text_line1, (10, 15))
    chat_cons_surf.blit(text_line2, (10, 55))
    chat_cons_surf.blit(text_line3, (10, 95))



    chat_cons_surf.blit(text_line4_1, (10, 135))
    chat_cons_surf.blit(text_line4, (90, 135))



    chat_cons_surf.blit(text_line5_1, (10, 175))
    chat_cons_surf.blit(text_line5, (90, 175))


    screen.blit(chat_cons_surf, (otst_x, otst_y))

def win_player():
    try:
        font = pygame.font.Font("8bitfont.otf", 60)
    except:
        font = pygame.font.SysFont("Arial", 60)
    text_surface = font.render("ТЫ ВЫЙГРАЛ!", True, (144, 238, 144))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    waiting = True
    while waiting:
        screen.fill((18, 18, 20))  # Темный фон
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        try:
            k_pad = gamepad.update()
        except:
            k_pad = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if k_pad == 1: gamepad.update_pos(event)
        keys = pygame.key.get_pressed()
        if gamepad.buttons.get("A") or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            waiting = False

flag_for_event = 0
count_event = 0          # ← ВОТ ЗДЕСЬ ДОБАВИТЬ
current_move = ""         # ← ВОТ ЗДЕСЬ ДОБАВИТЬ
sg = "" 

while running:

    try:
        k = gamepad.update()
    except Exception:
        k = 0

    if (player.x // mapa) == coord_exit_x and (player.y // mapa) == coord_exit_y:
        print("WIN")
        win_player()
        reset_level()
        pygame.mixer.music.load('music/horror_music.mp3')
        pygame.mixer.music.play(loops=-1, start=0.0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if k == 1:
            gamepad.update_pos(event)

        if event.type == POLL_EVENT:
            print("recalc path")
            find_path()

            flag_for_event = 1

    timer += 1

    pygame.draw.rect(screen, werx_rect_color, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, niz_rect_color, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    keys = pygame.key.get_pressed()
    speed = 8
    old_pos = player.topleft
    is_moving = False

    if keys[pygame.K_w] or gamepad.buttons["k_UP"]:
        player.x += speed * math.cos(ang)
        player.y += speed * math.sin(ang)
        is_moving = True

        # Назад
    if keys[pygame.K_s] or gamepad.buttons["k_DOWN"]:
        player.x -= speed * math.cos(ang)
        player.y -= speed * math.sin(ang)
        is_moving = True

    if gamepad.buttons["k_R"] or keys[pygame.K_d]:
        player.x += speed * math.cos(ang+math.pi/2)
        player.y += speed * math.sin(ang+math.pi/2)

    if gamepad.buttons["k_L"] or keys[pygame.K_a]:
        player.x -= speed * math.cos(ang+math.pi/2)
        player.y -= speed * math.sin(ang+math.pi/2)



        # Поворот влево
    if keys[pygame.K_LEFT] or gamepad.buttons["LT"]:
        ang -= ang1

        # Поворот вправо
    if keys[pygame.K_RIGHT] or gamepad.buttons["RT"]:
        ang += ang1

    if is_moving: walk_timer += 0.35
    else: walk_timer = 0

    bobbing = int(math.sin(walk_timer) * 9)

    for rect in rect_mas:
        if player.colliderect(rect):
            player.topleft = old_pos

    start_pos = player.center

    if count > 1: step = math.radians(arch) / (count - 1)
    else: step = 0
    # print(player.center)

    if len(boss) < 0:
        running = False


    boss_dx = player.centerx - boss_x
    boss_dy = player.centery - boss_y
    rast = int(math.hypot(boss_dx, boss_dy))


    if len(boss) > 0:
        boss[0].center = (int(boss_x), int(boss_y))
        old_rast = rast
        if timer >= FPS:
            timer = 0
            if rast <= mapa:

                # Создаем быстрый экран смерти прямо в Pygame
                try:
                    font = pygame.font.Font("8bitfont.otf", 60)
                except:
                    font = pygame.font.SysFont("Arial", 60)
                text_surface = font.render("ПОМЕР", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                waiting = True
                while waiting:
                    screen.fill((18, 18, 20))  # Темный фон
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    try:
                        k_pad = gamepad.update()
                    except:
                        k_pad = 0
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit();
                            sys.exit()
                        if k_pad == 1: gamepad.update_pos(event)
                    keys = pygame.key.get_pressed()
                    if gamepad.buttons.get("A") or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
                        waiting = False
                running = False
                break

        # для босса________________________________________________________________



        if boss_visible:
            if bl_visit:
                pygame.mixer.music.load('music/pogonja.mp3')
                pygame.mixer.music.play(-1, start=12.0)
                bl_visit = False
                bl_not_visit = True
            if boss_invisible:
                boss_invisible=False

            if rast > 10 and boss_move_flag == 1:
                boss_x += (boss_dx / rast) * boss_speed
                boss_y += (boss_dy / rast) * boss_speed

                boss_target_x, boss_target_y = boss_x, boss_y
                boss_is_walking = False
        else:
            if bl_not_visit:
                pygame.mixer.music.load('music/horror_music.mp3')
                pygame.mixer.music.play(-1, start=0.0)
                bl_visit = True
                bl_not_visit = False
            if not boss_invisible:
                boss_invisible=True
                find_path()

            if not boss_is_walking:
                if boss_action_timer % 150 == 0:

                    if boss_step_index < len(boss_instruction):
                        current_move = boss_instruction[boss_step_index]
                        # print(f"Босс выполняет шаг {boss_step_index + 1}/{len(boss_instruction)}: {current_move}")

                        sg = str(boss_step_index + 1) + ' of ' + str(len(boss_instruction))

                        if current_move == 'U':
                            boss_target_x, boss_target_y = boss_UP(boss_x, boss_y)
                        elif current_move == 'D':
                            boss_target_x, boss_target_y = boss_DOWN(boss_x, boss_y)
                        elif current_move == 'L':
                            boss_target_x, boss_target_y = boss_Left(boss_x, boss_y)
                        elif current_move == 'R':
                            boss_target_x, boss_target_y = boss_Right(boss_x, boss_y)

                        boss_is_walking=True
                        boss_step_index += 1
                    else:

                        # print("ended instruction, recalc")
                        find_path()
            else:
                move_dx = boss_target_x - boss_x
                move_dy = boss_target_y - boss_y
                step_dist = math.hypot(move_dx, move_dy)

                if step_dist > boss_speed:
                    boss_x += (move_dx / step_dist) * boss_speed
                    boss_y += (move_dy / step_dist) * boss_speed
                else:
                    boss_x = boss_target_x
                    boss_y = boss_target_y
                    boss_is_walking = False



        # для босса_________________________________________________________________



        angle_to_boss = math.atan2(boss_y - player.centery, boss_x - player.centerx)
        rel_angle = angle_to_boss - ang
        rel_angle = (rel_angle + math.pi) % (2 * math.pi) - math.pi
        half_fov = math.radians(arch) / 2

        boss_screen_x = (WIDTH / 2) + (rel_angle / half_fov) * (WIDTH / 2)
        boss_dist = rast * math.cos(rel_angle)
        if boss_dist < 1: boss_dist = 1
        boss_size = min(int((mapa * DIST_TO_PROJ_PLANE) / boss_dist), HEIGHT)
        boss_screen_y = (HEIGHT - boss_size) // 2 + bobbing

        wave_rad = (timer / FPS) * mapa
        wave_width = (2 * wave_rad * DIST_TO_PROJ_PLANE) / boss_dist
        wave_height = wave_width / 4
        wave_screen_y = boss_screen_y + boss_size - (wave_height / 2)

    start_angle = ang - math.radians(arch) / 2
    z_buffer = [float(pror)] * count

    for i in range(count):
        current_ray_angle = start_angle + i * step

        end_pos = (start_pos[0] + pror * math.cos(current_ray_angle), start_pos[1] + pror * math.sin(current_ray_angle))
        closest_point = end_pos

        hit_wall = False
        hit_wall1 = False
        hit_trig = False
        hit_boss = False

        for wall in trig:
            if player.colliderect(wall):
                player.topleft = (old_pos[0] - 1, old_pos[1] - 1)
            points = wall.clipline(start_pos, end_pos)
            if points:
                p1 = points[0]
                if math.hypot(p1[0] - start_pos[0], p1[1] - start_pos[1]) < math.hypot(closest_point[0] - start_pos[0], closest_point[1] - start_pos[1]):
                    closest_point = p1
                    hit_trig = True

        # для игрока__________________________________________________

        for wall in range(len(t_mas)):
            if t_mas[wall][0] + mapa > player.x >= t_mas[wall][0] and t_mas[wall][1] + mapa > player.y >= t_mas[wall][1]:

                if old_pl_pos != t_mas[wall]:

                    player_tile = t_mas[wall] # переменная игрока

                    # print('тайл игрока:', player_tile)

                old_pl_pos = t_mas[wall]

        # для игрока__________________________________________________


        # для босса___________________________________________________


        for wall in range(len(t_mas)):

            if t_mas[wall][0] + mapa > boss_x >= t_mas[wall][0] and t_mas[wall][1] + mapa > boss_y >= t_mas[wall][1]:

                if old_bs_pos != t_mas[wall]:

                    boss_tile = t_mas[wall] # переменная босса

                    # print('тайл босса:', boss_tile)

                old_bs_pos = t_mas[wall]


        # для босса____________________________________________________

        for wall in rect_mas1:
            points = wall.clipline(start_pos, end_pos)
            if points:
                p1 = points[0]
                if math.hypot(p1[0] - start_pos[0], p1[1] - start_pos[1]) < math.hypot(closest_point[0] - start_pos[0], closest_point[1] - start_pos[1]):
                    closest_point = p1
                    if flag_zel:
                        hit_wall1 = True
                        cont_wal = rect_mas1.index(wall)

        for wall in rect_mas:
            points = wall.clipline(start_pos, end_pos)
            if points:
                p1 = points[0]
                if math.hypot(p1[0] - start_pos[0], p1[1] - start_pos[1]) < math.hypot(closest_point[0] - start_pos[0],
                                                                                       closest_point[1] - start_pos[1]):
                    closest_point = p1;
                    p2 = wall
                    hit_wall = True

        if hit_wall1:
            dist = math.hypot(closest_point[0] - start_pos[0], closest_point[1] - start_pos[1])
            if player.colliderect(rect_mas1[cont_wal]): rect_mas1.pop(cont_wal); count_s_points += 1

            dist *= math.cos(current_ray_angle - ang)
            if dist < 1: dist = 1

            wall_height = min(int((mapa * DIST_TO_PROJ_PLANE) / dist), HEIGHT)
            screen_x = i * SCALE
            screen_y = (HEIGHT//2) - (wall_height // 2) + bobbing

            pygame.draw.rect(screen, point_color, (screen_x, screen_y, int(SCALE) + 1, wall_height))
            if count_s_points == count_points: trig.pop(count_door); count_door += 1
            z_buffer[i] = dist

        elif hit_trig:
            dist = math.hypot(closest_point[0] - start_pos[0], closest_point[1] - start_pos[1])
            dist *= math.cos(current_ray_angle - ang)
            if dist < 1: dist = 1

            wall_height = min(int((mapa * DIST_TO_PROJ_PLANE) / dist), HEIGHT)
            screen_x = i * SCALE
            screen_y = (HEIGHT//2) - (wall_height//2) + bobbing

            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, int(SCALE) + 1, wall_height))
            z_buffer[i] = dist

        if hit_wall:
            dist = math.hypot(closest_point[0] - start_pos[0], closest_point[1] - start_pos[1])
            dist *= math.cos(current_ray_angle - ang)
            if dist < 1: dist = 1

            wall_height = min(int((mapa * DIST_TO_PROJ_PLANE) / max(1,dist)), HEIGHT)
            color = (0, 255, 0) if hit_wall1 else (255, 0, 0) if hit_trig else (100, 100, 100)


            color_factor = max(0.0, 1.0 - (dist / pror))


            base_r, base_g, base_b = 100, 110, 130


            grid_light = int(30 * color_factor) if rect_mas.index(p2) % 2 == 0 else 0


            r = min(255, max(0, int(base_r * color_factor) + grid_light))
            g = min(255, max(0, int(base_g * color_factor) + grid_light))
            b = min(255, max(0, int(base_b * color_factor) + grid_light))

            screen_x = i * SCALE
            screen_y = (HEIGHT//2) - (wall_height//2) + bobbing

            pygame.draw.rect(screen, (r, g, b), (screen_x, screen_y, int(SCALE) + 2, wall_height))
            z_buffer[i] = dist


    if len(boss) > 0:
        boss_ray_index = int(boss_screen_x / SCALE)

        if boss_dist < 10: boss_dist = 10
        boss_size = min(int((mapa * DIST_TO_PROJ_PLANE) / boss_dist), HEIGHT)
        boss_screen_y = (HEIGHT - boss_size) // 2 + bobbing

        left_x = int(boss_screen_x - boss_size // 2)
        right_x = int(boss_screen_x + boss_size // 2)

        start_ray = max(0, int(left_x / SCALE))
        end_ray = min(count - 1, int(right_x / SCALE))
        boss_move_flag = 0


        boss_visible = False

        for r in range(start_ray, end_ray + 1):
            if z_buffer[r] > boss_dist:
                boss_visible = True

                boss_move_flag = 1
                break



        if boss_visible and right_x > 0 and left_x < WIDTH:
            if wave_width > 0 and wave_height > 0:
                wave_rect = pygame.Rect(
                    int(boss_screen_x - wave_width // 2),
                    int(wave_screen_y),
                    int(wave_width),
                    int(wave_height)
                )
                pygame.draw.ellipse(screen, (255, 0, 0), wave_rect, 15)

            scaled_boss = pygame.transform.scale(boss_img, (boss_size, boss_size))
            screen.blit(scaled_boss, (left_x, boss_screen_y))

    chat_cons(current_move, sg, boss_visible, flag_for_event)
    draw_minimap()

    if count_event == 100:
        flag_for_event = 0
        count_event = 0

    count_event += 1

    pygame.display.flip()
    clock.tick(FPS)

pygame.display.quit()

