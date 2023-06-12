import sys
import pygame


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class KeyConfig(metaclass=Singleton):
    def __init__(self):
        self.keymap = {
            'up': 0,
            'down': 0,
            'right': 0,
            'left': 0,
            'attack': 0
        }

        self.current_keys = []

    def init_keymaps(self):
        with open('../data/keymaps.txt', 'r') as save:
            imported_files = save.readlines()

            for line in imported_files:
                gap = line.find(':')
                self.keymap[line[0:gap]] = int(line[gap + 1:len(line)])

    def update_pressed_keys(self, pressed_keys):
        self.current_keys = pressed_keys

    def save_keymaps(self):
        with open('../data/keymaps.txt', 'w') as save:
            for action, key in self.keymap.items():
                save.write(str(action) + ':' + str(key) + '\n')

    def set_key(self, action):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keymap[action] = event.key
                    break

    def detect_key(self, key):
        if self.keymap[key] > len(self.current_keys):
            return 0
        else:
            return self.current_keys[self.keymap[key]]  # Return if the asked key is pressed in any keymap
