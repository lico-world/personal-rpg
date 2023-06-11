import pygame

from support import import_folder
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.animations = None
        self.image = pygame.image.load('../graphics/test/02_player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-pygame.math.Vector2(PLAYER_COLLISION_MARGIN))

        self.import_player_assets()
        self.status = 'down'

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.doing_action = False
        self.action_cooldown = 400
        self.action_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        player_path = '../graphics/player/'

        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement keys
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0  # To avoid keep moving when no key is pressed

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0  # To avoid keep moving when no key is pressed

        # Actions keys
        if keys[pygame.K_SPACE] and not self.doing_action:
            self.doing_action = True
            self.action_time = pygame.time.get_ticks()
            print('Attack')

    def get_status(self):
        # Idle status
        if self.direction.x == self.direction.y == 0:
            if 'idle' not in self.status:
                self.status += '_idle'

    def move(self, speed):
        if self.direction.magnitude() != 0:  # Can't normalize a null vector
            self.direction = self.direction.normalize()  # Avoid the speed boost with diagonal movement

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.doing_action:
            if current_time - self.action_time >= self.action_cooldown:
                self.doing_action = False

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)
