import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0    # To avoid keep moving when no key is pressed

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0    # To avoid keep moving when no key is pressed

    def move(self, speed):
        if self.direction.magnitude() != 0:     # Can't normalize a null vector
            self.direction = self.direction.normalize()     # Avoid the speed boost with diagonal movement
        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)
