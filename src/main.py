import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (Kiro brand colors)
BLACK_900 = (13, 13, 13)
PURPLE_500 = (121, 14, 203)
WHITE = (255, 255, 255)
PREY_300 = (156, 163, 175)

# Physics
GRAVITY = 0.3
JUMP_POWER = -6
MOVE_SPEED = 3

class Player:
    def __init__(self, x, y, image):
        self.original_image = pygame.transform.scale(image, (50, 50))
        self.image = self.original_image
        self.facing_right = True
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        
    def update(self, keys, ground_y):
        # Horizontal movement and sprite flipping
        moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        if moving_left:
            self.rect.x -= MOVE_SPEED
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.original_image, True, False)
                
        if moving_right:
            self.rect.x += MOVE_SPEED
            if not self.facing_right:
                self.facing_right = True
                self.image = self.original_image
            
        # Keep player on screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y, image):
        self.original_image = pygame.transform.scale(image, (50, 50))
        self.image = self.original_image
        self.facing_right = True
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Physics attributes (same as Player)
        self.vel_y = 0
        self.on_ground = False
        
        # Random movement AI attributes
        self.move_direction = random.choice([-1, 0, 1])  # -1 = left, 0 = still, 1 = right
        self.direction_timer = 0
        self.direction_change_interval = random.randint(30, 90)
        
    def update(self, ground_y):
        """Update enemy position with physics-based random movement"""
        # Update direction change timer
        self.direction_timer += 1
        
        # Change direction at random intervals
        if self.direction_timer >= self.direction_change_interval:
            # Choose new horizontal movement direction or jump
            action = random.choice(['left', 'right', 'still', 'jump'])
            
            if action == 'left':
                self.move_direction = -1
            elif action == 'right':
                self.move_direction = 1
            elif action == 'still':
                self.move_direction = 0
            elif action == 'jump' and self.on_ground:
                self.vel_y = JUMP_POWER
                self.on_ground = False
            
            self.direction_timer = 0
            self.direction_change_interval = random.randint(30, 90)
        
        # Sprite flipping based on movement direction
        if self.move_direction < 0:  # Moving left
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.move_direction > 0:  # Moving right
            if not self.facing_right:
                self.facing_right = True
                self.image = self.original_image
        
        # Apply horizontal movement
        self.rect.x += self.move_direction * MOVE_SPEED
        
        # Keep enemy on screen horizontally
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        
        # Apply gravity (same as player)
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kiro Shmup")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'  # 'start', 'playing', 'gameOver'
        
        # Load Kiro logo
        try:
            self.kiro_image = pygame.image.load('assets/kiro-logo.png')
        except:
            # Create a placeholder if image not found
            self.kiro_image = pygame.Surface((50, 50))
            self.kiro_image.fill(PURPLE_500)
        
        # Load heart icon for health display
        try:
            heart_loaded = pygame.image.load('assets/heart.png')
            self.heart_image = pygame.transform.scale(heart_loaded, (30, 30))
        except:
            # Create a red circle fallback if image not found
            self.heart_image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.heart_image, (255, 0, 0), (15, 15), 15)
        
        # Ground
        self.ground_y = SCREEN_HEIGHT - 100
        
        # Font
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.init_game()
        
    def init_game(self):
        """Initialize/reset game objects"""
        self.player = Player(100, self.ground_y - 50, self.kiro_image)
        self.enemy = Enemy(600, self.ground_y - 50, self.kiro_image)
        self.player_health = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 60  # frames (1 second at 60 FPS)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == 'start':
                        self.state = 'playing'
                    elif self.state == 'gameOver':
                        self.state = 'start'
                        self.init_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'start':
                    self.state = 'playing'
                elif self.state == 'gameOver':
                    self.state = 'start'
                    self.init_game()
                    
    def update(self):
        if self.state == 'playing':
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.ground_y)
            self.enemy.update(self.ground_y)
            
            # Update invulnerability timer
            if self.invulnerable:
                self.invulnerable_timer -= 1
                if self.invulnerable_timer <= 0:
                    self.invulnerable = False
                    self.invulnerable_timer = 0
            
            # Check collision with enemy
            if self.player.rect.colliderect(self.enemy.rect):
                # Only take damage if not invulnerable
                if not self.invulnerable:
                    self.player_health -= 1
                    
                    # Check if game over
                    if self.player_health <= 0:
                        self.state = 'gameOver'
                    else:
                        # Set invulnerability after taking damage
                        self.invulnerable = True
                        self.invulnerable_timer = self.invulnerable_duration
                
    def draw(self):
        self.screen.fill(BLACK_900)
        
        # Draw ground platform
        pygame.draw.rect(self.screen, PREY_300, 
                        (0, self.ground_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.ground_y))
        
        if self.state == 'start':
            self.draw_start_screen()
        elif self.state == 'playing':
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            self.draw_health()
        elif self.state == 'gameOver':
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            self.draw_game_over_screen()
            
        pygame.display.flip()
        
    def draw_start_screen(self):
        title = self.font_large.render("KIRO SHMUP", True, PURPLE_500)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        instruction = self.font_small.render("Press SPACE or click to start!", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(instruction, instruction_rect)
        
        controls = self.font_small.render("Arrow Keys/WASD to move, SPACE to jump", True, PREY_300)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(controls, controls_rect)
        
    def draw_health(self):
        """Render hearts in top left corner to show player health"""
        for i in range(self.player_health):
            x_pos = 10 + (i * 40)
            y_pos = 10
            self.screen.blit(self.heart_image, (x_pos, y_pos))
    
    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK_900)
        self.screen.blit(overlay, (0, 0))
        
        game_over = self.font_large.render("GAME OVER", True, PURPLE_500)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over, game_over_rect)
        
        restart = self.font_small.render("Press SPACE or click to restart", True, WHITE)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart, restart_rect)
        
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
