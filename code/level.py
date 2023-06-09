import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera_pos = pygame.math.Vector2()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):

        # Later: The camera should only move when the player is about to exit a camera sub-rectangle (static when the
        # player is centered)

        self.camera_pos.x = player.rect.centerx - self.half_width
        self.camera_pos.y = player.rect.centery - self.half_height

        # Sort sprites to draw according to the y value
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.camera_pos
            self.display_surface.blit(sprite.image, offset)
