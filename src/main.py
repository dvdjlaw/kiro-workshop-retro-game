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
SPOOKY_GREEN = (50, 205, 50)  # Lime green for spooky enemies

# Physics
GRAVITY = 0.3
JUMP_POWER = -6
MOVE_SPEED = 3

# Shooting
SHOOT_COOLDOWN = 30  # frames (0.5 seconds at 60 FPS)

class SonicWave:
    def __init__(self, x, y, direction):
        """
        Initialize a sonic wave at the given position.
        
        Args:
            x: Center x-coordinate (player center)
            y: Center y-coordinate (player center)
            direction: 1 for right, -1 for left (player's facing direction)
        """
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.speed = 8  # pixels per frame
        self.radius = 15  # Fixed radius for the projectile
        
    def update(self):
        """
        Move the wave horizontally.
        
        Returns:
            True if wave should continue existing, False if off-screen
        """
        self.x += self.speed * self.direction
        
        # Check if wave is off-screen
        if self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius:
            return False
        return True
        
    def draw(self, screen):
        """
        Render the sonic wave as a circle.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw circle with PURPLE_500 color
        pygame.draw.circle(screen, PURPLE_500, (int(self.x), int(self.y)), self.radius, 3)
        
    def collides_with(self, rect):
        """
        Check if wave overlaps with a rectangular enemy.
        
        Uses circle-rectangle collision detection:
        Find the closest point on the rectangle to the circle center,
        then check if that point is within the circle's radius.
        
        Args:
            rect: Pygame Rect object representing enemy bounds
            
        Returns:
            True if circle overlaps rectangle, False otherwise
        """
        # Find the closest point on the rectangle to the circle center
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        
        # Calculate distance from circle center to this closest point
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y
        distance_squared = distance_x ** 2 + distance_y ** 2
        
        # Check if distance is less than radius (collision detected)
        return distance_squared < self.radius ** 2

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
        # Scale the enemy sprite to standard size
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
        
        # Boundary behavior attributes
        self.boundary_timer = 0
        self.boundary_direction = 0
        
    def update(self, ground_y):
        """Update enemy position with physics-based random movement"""
        # Check for boundary collision and set forced direction
        if self.rect.x <= 0 and self.boundary_timer == 0:
            # Hit left boundary - force movement right
            self.boundary_timer = 60  # 1 second at 60 FPS
            self.boundary_direction = 1
        elif self.rect.x >= SCREEN_WIDTH - self.rect.width and self.boundary_timer == 0:
            # Hit right boundary - force movement left
            self.boundary_timer = 60
            self.boundary_direction = -1
        
        # Decrement boundary timer
        if self.boundary_timer > 0:
            self.boundary_timer -= 1
            # Override move_direction with boundary_direction
            self.move_direction = self.boundary_direction
        else:
            # Normal random movement logic (only when timer is 0)
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
    # Spawn system constants
    MAX_ENEMIES = 5
    MIN_SPAWN_INTERVAL = 30  # frames (0.5 seconds at 60 FPS)
    MAX_SPAWN_INTERVAL = 90  # frames (1.5 seconds at 60 FPS)
    EMPTY_SPAWN_INTERVAL = 10  # frames (immediate spawn when no enemies)
    MIN_SPAWN_DISTANCE = 100  # pixels
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kiro Shmup")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'  # 'start', 'playing', 'gameOver'
        
        # Enemy pool and spawn management
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = random.randint(self.MIN_SPAWN_INTERVAL, self.MAX_SPAWN_INTERVAL)
        
        # Sonic wave attributes
        self.sonic_waves = []  # List of active sonic wave projectiles
        self.shoot_key_pressed = False
        self.shoot_cooldown_timer = 0
        
        # Load Kiro logo for player
        try:
            self.kiro_image = pygame.image.load('assets/kiro-logo.png')
        except:
            # Create a placeholder if image not found
            self.kiro_image = pygame.Surface((50, 50))
            self.kiro_image.fill(PURPLE_500)
        
        # Load enemy sprite
        try:
            self.enemy_image = pygame.image.load('assets/enemy.png')
        except:
            # Fallback to Kiro logo if enemy sprite not found
            self.enemy_image = self.kiro_image
        
        # Load pumpkin sprite for spawned enemies
        try:
            self.pumpkin_image = pygame.image.load('assets/pumpkin.png')
        except:
            # Fallback to orange placeholder surface if not found
            self.pumpkin_image = pygame.Surface((50, 50))
            self.pumpkin_image.fill((255, 165, 0))  # Orange color
            # Secondary fallback to existing enemy sprite
            if hasattr(self, 'enemy_image'):
                self.pumpkin_image = self.enemy_image
        
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
        self.enemy = Enemy(600, self.ground_y - 50, self.enemy_image)
        self.player_health = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 60  # frames (1 second at 60 FPS)
        
        # Initialize empty enemy pool and spawn timer
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = random.randint(self.MIN_SPAWN_INTERVAL, self.MAX_SPAWN_INTERVAL)
        
        # Reset sonic wave attributes
        self.sonic_waves = []  # Clear all active sonic waves
        self.shoot_key_pressed = False
        self.shoot_cooldown_timer = 0
    
    def is_valid_spawn_position(self, x):
        """Check if spawn position is far enough from player
        
        Args:
            x: The x-coordinate to validate
            
        Returns:
            True if distance >= MIN_SPAWN_DISTANCE, False otherwise
        """
        horizontal_distance = abs(x - self.player.rect.x)
        return horizontal_distance >= self.MIN_SPAWN_DISTANCE
    
    def get_random_spawn_position(self):
        """Generate random spawn position with validation
        
        Returns:
            Valid x-coordinate for spawn, or None if no valid position found after 10 attempts
        """
        for _ in range(10):
            # Generate random x-coordinate within screen bounds
            # Account for enemy width (50 pixels) to keep fully on screen
            x = random.randint(0, SCREEN_WIDTH - 50)
            
            if self.is_valid_spawn_position(x):
                return x
        
        # No valid position found after 10 attempts
        return None
    
    def attempt_spawn(self):
        """Attempt to spawn a new enemy if conditions are met
        
        Checks:
        - Game state is 'playing'
        - Enemy pool size < MAX_ENEMIES
        - Valid spawn position exists
        
        If all conditions met, creates new Enemy and adds to pool
        """
        # Check if game state is 'playing'
        if self.state != 'playing':
            return
        
        # Check if enemy pool size < MAX_ENEMIES
        if len(self.enemies) >= self.MAX_ENEMIES:
            return
        
        # Get valid spawn position
        spawn_x = self.get_random_spawn_position()
        if spawn_x is None:
            return
        
        # Create new Enemy instance at spawn position (on ground)
        spawn_y = self.ground_y - 50  # Position enemy on ground (50 is enemy height)
        new_enemy = Enemy(spawn_x, spawn_y, self.pumpkin_image)
        
        # Add enemy to pool
        self.enemies.append(new_enemy)
    
    def update_spawn_timer(self):
        """Update spawn timer and trigger spawn attempts
        
        Decrements spawn_timer each frame.
        When timer reaches 0, calls attempt_spawn.
        If no enemies exist, uses faster spawn interval.
        """
        # Decrement spawn_timer each frame
        self.spawn_timer -= 1
        
        # Call attempt_spawn when timer reaches 0
        if self.spawn_timer <= 0:
            self.attempt_spawn()
            
            # If no enemies left, use faster spawn interval
            if len(self.enemies) == 0:
                self.spawn_timer = self.EMPTY_SPAWN_INTERVAL
                self.spawn_interval = self.EMPTY_SPAWN_INTERVAL
            else:
                # Normal spawn interval
                self.spawn_timer = self.spawn_interval
                self.spawn_interval = random.randint(self.MIN_SPAWN_INTERVAL, self.MAX_SPAWN_INTERVAL)
    
    def remove_offscreen_enemies(self):
        """Remove enemies that have moved completely off-screen
        
        Checks if enemy's entire rect is beyond screen boundaries:
        - Left boundary: x + width < 0
        - Right boundary: x > SCREEN_WIDTH
        
        Removes off-screen enemies from the pool.
        """
        # Use list comprehension to keep only on-screen enemies
        self.enemies = [
            enemy for enemy in self.enemies
            if not (enemy.rect.x + enemy.rect.width < 0 or enemy.rect.x > SCREEN_WIDTH)
        ]
        
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
                # Shoot key handling (X or Z)
                elif event.key in (pygame.K_x, pygame.K_z):
                    if self.state == 'playing' and not self.shoot_key_pressed and self.shoot_cooldown_timer <= 0:
                        # Create new SonicWave at player center position
                        center_x = self.player.rect.centerx
                        center_y = self.player.rect.centery
                        # Pass player's facing direction (1 for right, -1 for left)
                        direction = 1 if self.player.facing_right else -1
                        new_wave = SonicWave(center_x, center_y, direction)
                        self.sonic_waves.append(new_wave)  # Add to list of active waves
                        self.shoot_key_pressed = True
                        # Start cooldown timer
                        self.shoot_cooldown_timer = SHOOT_COOLDOWN
            elif event.type == pygame.KEYUP:
                # Reset shoot key flag when key is released
                if event.key in (pygame.K_x, pygame.K_z):
                    self.shoot_key_pressed = False
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
            
            # Update spawn timer and manage spawning
            self.update_spawn_timer()
            
            # Update shoot cooldown timer
            if self.shoot_cooldown_timer > 0:
                self.shoot_cooldown_timer -= 1
            
            # Update all enemies in pool
            for enemy in self.enemies:
                enemy.update(self.ground_y)
            
            # Remove off-screen enemies after updates
            self.remove_offscreen_enemies()
            
            # Update all sonic waves
            waves_to_remove = []
            for wave in self.sonic_waves:
                # Call update() and mark wave for removal if it returns False (off-screen)
                if not wave.update():
                    waves_to_remove.append(wave)
            
            # Remove off-screen waves
            for wave in waves_to_remove:
                self.sonic_waves.remove(wave)
            
            # Collision detection between sonic waves and enemies
            waves_to_remove = []
            for wave in self.sonic_waves:
                # Check if this wave hits any enemy
                hit_enemy = False
                for enemy in self.enemies:
                    if wave.collides_with(enemy.rect):
                        hit_enemy = True
                        break
                
                # Mark wave for removal if it hit an enemy
                if hit_enemy:
                    waves_to_remove.append(wave)
            
            # Remove enemies that collide with any sonic wave
            enemies_to_remove = []
            for enemy in self.enemies:
                for wave in self.sonic_waves:
                    if wave.collides_with(enemy.rect):
                        enemies_to_remove.append(enemy)
                        break
            
            # Remove hit enemies
            for enemy in enemies_to_remove:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
            
            # Remove waves that hit enemies
            for wave in waves_to_remove:
                if wave in self.sonic_waves:
                    self.sonic_waves.remove(wave)
            
            # Update invulnerability timer
            if self.invulnerable:
                self.invulnerable_timer -= 1
                if self.invulnerable_timer <= 0:
                    self.invulnerable = False
                    self.invulnerable_timer = 0
            
            # Check collision with all enemies in pool
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
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
                        
                        # Break after first collision to avoid multiple damage in same frame
                        break
                
    def draw(self):
        self.screen.fill(BLACK_900)
        
        # Draw ground platform
        pygame.draw.rect(self.screen, PREY_300, 
                        (0, self.ground_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.ground_y))
        
        if self.state == 'start':
            self.draw_start_screen()
        elif self.state == 'playing':
            self.player.draw(self.screen)
            # Draw all enemies in pool
            for enemy in self.enemies:
                enemy.draw(self.screen)
            # Draw all sonic waves
            for wave in self.sonic_waves:
                wave.draw(self.screen)
            self.draw_health()
        elif self.state == 'gameOver':
            self.player.draw(self.screen)
            # Draw all enemies in pool
            for enemy in self.enemies:
                enemy.draw(self.screen)
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
        
        shoot_controls = self.font_small.render("Press X or Z to shoot sonic waves", True, PREY_300)
        shoot_controls_rect = shoot_controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(shoot_controls, shoot_controls_rect)
        
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
