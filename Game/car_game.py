import pygame
import random
pygame.init()
stage='menu'
pygame.mixer.music.load('лютый звук машины.mp3')
pygame.mixer.music.load('столкновение.mp3')
pygame.mixer.music.load('собрано.mp3')
sound1=pygame.mixer.Sound('лютый звук машины.mp3')
sound2=pygame.mixer.Sound('столкновение.mp3')
sound3=pygame.mixer.Sound('собрано.mp3')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (182, 4, 4)
CAR_COLOR = RED
TEXT_COLOR = (250, 105, 10)


from drivers import GamepadDriver

gamepad = GamepadDriver()


gui_font=pygame.font.Font(None,30)
pressed=False
def button_c(width, height, pos):
    mouse_pos = pygame.mouse.get_pos()
    top_rect = pygame.Rect(pos, (width, height))
    if top_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            return True
class Button:
    def __init__(self, text, width, height, pos, elevation, type):
        self.top_rect=pygame.Rect(pos,(width,height))
        self.pressed=False
        self.elevation=elevation
        self.dynamic_elevation=elevation
        self.original_y_pos=pos[1]
        self.top_color='#475F77'
        self.text_surf=gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.type=type

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos=pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D73B4B'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:


                    start_p=True
                    self.pressed = False

class Car:
    def __init__(self, x=0, y=0, dx=4, dy=0, width=30, height=50, color=RED):
        self.image = ""
        self.x = x
        self.y = y
        self. dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.color = color

    def load_image(self, img):
        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey(BLACK)

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def draw_rect(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    def check_out_of_screen(self):
        if self.x+self.width > 400 or self.x < 0:
            self.x -= self.dx
carCol=False
size = (400, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("car game")
done = False
clock = pygame.time.Clock()
player = Car(175, 475, 0, 0, 70, 131, RED)
player.load_image("car.png")
collision = True
score = 0
font_40 = pygame.font.SysFont("Arial", 40, True, False)
font_30 = pygame.font.SysFont("Arial", 30, True, False)
text_title = font_40.render("Машинка", True, RED)

button_start = Button('Начать', 200, 80, (100, 200), 6, 'start')
button_end = Button('Выйти', 200, 80, (100, 700), 6, 'start')
button_set = Button('Настройки', 200, 80, (100, 500), 6, 'start')




def draw_main_menu():
    button_start.top_color = '#475F77'
    button_set.top_color = '#475F77'
    button_end.top_color = '#475F77'
    menu_buttons[menu_selected_button].top_color = '#D73B4B'

    button_start.draw()
    score_text = font_40.render("Cчёт: " + str(score), True, RED)
    screen.blit(score_text, [size[0] / 2 - 80, size[1] / 2 - 30])
    button_set.draw()
    button_end.draw()
    pygame.display.flip()


button_back_from_l = Button('В меню', 200, 80, (100, 100), 6, 'start')
def draw_loose():
    button_back_from_l.top_color = '#D73B4B'
    button_back_from_l.draw()
    screen.blit(text_title, [size[0] / 2 - 100, size[1] / 2 - 100])
    score_text = font_40.render("Вы Проиграли... ", True, RED)
    screen.blit(score_text, [size[0] / 2 - 150, size[1] / 2 - 30])
    pygame.display.flip()
button_plus = Button('Включить звук', 200, 80, (100, 300), 6, 'start')
button_minus = Button('Выключить звук', 200, 80, (100, 450), 6, 'start')
button_back_to_menu=Button('Назад', 200, 80, (100, 600), 6, 'start')
def draw_set_menu():
    button_plus.top_color='#475F77'
    button_minus.top_color = '#475F77'
    button_back_to_menu.top_color = '#475F77'
    set_buttons[set_selected_button].top_color = '#D73B4B'
    button_plus.draw()
    button_minus.draw()
    button_back_to_menu.draw()
    pygame.display.flip()
cars = []
car_count = 2
for i in range(car_count):
    x = random.randrange(0, 400)
    car = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 60, 110, CAR_COLOR)
    cars.append(car)
bonuses = []
bonus_count = 1
for i in range(car_count):
    x = random.randrange(0, 400)
    bonus = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 40, 40, GREEN)
    bonuses.append(bonus)
stripes = []
stripe_count = 20
stripe_x = 185
stripe_y = 0
stripe_width = 15
stripe_height = 60
space = 40
for i in range(stripe_count):
    stripes.append([190, stripe_y])
    stripe_y += stripe_height + space


menu_buttons=[button_start,button_set,button_end]
menu_selected_button=0


set_buttons=[button_plus,button_minus,button_back_to_menu]
set_selected_button=0


pressed_button=[False,False,False]




gamepad = GamepadDriver()

