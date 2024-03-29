from settings import *
from support import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        # Import all the layers for the map (imported from Tiled)
        layouts = {
            'boundary'  : import_csv_layout('../map/test_map_collisions.csv'),
            'object'    : import_csv_layout('../map/test_map_elements.csv'),
            'big_object': import_csv_layout('../map/test_map_big_elements.csv')
        }

        # Import all the graphics folders for world elements
        graphics = {
            'objects'    : import_folder('../graphics/test/objects'),
            'big_objects': import_folder('../graphics/test/big_objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # Get coordinates where the bloc should be
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # Fill the sprite lists with all the world elements
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'object':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object',
                                 graphics['objects'][int(col)])
                        elif style == 'big_object':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'big_object',
                                 graphics['big_objects'][int(col)])

        self.player = Player((1500, 900), [self.visible_sprites], self.obstacle_sprites)  # Create the player instance

    def save(self):
        pass  # In the future, it should save player info and anything needed to be saved in the level

    def run(self):
        self.visible_sprites.update()                   # Update what are the visible sprites
        self.visible_sprites.custom_draw(self.player)   # Draw each one of them


def item_is_displayable(player, item):  # Allow to only display visible objects
    player_position = player.rect.center
    item_position = item.rect.center

    return abs(player_position[0] - item_position[0]) < (WIDTH // 2) + SCROLL_WIDTH and \
        abs(player_position[1] - item_position[1]) < (HEIGHT // 2) + SCROLL_HEIGHT


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera_pos = pygame.math.Vector2()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # Floor management
        self.floor_surface = pygame.image.load('../map/test_map.png').convert()
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
            if item_is_displayable(player, sprite):
                offset = sprite.rect.topleft - self.camera_pos
                self.display_surface.blit(sprite.image, offset)
