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
            'up'    : 0,
            'down'  : 0,
            'right' : 0,
            'left'  : 0,
            'attack': 0
        }

        self.current_keys = []  # This list store all the currently pressed (to update with 'update_key_pressed()')

        self.save_file = '../data/keymaps.txt'

    def init_keymaps(self):
        with open(self.save_file, 'r') as saved_keymap:
            imported_keymap = saved_keymap.readlines()

            for key in imported_keymap:
                sep = key.find(':')
                self.keymap[key[0:sep]] = int(key[sep + 1:len(key)])

    def update_pressed_keys(self, pressed_keys):  # This function allow to not call the 'pygame.key.get_pressed()'
                                                  # at each 'detect_key()' call
        self.current_keys = pressed_keys

    def save_keymaps(self):
        with open(self.save_file, 'w') as saving_file:
            for action, key in self.keymap.items():
                saving_file.write(str(action) + ':' + str(key) + '\n')

    def set_key(self, action):
        key_set = False
        while not key_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # To be sure a call in a loop will not soft lock the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keymap[action] = event.key
                    key_set = True  # To leave while loop
                    break           # To leave for loop

    def detect_key(self, key):
        if self.keymap[key] > len(self.current_keys):
            return 0
        else:
            return self.current_keys[self.keymap[key]]  # Return if the asked key is pressed in any keymap
