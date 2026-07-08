import pygame


class GamepadDriver:

    def __init__(self):
        # Инициализируем только подсистему джойстиков
        pygame.joystick.init()
        self.joystick = None
        self.w_k = 0

        # Словарь состояний кнопок
        self.buttons = {
            "X": False,
            "A": False,
            "B": False,
            "Y": False,
            "START": False,
            "SELECT": False,
            "LT": False,
            "RT": False,
            "1111": False,
            "k_L": False,
            "k_R": False,
            "k_UP": False,
            "k_DOWN": False,
        }

    def update(self):
        """Проверяет подключение джойстика."""
        pygame.event.pump()
        is_now_connected = pygame.joystick.get_count() > 0

        if is_now_connected != self.w_k:
            self.w_k = 1 if is_now_connected else 0

            if is_now_connected:
                try:
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                    print("connected")
                    return 1
                except Exception:
                    self.w_k = 0
                    return 0
            else:
                self.joystick = None
                print("disconnected")
                # Сброс кнопок при отключении
                for key in self.buttons:
                    self.buttons[key] = False
                return 0
        else:
            return 1 if is_now_connected else 0

    def update_pos(self, event):
        """Обновляет состояние кнопок."""
        # 1. НАЖАТИЕ КНОПОК
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                self.buttons["X"] = True
            elif event.button == 1:
                self.buttons["A"] = True
            elif event.button == 2:
                self.buttons["B"] = True
            elif event.button == 3:
                self.buttons["Y"] = True
            elif event.button == 9:
                self.buttons["START"] = True
            elif event.button == 8:
                self.buttons["SELECT"] = True
            elif event.button == 4:
                self.buttons["LT"] = True
            elif event.button == 5:
                self.buttons["RT"] = True
            elif event.button == 10:
                self.buttons["1111"] = True

        # 2. ОТПУСКАНИЕ КНОПОК (чтобы персонаж останавливался)
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.buttons["X"] = False
            elif event.button == 1:
                self.buttons["A"] = False
            elif event.button == 2:
                self.buttons["B"] = False
            elif event.button == 3:
                self.buttons["Y"] = False
            elif event.button == 9:
                self.buttons["START"] = False
            elif event.button == 8:
                self.buttons["SELECT"] = False
            elif event.button == 4:
                self.buttons["LT"] = False
            elif event.button == 5:
                self.buttons["RT"] = False
            elif event.button == 10:
                self.buttons["1111"] = False

        # 3. КРЕСТОВИНА (ОСИ)
        elif event.type == pygame.JOYAXISMOTION:
            val = round(event.value)

            if event.axis == 0:  # Горизонтальная ось
                if val == -1:
                    self.buttons["k_L"] = True
                    self.buttons["k_R"] = False
                elif val == 1:
                    self.buttons["k_R"] = True
                    self.buttons["k_L"] = False
                elif val == 0:
                    self.buttons["k_L"] = False
                    self.buttons["k_R"] = False

            elif event.axis == 1:  # Вертикальная ось
                if val == -1:
                    self.buttons["k_UP"] = True
                    self.buttons["k_DOWN"] = False
                elif val == 1:
                    self.buttons["k_DOWN"] = True
                    self.buttons["k_UP"] = False
                elif val == 0:
                    self.buttons["k_UP"] = False
                    self.buttons["k_DOWN"] = False