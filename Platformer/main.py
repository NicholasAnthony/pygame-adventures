import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)
DARK_GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Player settings
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_SPEED = 5
JUMP_POWER = -15
GRAVITY = 0.7
MAX_HEALTH = 100
ENEMY_DAMAGE = 20  # 20% health loss per enemy hit
INVINCIBILITY_TIME = 60  # Frames of invincibility after taking damage (1 second at 60 FPS)

# Cheat code settings
CHEAT_CODE = "idkfa"  # Classic Doom cheat code for infinite invincibility

# Enemy settings
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
ENEMY_SPEED = 2

# Shooting settings
BULLET_SPEED = 12
BULLET_WIDTH = 8
BULLET_HEIGHT = 3
BULLET_COOLDOWN_FRAMES = 12

# Shooter enemy settings
SHOOTER_ENEMY_WIDTH = 50
SHOOTER_ENEMY_HEIGHT = 50
ENEMY_SHOOT_COOLDOWN_FRAMES = 90
ENEMY_BULLET_SPEED = 6
ENEMY_BULLET_WIDTH = 6
ENEMY_BULLET_HEIGHT = 3
ENEMY_BULLET_DAMAGE = 10

# Explosion settings
EXPLOSION_LIFETIME_FRAMES = 20
EXPLOSION_PARTICLES = 12

# Gun drawing settings
GUN_LENGTH = 22
GUN_HEIGHT = 10
GUN_OFFSET_Y = 14  # vertical offset from player's top
GUN_OFFSET_X = 15   # small overlap into body

# Coin settings
COIN_SIZE = 20

