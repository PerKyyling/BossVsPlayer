import pygame
from drivers import GamepadDriver
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
import subprocess
import sys

Window.clearcolor = (18 / 255, 18 / 255, 20 / 255, 1)

class RoundedButton(Button):
    def __init__(self, bg_color=(58 / 255, 195 / 255, 175 / 255, 1), radius=[20], **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.95, 0.95)
        self.size = (160, 65)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.bold = True


        with self.canvas.before:
            self.canvas_color = Color(*bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=radius)


        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def change_color(self, color):
        self.canvas_color.rgba = color


    def _update_canvas(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class window(App):
    def __init__(self):
        super().__init__()
        self.selected_button=0

    def build(self):
        self.gamepad = GamepadDriver()
        self.button_pressed_lock = False

        main_main_layout = BoxLayout(orientation='vertical')

        main_zone1 = BoxLayout(size_hint_y=0.2)
        main_zone2 = BoxLayout(size_hint_y=0.6)
        main_zone3 = BoxLayout(size_hint_y=0.2)

        main_main_layout.add_widget(main_zone1)
        main_main_layout.add_widget(main_zone2)
        main_main_layout.add_widget(main_zone3)

        main_layout = BoxLayout(orientation='horizontal')

        self.bt1 = RoundedButton(text="3Д-игра", bg_color=(58 / 255, 195 / 255, 175 / 255, 1), radius=[10])
        #self.bt1 = RoundedButton(text="Button 1", bg_color=(58 / 255, 60 / 255, 65 / 255, 1), radius=[10])
        self.bt2 = RoundedButton(text="Гонка", bg_color=(60 / 255, 60 / 255, 65 / 255, 1), radius=[10])
        self.bt3 = RoundedButton(text="Самогонка", bg_color=(60 / 255, 60 / 255, 65 / 255, 1), radius=[10])

        self.buttons_list=[self.bt1, self.bt2, self.bt3]

        self.buttons_state_list=[False for _ in range(3)]

        self.games_list=[self.play_3d_game,self.play_car_game,self.placeholder]

        for i in range(3):
            self.buttons_list[i].bind(on_release=self.games_list[i])




        #self.buttons_list[self.selected_button].bind(on_release=self.games_list[self.selected_button])

        zone1 = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.2)
        zone2 = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.6)
        zone3 = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.2)

        zone1.add_widget(self.bt1)
        zone2.add_widget(self.bt2)
        zone3.add_widget(self.bt3)

        main_layout.add_widget(zone1)
        main_layout.add_widget(zone2)
        main_layout.add_widget(zone3)

        main_zone2.add_widget(main_layout)

        Clock.schedule_interval(self.read_gamepad, 1 / 60.0)

        return main_main_layout

    def read_gamepad(self, dt):
        if self.gamepad.update() == 1:
            for event in pygame.event.get():
                self.gamepad.update_pos(event)


        if self.gamepad.buttons.get("k_R"):
            if not self.k_R_pressed_lock:
                self.buttons_list[self.selected_button].change_color((60 / 255, 60 / 255, 65 / 255, 1))
                self.selected_button = (self.selected_button + 1) % 3
                self.buttons_list[self.selected_button].change_color((58 / 255, 195 / 255, 175 / 255, 1))
                self.k_R_pressed_lock = True

        else:
            self.k_R_pressed_lock = False

        if self.gamepad.buttons.get("k_L"):
            if not self.k_L_pressed_lock:
                self.buttons_list[self.selected_button].change_color((60 / 255, 60 / 255, 65 / 255, 1))
                self.selected_button = (self.selected_button - 1 + 3) % 3
                self.buttons_list[self.selected_button].change_color((58 / 255, 195 / 255, 175 / 255, 1))
                self.k_L_pressed_lock = True

        else:
            self.k_L_pressed_lock = False




        if self.gamepad.buttons.get("A"):
            self.buttons_list[self.selected_button].state = "down"
            if not self.button_pressed_lock:
                self.button_pressed_lock = True
                self.buttons_list[self.selected_button].dispatch('on_release')
        else:
            self.buttons_list[self.selected_button].state = "normal"
            self.button_pressed_lock = False

    def play_3d_game(self, instance):
        print("игра запущена")

        Clock.unschedule(self.read_gamepad)
        subprocess.run([sys.executable, "3d_game.py"])


        print("игра закрыта")

        Clock.schedule_interval(self.read_gamepad, 1 / 60.0)

    def play_car_game(self, instance):
        print("игра запущена")

        Clock.unschedule(self.read_gamepad)
        subprocess.run([sys.executable, "car_game.py"])


        print("игра закрыта")

        Clock.schedule_interval(self.read_gamepad, 1 / 60.0)

    def placeholder(self, instance):
        print("АРА,АРА")

        #Clock.unschedule(self.read_gamepad)
        #subprocess.run([sys.executable, "car_game.py"])


        print("ТЫ КРУТОЙ")

        Clock.schedule_interval(self.read_gamepad, 1 / 60.0)

if __name__ == "__main__":
    window().run()