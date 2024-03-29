from support import import_folder
from settings import *
from keys_config import *
from debug import DevTool
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # Player visual aspect and hitbox
        self.animations = None
        self.image = pygame.image.load('../graphics/test/02_player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # The hitbox is smaller than the sprite for an illusion of depth
        self.hitbox = self.rect.inflate(-pygame.math.Vector2(PLAYER_COLLISION_MARGIN))

        self.import_player_assets()     # Import player animation sprites
        self.status = 'down'
        self.frame_index = 0            # Used to follow the animation evolution

        # Movement components
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites  # Contains all the sprites to collide with

    def import_player_assets(self):
        player_path = '../graphics/test/player/'

        self.animations = {
            'up'       : [], 'down': [], 'left': [], 'right': [],
            'up_idle'  : [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        key_config = KeyConfig()
        key_config.update_pressed_keys(pygame.key.get_pressed())

        # Movement keys
        if key_config.detect_key('up'):
            self.direction.y = -1
            self.status = 'up'
        elif key_config.detect_key('down'):
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0  # To avoid keep moving when no key is pressed

        if key_config.detect_key('right'):
            self.direction.x = 1
            self.status = 'right'
        elif key_config.detect_key('left'):
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0  # To avoid keep moving when no key is pressed

        # Actions keys
        if key_config.detect_key('attack') and not self.attacking:  # Only do an action if it is not already the case
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()  # First time point to manage action cooldown
            print('Attack')

    def get_status(self):
        # Idle status
        if self.direction.x == self.direction.y == 0:  # Detect if the player is idle
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

        dev_tool = DevTool()
        dev_tool.update_info('animation_state', self.status)

    def move(self, speed):
        if self.direction.magnitude() != 0:  # Can't normalize a null vector
            self.direction = self.direction.normalize()  # Avoid the speed boost with diagonal movement

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        dev_tool = DevTool()
        dev_tool.update_info('coordinates',
                             pygame.math.Vector2(self.rect.centerx / TILESIZE, self.rect.centery / TILESIZE))
        dev_tool.update_info('player_speed', math.sqrt(math.pow(self.direction.x * self.speed, 2) +
                                                       math.pow(self.direction.y * self.speed, 2)))
        dev_tool.update_info('player_dir', round(self.direction, 2))

    def is_collidable(self, sprite, collision_direction):   # Used to reduce collision checking and thus reduce
                                                            # computation costs
        if collision_direction == 'vertical':
            return abs(self.hitbox.centery - sprite.hitbox.centery) < WIDTH // 4
        elif collision_direction == 'horizontal':
            return abs(self.hitbox.centerx - sprite.hitbox.centerx) < HEIGHT // 4

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.is_collidable(sprite, direction):  # Only execute if the collision is conceivable
                    if sprite.hitbox.colliderect(self.hitbox):  # Check the actual collision
                        if self.direction.x > 0:  # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:  # Moving left
                            self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.is_collidable(sprite, direction):
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:  # Moving up
                            self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        self.get_status()  # Get the player animation status

        animation_set = self.animations[self.status]  # Get the good animation_set set

        # Loop with the frame index restricted to the animation set size
        self.frame_index = (self.frame_index + ANIMATION_SPEED) % len(animation_set)

        self.image = animation_set[int(self.frame_index)]  # Get the animation image
        self.rect = self.image.get_rect(center=self.hitbox.center)  # Recalibrate the hitbox

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Verifying all the possible player cooldowns
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()            # Process player inputs
        self.cooldowns()        # Adjust all player cooldowns
        self.animate()          # Animate the player
        self.move(self.speed)   # Move the player
