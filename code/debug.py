import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DevTool(metaclass=Singleton):
    def __init__(self):
        self.display_info = False

        self.infos = {
            'FPS': '',
            'animation_state': '',
            'player_speed': '',
            'player_dir': ''
        }

    def display(self):
        display_surface = pygame.display.get_surface()

        index = 0
        for key, info in self.infos.items():
            debug_surf = font.render(str(key) + ' : ' + str(info), True, 'White')
            debug_rect = debug_surf.get_rect(topleft=(10, 20 * index + 10))
            background_surf = font.render(str(key) + ' : ' + str(info), True, 'Black')
            background_surf.fill((0, 0, 0))
            debug_surf.set_alpha(175)
            background_surf.set_alpha(175)
            display_surface.blit(background_surf, debug_rect)
            display_surface.blit(debug_surf, debug_rect)
            index += 1

    def switch_on_off(self):
        self.display_info = not self.display_info

    def update_info(self, key, value):
        self.infos[str(key)] = str(value)
