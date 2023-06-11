import pygame

keymap = {
    'up': 0,
    'down': 0,
    'right': 0,
    'left': 0,
    'action': 0
}


def init_keymaps():
    with open('../data/keymaps.txt', 'r') as save:
        imported_files = save.readlines()

        for line in imported_files:
            gap = line.find(':')
            keymap[line[0:gap]] = int(line[gap + 1:len(line)])


def save_keymaps():
    with open('../data/keymaps.txt', 'w') as save:
        for action, key in keymap.items():
            save.write(str(action) + ':' + str(key) + '\n')


def detect_key(key):
    keys = pygame.key.get_pressed()  # Get a list of pressed keys

    return keys[keymap[key]] or keys[keymap[key]]  # Return if the asked key is pressed in any keymap
