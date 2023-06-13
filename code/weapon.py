import pygame

weapons_properties = ['name', 'cooldown', 'power', 'path']
all_weapons = {}


def import_weapons():
    with open('../data/weapons.txt', 'r') as import_file:
        imported_weapons = import_file.readlines()

        for weapon_line in imported_weapons:
            weapon = {
                'name'    : '',
                'cooldown': '',
                'power'   : '',
                'path'    : ''
            }

            sep = weapon_line.find(':')
            properties_done = 0
            while not sep == -1 and properties_done < len(weapons_properties):
                if properties_done > 0:
                    sep = weapon_line.find(':')
                weapon[weapons_properties[properties_done]] = weapon_line[0:sep]
                weapon_line = weapon_line[sep+1:len(weapon_line)]
                properties_done += 1

            all_weapons[weapon['name']] = weapon


class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
