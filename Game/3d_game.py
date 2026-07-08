

'''

boss_tile координата босса в тайлах (x, y) с масштабом mapa = 60
player_tile координата игрока в тайлах (x, y) с масштабом mapa = 60

'''


import astar_lib
import pygame
import math
import sys
import os

os.environ['KIVY_NO_ARGS'] = '1'
from kivy.config import Config
Config.set('input', 'wm_pen', 'none')
Config.set('input', 'wm_touch', 'none')

Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'resizable', '0')


from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label

from drivers import GamepadDriver

gamepad = GamepadDriver()



class game_over_window(App):
    def __init__(self, gamepad_driver, **kwargs):
        super().__init__(**kwargs)
        self.gamepad = gamepad_driver
        self.button_pressed_lock = False

    def build(self):

        from kivy.core.window import Window
        from kivy.uix.anchorlayout import AnchorLayout
        from kivy.graphics import Color, Rectangle

        Window.size = (960, 960)


        Clock.schedule_interval(self.read_gamepad, 1 / 60.0)

        layout = AnchorLayout(anchor_x='center', anchor_y='center')

        with layout.canvas.before:
            Color(18 / 255, 18 / 255, 20 / 255, 1)  # Тот самый темный цвет меню
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))

        Window.bind(on_resize=lambda win, w, h: setattr(self.bg_rect, 'size', (w, h)))


        return Label(
            text="ПОМЕР",
            font_name="8bitfont.otf",
            font_size=60,
            color=(1, 0, 0,1),
            mipmap=False
        )

        # layout.add_widget(Label)
        # return layout



    def read_gamepad(self, dt):
        if self.gamepad.update() == 1:
            for event in pygame.event.get():
                self.gamepad.update_pos(event)

        if self.gamepad.buttons.get("A"):
            if not self.button_pressed_lock:
                self.stop()
                sys.exit()
        else:
            self.button_pressed_lock = False




#_______________________Настройки экрана и графики________________________
WIDTH = 960
HEIGHT = 960
FPS =  30
#_______________________Настройки экрана и графики________________________

# ____________________________Настройки лучей_____________________________
count = 80 # Количество лучей (чем больше, тем выше качество 3D)
arch = 60  # Поле зрения в градусах
width = 1
# ____________________________Настройки лучей_____________________________

flag_zel = True

point_color = (0, 255, 21)

werx_rect_color = (155, 155, 155)
niz_rect_color = (25, 25, 25)

# (50, 55, 70)
# (35, 35, 35)
boss_speed = 3.5
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

map = [
    "11111111111111111111111111111111111111111111111111111111111111111111111111",
    "1..........................1......................B......................1",
    "1..........................1.............................................1",
    "1..........................1.............................................1",
    "1..........................1.............................................1",
    "1..........................1.............................................1",
    "1.............P............1.............................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
    "1........................................................................1",
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

print(t_mas)
# _________________________ ____________________


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
    boss_img = pygame.image.load('boss1.png').convert_alpha()
except:
    boss_img = pygame.Surface((64, 64))
    boss_img.fill((255, 0, 100))

boss_move_flag = 1
walk_timer = 0
count_s_points = 0
old_rast = 0


#____________________________________________________________________________


boss_visible = False


#____________________________________________________________________________



# для игрока___________________________________________________

old_pl_pos = player.x, player.y

# для игрока___________________________________________________
# для босса____________________________________________________

old_bs_pos = boss_x, boss_y

# для босса____________________________________________________


POLL_EVENT = pygame.USEREVENT + 1

# Запускаем таймер: 5000 миллисекунд = 5 секунд
pygame.time.set_timer(POLL_EVENT, 5000)




py, px = player.x, player.y
by, bx = boss_x, boss_y


print(astar_lib.astar(map, py, px, by, bx))

# _______________________________________________________________________


boss_instruction = "URUULD"
boss_step_index = 0         # Индекс текущего шага в инструкции
boss_action_timer = 0       # Отдельный таймер для шагов босса


# _______________________________________________________________________

while running:

    try:
        k = gamepad.update()
    except Exception:
        k = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if k == 1:
            gamepad.update_pos(event)

    timer += 1

    pygame.draw.rect(screen, werx_rect_color, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, niz_rect_color, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    keys = pygame.key.get_pressed()
    speed = 10
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
                running = False
                print('андрей лоооох')
                os.environ['SDL_VIDEODRIVER'] = 'dummy'
                pygame.display.init()
                pygame.display.set_mode((1, 1))
                game_over_window(gamepad_driver=gamepad).run()
                break

        # для босса________________________________________________________________


        if boss_visible:
            if boss_visible:

                if rast > 10 and boss_move_flag == 1:
                    boss_x += (boss_dx / rast) * boss_speed
                    boss_y += (boss_dy / rast) * boss_speed
            else:

                if boss_action_timer % 150 == 0:

                    if boss_step_index < len(boss_instruction):
                        current_move = boss_instruction[boss_step_index]
                        print(f"Босс выполняет шаг {boss_step_index + 1}/{len(boss_instruction)}: {current_move}")


                        if current_move == 'U':
                            boss_x, boss_y = boss_UP(boss_x, boss_y)
                        elif current_move == 'D':
                            boss_x, boss_y = boss_DOWN(boss_x, boss_y)
                        elif current_move == 'L':
                            boss_x, boss_y = boss_Left(boss_x, boss_y)
                        elif current_move == 'R':
                            boss_x, boss_y = boss_Right(boss_x, boss_y)

                        boss_step_index += 1
                    else:

                        print("Инструкция закончилась, босс ждет...")

                        # Вариант Б: Зациклить ходить по кругу (раскомментируйте, если нужно):
                        # boss_step_index = 0
        else:
            if timer % 150 == 0:
                print("Прошло 5 секунд!")
                boss_x, boss_y = boss_DOWN(boss_x, boss_y)


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

                    print('тайл игрока:', player_tile)

                old_pl_pos = t_mas[wall]

        # для игрока__________________________________________________


        # для босса___________________________________________________


        for wall in range(len(t_mas)):

            if t_mas[wall][0] + mapa > boss_x >= t_mas[wall][0] and t_mas[wall][1] + mapa > boss_y >= t_mas[wall][1]:

                if old_bs_pos != t_mas[wall]:

                    boss_tile = t_mas[wall] # переменная босса

                    print('тайл босса:', boss_tile)

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

    pygame.display.flip()
    clock.tick(FPS)

pygame.display.quit()

