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

        # Floor management
        self.floor_surface = pygame.image.load('../graphics/test/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        if self.camera_pos == pygame.math.Vector2():
            self.camera_pos += player.rect.center - pygame.math.Vector2(self.half_width, self.half_height)

        # Horizontal camera movement
        if (player.rect.right - self.camera_pos.x >= WIDTH - SCROLL_WIDTH and player.direction[0] > 0) or \
                (player.rect.left - self.camera_pos.x <= SCROLL_WIDTH and player.direction[0] < 0):

            # If the player reach the end of the static zone : camera move
            self.camera_pos.x += player.direction[0] * player.speed

        # Vertical camera movement
        if (player.rect.top - self.camera_pos.y >= HEIGHT - SCROLL_HEIGHT and player.direction[1] > 0) or \
                (player.rect.bottom - self.camera_pos.y <= SCROLL_HEIGHT and player.direction[1] < 0):

            # If the player reach the end of the static zone : camera move
            self.camera_pos.y += player.direction[1] * player.speed

        # Drawing the floor
        self.display_surface.blit(self.floor_surface, self.floor_rect.topleft - self.camera_pos)

        # Sort sprites to draw according to the y value
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.camera_pos
            self.display_surface.blit(sprite.image, offset)