while not done:

    gamepad.update()


    for event in pygame.event.get():
        gamepad.update_pos(event)

        if stage=='set':
            draw_set_menu()
        if stage == 'set' and button_c(200, 80, (100, 300)):
            sound1.play(-1)
        if stage == 'set' and button_c(200, 80, (100, 450)):
            sound1.stop()
        if stage == 'set' and button_c(200, 80, (100, 600)):
            stage='menu'
        if event.type == pygame.QUIT or button_c(200, 80, (100, 700)):
            done = True
        if button_c(200, 80, (100, 500)):
            stage='set'
        if stage=='loose' and button_c(200, 80, (100, 100)):
            draw_main_menu()
            stage = 'menu'
            score = 0
        if collision and button_c(200, 80, (100, 200)):
            if stage=='menu':
                collision = False
                for i in range(car_count):
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].x = random.randrange(0, 350)
                for i in range(bonus_count):
                    bonuses[i].y = random.randrange(-150, -50)
                    bonuses[i].x = random.randrange(0, 350)
                player.x = 175
                player.dx = 0
                score = 0
                pygame.mouse.set_visible(False)
        if not collision:
            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 4
                elif event.key == pygame.K_LEFT:
                    player.dx = -4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.dx = 0
                elif event.key == pygame.K_RIGHT:
                    player.dx = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                collision = True
                pygame.mouse.set_visible(True)'''
    if not collision:
        if gamepad.buttons.get('k_R'):
            player.dx=4
        elif gamepad.buttons.get('k_L'):
            player.dx=-4
        else:
            player.dx=0
        if gamepad.buttons.get('START'):
            collision = True
            pygame.mouse.set_visible(True)
    if collision:
        if stage == 'menu':
            if (gamepad.buttons.get('k_DOWN')):
                if not pressed_button[0]:
                    pressed_button[0] = True
                    menu_selected_button = (menu_selected_button + 1) % 3
            else:
                if pressed_button[0]:
                    pressed_button[0] = False

            if (gamepad.buttons.get('k_UP')):
                if not pressed_button[1]:
                    pressed_button[1] = True
                    menu_selected_button = (menu_selected_button - 1 + 3) % 3
            else:
                if pressed_button[1]:
                    pressed_button[1] = False
            if gamepad.buttons.get('A'):
                if not pressed_button[2]:
                    pressed_button[2] = True
                    if menu_selected_button==0:
                        collision = False
                        for i in range(car_count):
                            cars[i].y = random.randrange(-150, -50)
                            cars[i].x = random.randrange(0, 350)
                        for i in range(bonus_count):
                            bonuses[i].y = random.randrange(-150, -50)
                            bonuses[i].x = random.randrange(0, 350)
                        player.x = 175
                        player.dx = 0
                        pygame.mouse.set_visible(False)
                    elif menu_selected_button==1:
                        stage='set'
                    else:
                        done=True
            else:
                pressed_button[2] = False



        if stage == 'set':
            if (gamepad.buttons.get('k_DOWN')):
                if not pressed_button[0]:
                    pressed_button[0] = True
                    set_selected_button = (set_selected_button + 1) % 3
            else:
                if pressed_button[0]:
                    pressed_button[0] = False

            if (gamepad.buttons.get('k_UP')):
                if not pressed_button[1]:
                    pressed_button[1] = True
                    set_selected_button = (set_selected_button - 1 + 3) % 3
            else:
                if pressed_button[1]:
                    pressed_button[1] = False
            if gamepad.buttons.get('A'):
                if not pressed_button[2]:
                    pressed_button[2] = True
                    if set_selected_button==0:
                        sound1.play(-1)
                    elif set_selected_button==1:
                        sound1.stop()
                    else:
                        stage='menu'
            else:
                pressed_button[2] = False
        if stage == 'loose':
            if gamepad.buttons.get('A'):
                if not pressed_button[2]:
                    pressed_button[2] = True
                    draw_main_menu()
                    stage = 'menu'
                    score = 0
            else:
                pressed_button[2] = False


    screen.fill(GRAY)
    if not collision:
        for i in range(stripe_count):
            pygame.draw.rect(screen, WHITE, [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
        for i in range(stripe_count):
            stripes[i][1] += 3
            if stripes[i][1] > size[1]:
                stripes[i][1] = -40 - stripe_height
        player.draw_image()
        player.move_x()
        player.check_out_of_screen()
        for i in range(car_count):
            cars[i].draw_rect()
            cars[i].y += cars[i].dy
            if cars[i].y > size[1]:
                cars[i].y = random.randrange(-150, -50)
                cars[i].x = random.randrange(0, 340)
                cars[i].dy = random.randint(4, 9)
        for i in range(bonus_count):
            bonuses[i].draw_rect()
            bonuses[i].y += cars[i].dy
            if bonuses[i].y > size[1]:
                bonuses[i].y = random.randrange(-150, -50)
                bonuses[i].x = random.randrange(0, 340)
                bonuses[i].dy = random.randint(4, 9)
        for i in range(car_count):
            if (player.x + player.width > cars[i].x) and (player.x < cars[i].x + cars[i].width) and (player.y < cars[i].y + cars[i].height) and (player.y + player.height > cars[i].y) :
                sound2.play()
                score-=5
                cars[i].y+=500
        for i in range(bonus_count):
            if (player.x + player.width > bonuses[i].x) and (player.x < bonuses[i].x + bonuses[i].width) and (player.y < bonuses[i].y + bonuses[i].height) and (player.y + player.height > bonuses[i].y) :
                score+=1
                sound3.play()
                bonuses[i].y+=500
        txt_score = font_30.render("Счёт: "+str(score), True, GREEN)
        screen.blit(txt_score, [15, 15])
        pygame.display.flip()

        if score<0:
            collision = True
            pygame.mouse.set_visible(True)

    else:
        if score<0:
            draw_loose()
            stage='loose'
        elif stage !='set':
            draw_main_menu()
            stage='menu'
    clock.tick(60)
pygame.quit()