# World generation settings
CHUNK_WIDTH = 800
WORLD_WIDTH = 10000  # Total world width
PLATFORM_MIN_WIDTH = 200  # Increased minimum width to prevent patrol distance issues
PLATFORM_MAX_WIDTH = 400

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.score = 0
        self.lives = 3

        self.health = MAX_HEALTH  # Add health system
        
        # Animation variables for legs
        self.leg_animation_frame = 0
        self.leg_animation_speed = 0.3
        self.leg_swing_angle = 0
        self.jump_animation_frame = 0
        
        # Invincibility system
        self.invincible_frames = 0
        self.is_invincible = False
        self.infinite_invincibility = False  # Cheat code activated
        
        # Shooting
        self.shoot_cooldown = 0
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Update leg animations
        if self.on_ground:
            if abs(self.vel_x) > 0:  # Walking
                self.leg_animation_frame += self.leg_animation_speed
                self.leg_swing_angle = math.sin(self.leg_animation_frame) * 15
            else:  # Standing still
                self.leg_animation_frame = 0
                self.leg_swing_angle = 0
        else:  # In air
            self.jump_animation_frame += 0.2
            self.leg_swing_angle = math.sin(self.jump_animation_frame) * 10
        
        # Update invincibility
        if self.is_invincible and not self.infinite_invincibility:
            self.invincible_frames -= 1
            if self.invincible_frames <= 0:
                self.is_invincible = False

        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Check platform collisions - ORIGINAL SIMPLE SYSTEM
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.jump_animation_frame = 0  # Reset jump animation
                elif self.vel_y < 0:  # Jumping up
                    self.y = platform.y + platform.height
                    self.vel_y = 0
        
        # Keep player on screen horizontally (but allow vertical fall)
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - self.width:
            self.x = WORLD_WIDTH - self.width
            
        # Check if player fell off screen
        if self.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.health = MAX_HEALTH  # Reset health when respawning
            self.is_invincible = False  # Reset invincibility
            self.invincible_frames = 0
            self.x = 100
            self.y = 100
            self.vel_x = 0
            self.vel_y = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            # Spawn bullet from player front
            dir_x = 1 if self.facing_right else -1
            muzzle_x, muzzle_y = self.get_muzzle_position()
            bullet_x = muzzle_x if dir_x == 1 else muzzle_x - BULLET_WIDTH
            bullet_y = muzzle_y - BULLET_HEIGHT // 2
            self.shoot_cooldown = BULLET_COOLDOWN_FRAMES
            return Bullet(bullet_x, bullet_y, dir_x)
        return None
    
    def take_damage(self, damage):
        """Take damage and reduce health"""
        if self.is_invincible or self.infinite_invincibility:
            return False  # Can't take damage while invincible
        
        self.health = max(0, self.health - damage)
        
        # Set invincibility (unless infinite invincibility is active)
        if not self.infinite_invincibility:
            self.is_invincible = True
            self.invincible_frames = INVINCIBILITY_TIME
        
        if self.health <= 0:
            self.lives -= 1
            self.health = MAX_HEALTH
            return True  # Player died
        return False  # Player survived
    
    def activate_cheat_code(self, code):
        """Activate cheat code if correct"""
        if code.lower() == CHEAT_CODE.lower():
            self.infinite_invincibility = True
            self.is_invincible = True
            return True
        return False
    
    def check_collision(self, obj):
        return (self.x < obj.x + obj.width and
                self.x + self.width > obj.x and
                self.y < obj.y + obj.height and
                self.y + self.height > obj.y)
    
    def draw(self, screen, camera_x):
        # Draw player relative to camera
        screen_x = self.x - camera_x
        if -self.width <= screen_x <= SCREEN_WIDTH:
            # Draw player (simple rectangle for now)
            if self.infinite_invincibility:
                # Rainbow effect for infinite invincibility cheat
                rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128)]
                color = rainbow_colors[int(pygame.time.get_ticks() / 100) % len(rainbow_colors)]
            elif self.is_invincible and self.invincible_frames % 10 < 5:
                # Flash white when invincible
                color = WHITE
            else:
                color = BLUE if self.facing_right else (100, 100, 255)
            pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))
            
            # Draw gun
            gun_color = (60, 60, 60)
            if self.facing_right:
                gun_x = screen_x + self.width - GUN_OFFSET_X
                gun_y = self.y + GUN_OFFSET_Y
                pygame.draw.rect(screen, gun_color, (gun_x, gun_y, GUN_LENGTH, GUN_HEIGHT))
                # small stock
                pygame.draw.rect(screen, gun_color, (gun_x - 4, gun_y + 2, 6, 3))
            else:
                gun_x = screen_x - (GUN_LENGTH - GUN_OFFSET_X)
                gun_y = self.y + GUN_OFFSET_Y
                pygame.draw.rect(screen, gun_color, (gun_x, gun_y, GUN_LENGTH, GUN_HEIGHT))
                # small stock
                pygame.draw.rect(screen, gun_color, (gun_x + GUN_LENGTH - 2, gun_y + 2, 6, 3))
            # Draw eyes
            eye_x = screen_x + 27 if self.facing_right else screen_x + 5
            pygame.draw.circle(screen, WHITE, (eye_x, self.y + 8), 5)
            pygame.draw.circle(screen, BLACK, (eye_x, self.y + 8), 2)
            # Draw mouth
            mouth_x = screen_x + 22 if self.facing_right else screen_x + 1
            pygame.draw.rect(screen, RED, (mouth_x, self.y + 22, 10, 5))
            # Draw hair
            pygame.draw.rect(screen, BLACK, (screen_x + 2, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 5, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 8, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 11, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 14, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 17, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 20, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 23, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 26, self.y - 10, 2, 10))
            pygame.draw.rect(screen, BLACK, (screen_x + 29, self.y - 10, 2, 10))
            
            # Draw animated legs
            self.draw_legs(screen, screen_x)

    def get_muzzle_position(self):
        """Return world coordinates of the gun muzzle center."""
        if self.facing_right:
            muzzle_x = self.x + self.width - GUN_OFFSET_X + GUN_LENGTH
        else:
            muzzle_x = self.x - (GUN_LENGTH - GUN_OFFSET_X)
        muzzle_y = self.y + GUN_OFFSET_Y + GUN_HEIGHT // 2
        return muzzle_x, muzzle_y
    
    def draw_legs(self, screen, screen_x):
        """Draw animated legs for the player"""
        # Leg positions relative to player
        left_leg_x = screen_x + 8
        right_leg_x = screen_x + 24
        leg_y = self.y + self.height  # Bottom of player
        
        # Leg dimensions
        leg_width = 4
        leg_height = 12
        
        if self.on_ground:
            if abs(self.vel_x) > 0:  # Walking animation
                # Left leg - swings opposite to right leg
                left_leg_angle = -self.leg_swing_angle
                left_leg_end_x = left_leg_x + math.sin(math.radians(left_leg_angle)) * 8
                left_leg_end_y = leg_y + math.cos(math.radians(left_leg_angle)) * 8
                
                # Right leg - swings with the animation
                right_leg_angle = self.leg_swing_angle
                right_leg_end_x = right_leg_x + math.sin(math.radians(right_leg_angle)) * 8
                right_leg_end_y = leg_y + math.cos(math.radians(right_leg_angle)) * 8
                
                # Draw legs as lines
                pygame.draw.line(screen, (100, 100, 100), (left_leg_x, leg_y), (left_leg_end_x, left_leg_end_y), leg_width)
                pygame.draw.line(screen, (100, 100, 100), (right_leg_x, leg_y), (right_leg_end_x, right_leg_end_y), leg_width)
                
                # Draw feet
                pygame.draw.circle(screen, (80, 80, 80), (int(left_leg_end_x), int(left_leg_end_y)), 3)
                pygame.draw.circle(screen, (80, 80, 80), (int(right_leg_end_x), int(right_leg_end_y)), 3)
            else:  # Standing still
                # Draw straight legs
                pygame.draw.rect(screen, (100, 100, 100), (left_leg_x, leg_y, leg_width, leg_height))
                pygame.draw.rect(screen, (100, 100, 100), (right_leg_x, leg_y, leg_width, leg_height))
                # Draw feet
                pygame.draw.circle(screen, (80, 80, 80), (left_leg_x + leg_width//2, leg_y + leg_height), 3)
                pygame.draw.circle(screen, (80, 80, 80), (right_leg_x + leg_width//2, leg_y + leg_height), 3)
        else:  # Jumping animation
            # Legs swing back and forth while jumping
            left_leg_angle = self.leg_swing_angle
            left_leg_end_x = left_leg_x + math.sin(math.radians(left_leg_angle)) * 6
            left_leg_end_y = leg_y + math.cos(math.radians(left_leg_angle)) * 6
            
            right_leg_angle = -self.leg_swing_angle
            right_leg_end_x = right_leg_x + math.sin(math.radians(right_leg_angle)) * 6
            right_leg_end_y = leg_y + math.cos(math.radians(right_leg_angle)) * 6
            
            # Draw legs as lines
            pygame.draw.line(screen, (100, 100, 100), (left_leg_x, leg_y), (left_leg_end_x, left_leg_end_y), leg_width)
            pygame.draw.line(screen, (100, 100, 100), (right_leg_x, leg_y), (right_leg_end_x, right_leg_end_y), leg_width)
            
            # Draw feet
            pygame.draw.circle(screen, (80, 80, 80), (int(left_leg_end_x), int(left_leg_end_y)), 3)
            pygame.draw.circle(screen, (80, 80, 80), (int(right_leg_end_x), int(right_leg_end_y)), 3)


class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -self.width <= screen_x <= SCREEN_WIDTH:
            if self.platform_type == "grass":
                color = GREEN
            elif self.platform_type == "stone":
                color = BROWN
            elif self.platform_type == "ice":
                color = (200, 200, 255)
            else:
                color = BROWN
            pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, x, y, patrol_distance, enemy_type="basic"):
        self.x = x
        self.y = y
        if enemy_type == "shooter":
            self.width = SHOOTER_ENEMY_WIDTH
            self.height = SHOOTER_ENEMY_HEIGHT
        else:
            self.width = ENEMY_WIDTH
            self.height = ENEMY_HEIGHT
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.direction = 1
        self.speed = ENEMY_SPEED
        self.enemy_type = enemy_type
        # Shooting state for shooter enemies
        self.shoot_cooldown = random.randint(0, ENEMY_SHOOT_COOLDOWN_FRAMES) if enemy_type == "shooter" else 0
    
    def update(self, platforms):
        # Move enemy
        self.x += self.speed * self.direction
        
        # Change direction at patrol boundaries
        if self.x <= self.start_x or self.x >= self.start_x + self.patrol_distance:
            self.direction *= -1
        
        # Apply gravity and check platform collisions
        self.y += 1
        for platform in platforms:
            if self.check_collision(platform):
                self.y = platform.y - self.height
                break
        
        # Tick shooter cooldown
        if self.enemy_type == "shooter" and self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def check_collision(self, obj):
        return (self.x < obj.x + obj.width and
                self.x + self.width > obj.x and
                self.y < obj.y + obj.height and
                self.y + self.height > obj.y)
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -self.width <= screen_x <= SCREEN_WIDTH:
            if self.enemy_type == "basic":
                color = RED
            elif self.enemy_type == "flying":
                color = PURPLE
            elif self.enemy_type == "fast":
                color = ORANGE
            elif self.enemy_type == "shooter":
                color = RED
            else:
                color = RED
                
            pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))
        # Draw eyes
            pygame.draw.circle(screen, WHITE, (screen_x + 8, self.y + 8), 3)
            pygame.draw.circle(screen, BLACK, (screen_x + 8, self.y + 8), 1)

class EnemyBullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = ENEMY_BULLET_WIDTH
        self.height = ENEMY_BULLET_HEIGHT
        self.alive = True
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > WORLD_WIDTH or self.y < -100 or self.y > SCREEN_HEIGHT + 100:
            self.alive = False
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -self.width <= screen_x <= SCREEN_WIDTH:
            pygame.draw.rect(screen, (200, 40, 40), (screen_x, self.y, self.width, self.height))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.direction = direction
        self.speed = BULLET_SPEED * direction
        self.alive = True
    
    def update(self):
        self.x += self.speed
        # Despawn if off world bounds
        if self.x < 0 or self.x > WORLD_WIDTH:
            self.alive = False
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -self.width <= screen_x <= SCREEN_WIDTH:
            pygame.draw.rect(screen, (30, 30, 30), (screen_x, self.y, self.width, self.height))

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.done = False
    
    def update(self):
        self.frame += 1
        if self.frame >= EXPLOSION_LIFETIME_FRAMES:
            self.done = True
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -20 <= screen_x <= SCREEN_WIDTH + 20:
            # Simple particle ring expanding
            progress = self.frame / EXPLOSION_LIFETIME_FRAMES
            radius = int(5 + 25 * progress)
            # Draw multiple colored circles
            pygame.draw.circle(screen, (255, 200, 0), (int(screen_x), int(self.y)), max(1, radius))
            pygame.draw.circle(screen, (255, 120, 0), (int(screen_x), int(self.y)), max(1, int(radius * 0.7)))
            pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(self.y)), max(1, int(radius * 0.3)))

