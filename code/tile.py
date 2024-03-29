import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface

        if sprite_type == 'big_object':  # Big object are twice tall in visual aspect but not for collisions
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
            self.hitbox = self.rect.inflate(0, -(TILESIZE + COLLISION_MARGIN))
            self.hitbox.topleft = self.rect.midleft
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -COLLISION_MARGIN)