class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.collected = False
        self.animation_frame = 0
        self.heal_amount = 40  # Heal 40% health
        
        # Load heart image
        try:
            self.image = pygame.image.load("heart.png")
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None
    
    def update(self):
        self.animation_frame += 0.1
    
    def check_collision(self, player):
        if not self.collected:
            return (player.x < self.x + self.width and
                    player.x + player.width > self.x and
                    player.y < self.y + self.height and
                    player.y + player.height > self.y)
        return False
    
    def collect(self):
        self.collected = True
    
    def draw(self, screen, camera_x):
        if not self.collected:
            screen_x = self.x - camera_x
            if -self.width <= screen_x <= SCREEN_WIDTH:
                # Animated floating heart
                float_offset = math.sin(self.animation_frame) * 3
                heart_y = self.y + float_offset
                
                if self.image:
                    # Draw heart image with floating animation
                    screen.blit(self.image, (screen_x, heart_y))
                else:
                    # Fallback to simple colored rectangle if image fails to load
                    pygame.draw.rect(screen, (255, 20, 147), (screen_x, heart_y, self.width, self.height))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = COIN_SIZE
        self.height = COIN_SIZE
        self.collected = False
        self.animation_frame = 0
    
    def update(self):
        self.animation_frame += 0.2
    
    def check_collision(self, player):
        if not self.collected:
            return (player.x < self.x + self.width and
                    player.x + player.width > self.x and
                    player.y < self.y + self.height and
                    player.y + player.height > self.y)
        return False
    
    def collect(self):
        self.collected = True
    
    def draw(self, screen, camera_x):
        if not self.collected:
            screen_x = self.x - camera_x
            if -self.width <= screen_x <= SCREEN_WIDTH:
                # Animated coin
                size = int(COIN_SIZE * (0.8 + 0.2 * abs(math.sin(self.animation_frame))))
                offset = (COIN_SIZE - size) // 2
                pygame.draw.circle(screen, YELLOW, (screen_x + COIN_SIZE//2, self.y + COIN_SIZE//2), size//2)
                pygame.draw.circle(screen, (255, 200, 0), (screen_x + COIN_SIZE//2, self.y + COIN_SIZE//2), size//2 - 2)

class Background:
    def __init__(self):
        self.clouds = []
        self.trees = []
        self.mountains = []
        self.generate_background_elements()
    
    def generate_background_elements(self):
        # Generate clouds
        for i in range(30):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(50, 200)
            size = random.randint(10, 80)
            self.clouds.append((x, y, size))
        
        # Generate trees
        for i in range(50):
            x = random.randint(0, WORLD_WIDTH)
            y = SCREEN_HEIGHT - 80
            height = random.randint(40, 80)
            self.trees.append((x, y, height))
        
        # Generate mountains
        for i in range(15):
            x = random.randint(0, WORLD_WIDTH)
            y = SCREEN_HEIGHT - 150
            height = random.randint(100, 200)
            width = random.randint(150, 300)
            self.mountains.append((x, y, width, height))
    
    def draw(self, screen, camera_x):
        # Draw sky gradient
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw mountains (parallax effect)
        for mountain in self.mountains:
            x, y, width, height = mountain
            screen_x = x - camera_x * 0.3  # Slower parallax
            if -width <= screen_x <= SCREEN_WIDTH:
                points = [
                    (screen_x, y + height),
                    (screen_x + width//2, y),
                    (screen_x + width, y + height)
                ]
                pygame.draw.polygon(screen, (139, 69, 19), points)
                pygame.draw.polygon(screen, (160, 82, 45), points, 2)
        
        # Draw clouds (parallax effect)
        for cloud in self.clouds:
            x, y, size = cloud
            screen_x = x - camera_x * 0.1  # Very slow parallax
            if -size <= screen_x <= SCREEN_WIDTH:
                pygame.draw.circle(screen, WHITE, (screen_x, y), size)
                pygame.draw.circle(screen, WHITE, (screen_x + size//2, y), size//2)
                pygame.draw.circle(screen, WHITE, (screen_x - size//2, y), size//2)
        
        # Draw trees (parallax effect)
        for tree in self.trees:
            x, y, height = tree
            screen_x = x - camera_x * 0.5  # Medium parallax
            if -50 <= screen_x <= SCREEN_WIDTH:
                # Tree trunk
                pygame.draw.rect(screen, BROWN, (screen_x - 5, y, 10, height))
                # Tree leaves
                pygame.draw.circle(screen, DARK_GREEN, (screen_x, y - 20), 30)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nicks Basic Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.player = Player(100, 100)
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.hearts = []  # Add hearts list
        self.background = Background()
        
        # Shooting containers
        self.bullets = []
        self.explosions = []
        self.enemy_bullets = []
        
        # Camera and world generation
        self.camera_x = 0
        self.last_generated_x = 0
        
        # Generate initial world
        self.generate_world_segment(0, CHUNK_WIDTH * 2)
        self.generate_hearts()  # Generate hearts
        
        # Game state
        self.game_over = False
        self.win = False
        
        # Cheat code system
        self.cheat_input_active = False
        self.cheat_input_text = ""
        self.cheat_input_font = pygame.font.Font(None, 36)
        
    def generate_world_segment(self, start_x, end_x):
        """Generate platforms, enemies, and coins for a world segment"""
        x = start_x
        
        while x < end_x:
            # Generate ground platform
            if x == 0:
                # Initial ground
                self.platforms.append(Platform(x, SCREEN_HEIGHT - 40, CHUNK_WIDTH, 40, "grass"))
                x += CHUNK_WIDTH
            else:
                # Decide whether to place ground or floating platform
                if random.random() < 0.4:  # 40% chance of ground segment
                    # Generate ground segment
                    ground_width = random.randint(200, 400)
                    self.platforms.append(Platform(x, SCREEN_HEIGHT - 40, ground_width, 40, "grass"))
                    x += ground_width
                else:
                    # Generate floating platform
                    platform_width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
                    
                    # Find valid Y position that doesn't overlap with existing platforms
                    valid_y_found = False
                    attempts = 0
                    platform_y = SCREEN_HEIGHT - 120  # Default starting position
                    
                    while not valid_y_found and attempts < 50:
                        platform_y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 80)
                        valid_y_found = True
                        
                        # Check overlap with existing platforms
                        for platform in self.platforms:
                            # Check X-axis overlap (no more than 10%)
                            x_overlap = 0
                            if x < platform.x + platform.width and x + platform_width > platform.x:
                                overlap_start = max(x, platform.x)
                                overlap_end = min(x + platform_width, platform.x + platform.width)
                                x_overlap = overlap_end - overlap_start
                            
                            # Check Y-axis gap (at least 80px)
                            y_gap = abs(platform_y - platform.y)
                            
                            # If X overlap > 10% or Y gap < 80px, position is invalid
                            if x_overlap > platform_width * 0.1 or y_gap < 80:
                                valid_y_found = False
                                break
                        
                        attempts += 1
                    
                    # If no valid position found, place it at a safe height
                    if not valid_y_found:
                        platform_y = SCREEN_HEIGHT - 120
                    
                    # Choose platform type based on position
                    if x > 2000:
                        platform_type = "stone"
                    elif x > 1000:
                        platform_type = "ice"
                    else:
                        platform_type = "grass"
                    
                    self.platforms.append(Platform(x, platform_y, platform_width, 20, platform_type))
                    
                    # Add enemies on platforms
                    if random.random() < 0.7:  # 70% chance of enemy
                        # Weighted choice including a few shooter enemies
                        enemy_type = random.choices([
                            "basic", "flying", "fast", "shooter"
                        ], weights=[55, 10, 20, 15], k=1)[0]
                        enemy_x = x + random.randint(20, platform_width - 50)
                        # Height accommodates larger shooter
                        enemy_y = platform_y - (SHOOTER_ENEMY_HEIGHT if enemy_type == "shooter" else ENEMY_HEIGHT)
                        # Ensure patrol distance is valid and reasonable
                        min_patrol = 30
                        max_patrol = max(min_patrol + 1, platform_width - 60)
                        patrol_distance = random.randint(min_patrol, max_patrol)
                        self.enemies.append(Enemy(enemy_x, enemy_y, patrol_distance, enemy_type))
                    
                    # Add coins
                    coin_count = random.randint(1, 3)
                    for i in range(coin_count):
                        coin_x = x + random.randint(20, platform_width - 20)
                        coin_y = platform_y - 30
                        self.coins.append(Coin(coin_x, coin_y))
                    
                    x += platform_width
                
                # Add gap between segments (ground or platform)
                gap = random.randint(50, 150)  # Gap between 50-150px
                x += gap
    
    def generate_hearts(self):
        """Generate floating hearts at strategic locations"""
        # Place hearts after 20% through the level, spaced 25% apart
        heart_positions = [
            WORLD_WIDTH * 0.2,   # 20% through
            WORLD_WIDTH * 0.45,  # 45% through (25% after first)
            WORLD_WIDTH * 0.7    # 70% through (25% after second)
        ]
        
        for heart_x in heart_positions:
            # Place heart floating above ground level
            heart_y = SCREEN_HEIGHT - 150
            self.hearts.append(Heart(heart_x, heart_y))
    
    def create_platforms(self):
        # This method is now handled by generate_world_segment
        pass
    
    def create_enemies(self):
        # This method is now handled by generate_world_segment
        pass
    
    def create_coins(self):
        # This method is now handled by generate_world_segment
        pass
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_r and (self.game_over or self.win):
                    self.__init__()  # Restart game
                    self.player.health = MAX_HEALTH  # Ensure health is reset
                    self.player.is_invincible = False  # Reset invincibility
                    self.player.invincible_frames = 0
                elif event.key == pygame.K_EQUALS:  # Press '=' to open cheat input
                    if not self.cheat_input_active:
                        self.cheat_input_active = True
                        self.cheat_input_text = ""
                elif self.cheat_input_active:
                    if event.key == pygame.K_RETURN:  # Enter to submit cheat code
                        if self.player.activate_cheat_code(self.cheat_input_text):
                            # Cheat code activated successfully
                            pass
                        self.cheat_input_active = False
                        self.cheat_input_text = ""
                    elif event.key == pygame.K_ESCAPE:  # Escape to cancel
                        self.cheat_input_active = False
                        self.cheat_input_text = ""
                    elif event.key == pygame.K_BACKSPACE:  # Backspace to delete
                        self.cheat_input_text = self.cheat_input_text[:-1]
                    elif event.unicode.isprintable():  # Add printable characters
                        self.cheat_input_text += event.unicode
                elif event.key == pygame.K_f:  # shoot
                    bullet = self.player.shoot()
                    if bullet is not None:
                        self.bullets.append(bullet)
    
    def update(self):
        if self.game_over or self.win:
            return
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vel_x = -PLAYER_SPEED
            self.player.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vel_x = PLAYER_SPEED
            self.player.facing_right = True
        
        self.player.update(self.platforms)
        
        # Update camera to follow player
        target_camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target_camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        
        # Generate new world segments as player moves right
        if self.player.x > self.last_generated_x - CHUNK_WIDTH:
            new_start = self.last_generated_x
            new_end = new_start + CHUNK_WIDTH
            self.generate_world_segment(new_start, new_end)
            self.last_generated_x = new_end
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.platforms)
            
            # Check collision with player
            if self.player.check_collision(enemy):
                # Use new health system instead of immediate death
                if self.player.take_damage(ENEMY_DAMAGE):
                    # Player died from health loss, reset position
                    self.player.x = 100
                    self.player.y = 100
                    self.player.vel_x = 0
                    self.player.vel_y = 0
                    self.camera_x = 0  # Reset camera

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
        # Remove dead/offscreen bullets
        self.bullets = [b for b in self.bullets if b.alive]

        # Bullet-enemy collisions
        remaining_enemies = []
        for enemy in self.enemies:
            hit = False
            for bullet in self.bullets:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    bullet.alive = False
                    hit = True
                    # Create explosion at enemy center
                    self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                    self.player.score += 25
                    break
            if not hit:
                remaining_enemies.append(enemy)
        self.enemies = remaining_enemies

        # Update explosions
        for exp in self.explosions:
            exp.update()
        self.explosions = [e for e in self.explosions if not e.done]

        # Shooter enemies fire at the player if cooled down and roughly on screen
        for enemy in self.enemies:
            if getattr(enemy, 'enemy_type', 'basic') == 'shooter' and enemy.shoot_cooldown == 0:
                # Aim at player
                dx = (self.player.x + self.player.width / 2) - (enemy.x + enemy.width / 2)
                dy = (self.player.y + self.player.height / 2) - (enemy.y + enemy.height / 2)
                dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
                vx = ENEMY_BULLET_SPEED * dx / dist
                vy = ENEMY_BULLET_SPEED * dy / dist
                bx = enemy.x + enemy.width / 2
                by = enemy.y + enemy.height / 2
                self.enemy_bullets.append(EnemyBullet(bx, by, vx, vy))
                enemy.shoot_cooldown = ENEMY_SHOOT_COOLDOWN_FRAMES

        # Update enemy bullets
        for eb in self.enemy_bullets:
            eb.update()
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]

        # Enemy bullet hits player
        for eb in list(self.enemy_bullets):
            if (self.player.x < eb.x + eb.width and
                self.player.x + self.player.width > eb.x and
                self.player.y < eb.y + eb.height and
                self.player.y + self.player.height > eb.y):
                eb.alive = False
                self.player.take_damage(ENEMY_BULLET_DAMAGE)
        
        # Update coins
        for coin in self.coins:
            coin.update()
            if coin.check_collision(self.player):
                coin.collect()
                self.player.score += 10
        
        # Update hearts
        for heart in self.hearts:
            heart.update()
            if heart.check_collision(self.player):
                heart.collect()
                # Heal player by 40%
                self.player.health = min(MAX_HEALTH, self.player.health + heart.heal_amount)
        
        # Check win condition (reach end of world)
        if self.player.x >= WORLD_WIDTH - 100:
            self.win = True
        
        # Check game over
        if self.player.lives <= 0:
            self.game_over = True
    
    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw background
        self.background.draw(self.screen, self.camera_x)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
        
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen, self.camera_x)
        
        # Draw hearts
        for heart in self.hearts:
            heart.draw(self.screen, self.camera_x)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera_x)
        # Draw enemy bullets
        for eb in self.enemy_bullets:
            eb.draw(self.screen, self.camera_x)
        
        # Draw explosions
        for exp in self.explosions:
            exp.draw(self.screen, self.camera_x)
        
        # Draw player
        self.player.draw(self.screen, self.camera_x)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        font = pygame.font.Font(None, 20)
        
        # Score
        score_text = font.render(f"Score: {self.player.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Coins collected
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        total_coins = len(self.coins)
        coins_text = font.render(f"Coins: {collected_coins}/{total_coins}", True, BLACK)
        self.screen.blit(coins_text, (10, 30))
        
        
        # Lives
        lives_text = font.render(f"Lives: {self.player.lives}", True, BLACK)
        self.screen.blit(lives_text, (10, 50))
        
        # Health bar
        health_text = font.render(f"Health: {self.player.health}%", True, BLACK)
        self.screen.blit(health_text, (10, 70))
        
        # Draw health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 90
        
        # Health bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health bar fill
        health_ratio = self.player.health / MAX_HEALTH
        fill_width = int(bar_width * health_ratio)
        health_color = (
            int(255 * (1 - health_ratio)),  # Red component (more red when low health)
            int(255 * health_ratio),        # Green component (more green when high health)
            0                                # Blue component
        )
        pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Health bar outline
        pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)
        

        # Progress indicator
        #progress = min(100, (self.player.x / WORLD_WIDTH) * 100)
        #progress_text = font.render(f"Progress: {progress:.1f}%", True, BLACK)
        #self.screen.blit(progress_text, (10, 190))
        
        # Cheat code input display
        if self.cheat_input_active:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Draw cheat input prompt
            prompt_text = self.cheat_input_font.render("Enter cheat code:", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(prompt_text, prompt_rect)
            
            # Draw cheat input text
            input_text = self.cheat_input_font.render(self.cheat_input_text + "|", True, WHITE)
            input_rect = input_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(input_text, input_rect)
            
            # Draw instructions
            instructions_text = self.cheat_input_font.render("Press Enter to submit, Escape to cancel", True, WHITE)
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(instructions_text, instructions_rect)
        
        # Game over or win message
        if self.game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        if self.win:
            win_text = font.render("YOU WIN! Press R to restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()