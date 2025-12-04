import pytest
import pygame
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import Player, Enemy, Game, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_POWER, MOVE_SPEED


@pytest.fixture
def pygame_init():
    """Initialize pygame for tests"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_image():
    """Create a mock pygame surface for testing"""
    surface = pygame.Surface((50, 50))
    surface.fill((255, 0, 255))
    return surface


class TestPlayer:
    """Test suite for Player class"""
    
    def test_player_initialization(self, pygame_init, mock_image):
        """Test that player initializes with correct attributes"""
        player = Player(100, 200, mock_image)
        
        assert player.rect.x == 100
        assert player.rect.y == 200
        assert player.vel_y == 0
        assert player.on_ground == False
        assert player.facing_right == True
        assert player.original_image is not None
    
    def test_player_move_left(self, pygame_init, mock_image):
        """Test player moves left when left key is pressed"""
        player = Player(100, 200, mock_image)
        initial_x = player.rect.x
        
        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False, 
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.rect.x == initial_x - MOVE_SPEED
        assert player.facing_right == False
    
    def test_player_move_right(self, pygame_init, mock_image):
        """Test player moves right when right key is pressed"""
        player = Player(100, 200, mock_image)
        initial_x = player.rect.x
        
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.rect.x == initial_x + MOVE_SPEED
        assert player.facing_right == True
    
    def test_player_stays_in_bounds_left(self, pygame_init, mock_image):
        """Test player cannot move past left screen boundary"""
        player = Player(0, 200, mock_image)
        
        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.rect.x == 0
    
    def test_player_stays_in_bounds_right(self, pygame_init, mock_image):
        """Test player cannot move past right screen boundary"""
        player = Player(SCREEN_WIDTH, 200, mock_image)
        
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.rect.x <= SCREEN_WIDTH - player.rect.width
    
    def test_player_jump(self, pygame_init, mock_image):
        """Test player jumps when space is pressed and on ground"""
        ground_y = 500
        player = Player(100, ground_y - 50, mock_image)
        
        # First update to set player on ground
        keys_no_jump = {pygame.K_LEFT: False, pygame.K_RIGHT: False,
                        pygame.K_SPACE: False, pygame.K_UP: False,
                        pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        player.update(keys_no_jump, ground_y)
        
        # Verify player is on ground
        assert player.on_ground == True
        
        # Now test jump
        keys_jump = {pygame.K_LEFT: False, pygame.K_RIGHT: False,
                     pygame.K_SPACE: True, pygame.K_UP: False,
                     pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys_jump, ground_y)
        
        # Check that player is jumping (negative velocity after gravity is applied)
        assert player.vel_y < 0  # Player should be moving upward
        assert player.on_ground == False

    def test_player_gravity(self, pygame_init, mock_image):
        """Test gravity is applied to player"""
        player = Player(100, 200, mock_image)
        initial_vel_y = player.vel_y
        
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.vel_y == initial_vel_y + GRAVITY
    
    def test_player_ground_collision(self, pygame_init, mock_image):
        """Test player stops at ground level"""
        ground_y = 500
        player = Player(100, ground_y + 10, mock_image)
        player.vel_y = 5
        
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, ground_y)
        
        assert player.rect.bottom == ground_y
        assert player.vel_y == 0
        assert player.on_ground == True
    
    def test_player_maintains_facing_direction_when_stationary(self, pygame_init, mock_image):
        """Test player maintains facing direction when not moving"""
        player = Player(100, 200, mock_image)
        player.facing_right = False
        
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False,
                pygame.K_SPACE: False, pygame.K_UP: False,
                pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}
        
        player.update(keys, 500)
        
        assert player.facing_right == False


class TestEnemy:
    """Test suite for Enemy class"""
    
    def test_enemy_initialization(self, pygame_init, mock_image):
        """Test that enemy initializes with correct attributes"""
        enemy = Enemy(300, 400, mock_image)
        
        assert enemy.rect.x == 300
        assert enemy.rect.y == 400
        assert enemy.vel_y == 0
        assert enemy.on_ground == False
        assert enemy.facing_right == True
        assert enemy.move_direction in [-1, 0, 1]
        assert enemy.direction_timer == 0
        assert 30 <= enemy.direction_change_interval <= 90
    
    def test_enemy_stays_in_bounds_left(self, pygame_init, mock_image):
        """Test enemy cannot move past left screen boundary"""
        enemy = Enemy(0, 200, mock_image)
        enemy.move_direction = -1
        
        enemy.update(500)
        
        assert enemy.rect.x == 0
    
    def test_enemy_stays_in_bounds_right(self, pygame_init, mock_image):
        """Test enemy cannot move past right screen boundary"""
        enemy = Enemy(SCREEN_WIDTH, 200, mock_image)
        enemy.move_direction = 1
        
        enemy.update(500)
        
        assert enemy.rect.x <= SCREEN_WIDTH - enemy.rect.width
    
    def test_enemy_gravity(self, pygame_init, mock_image):
        """Test gravity is applied to enemy"""
        enemy = Enemy(300, 200, mock_image)
        initial_vel_y = enemy.vel_y
        
        enemy.update(500)
        
        assert enemy.vel_y == initial_vel_y + GRAVITY
    
    def test_enemy_ground_collision(self, pygame_init, mock_image):
        """Test enemy stops at ground level"""
        ground_y = 500
        enemy = Enemy(300, ground_y + 10, mock_image)
        enemy.vel_y = 5
        
        enemy.update(ground_y)
        
        assert enemy.rect.bottom == ground_y
        assert enemy.vel_y == 0
        assert enemy.on_ground == True
    
    def test_enemy_direction_timer_increments(self, pygame_init, mock_image):
        """Test enemy direction timer increments each update"""
        enemy = Enemy(300, 200, mock_image)
        initial_timer = enemy.direction_timer
        
        enemy.update(500)
        
        assert enemy.direction_timer == initial_timer + 1
    
    def test_enemy_changes_direction_after_interval(self, pygame_init, mock_image):
        """Test enemy changes direction after reaching interval"""
        enemy = Enemy(300, 200, mock_image)
        enemy.direction_timer = enemy.direction_change_interval - 1
        
        enemy.update(500)
        
        assert enemy.direction_timer == 0


class TestGame:
    """Test suite for Game class"""
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_game_initialization(self, mock_load, mock_display, pygame_init):
        """Test that game initializes with correct state"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        
        assert game.running == True
        assert game.state == 'start'
        assert game.player is not None
        assert game.enemy is not None
        assert game.player_health == 3
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_health_decreases_on_collision(self, mock_load, mock_display, pygame_init):
        """Test player health decreases when colliding with enemy"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        initial_health = game.player_health
        
        # Position player and enemy to collide
        game.player.rect.x = 100
        game.player.rect.y = 100
        game.enemy.rect.x = 100
        game.enemy.rect.y = 100
        
        game.update()
        
        assert game.player_health == initial_health - 1
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_game_over_when_health_zero(self, mock_load, mock_display, pygame_init):
        """Test game transitions to game over when health reaches zero"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.player_health = 1
        
        # Position player and enemy to collide
        game.player.rect.x = 100
        game.player.rect.y = 100
        game.enemy.rect.x = 100
        game.enemy.rect.y = 100
        
        game.update()
        
        assert game.state == 'gameOver'
        assert game.player_health == 0

    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_invulnerability_prevents_damage(self, mock_load, mock_display, pygame_init):
        """Test player doesn't take damage when invulnerable"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.invulnerable = True
        game.invulnerable_timer = 30  # Set timer to keep invulnerability active
        initial_health = game.player_health
        
        # Position player and enemy to collide
        game.player.rect.x = 100
        game.player.rect.y = 100
        game.enemy.rect.x = 100
        game.enemy.rect.y = 100
        
        game.update()
        
        assert game.player_health == initial_health
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_invulnerability_timer_decrements(self, mock_load, mock_display, pygame_init):
        """Test invulnerability timer decrements each frame"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.invulnerable = True
        game.invulnerable_timer = 30
        
        game.update()
        
        assert game.invulnerable_timer == 29
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_invulnerability_expires(self, mock_load, mock_display, pygame_init):
        """Test invulnerability flag clears when timer reaches zero"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.invulnerable = True
        game.invulnerable_timer = 1
        
        game.update()
        
        assert game.invulnerable == False
        assert game.invulnerable_timer == 0
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_collision_sets_invulnerability(self, mock_load, mock_display, pygame_init):
        """Test collision activates invulnerability period"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.player_health = 3
        
        # Position player and enemy to collide
        game.player.rect.x = 100
        game.player.rect.y = 100
        game.enemy.rect.x = 100
        game.enemy.rect.y = 100
        
        game.update()
        
        assert game.invulnerable == True
        assert game.invulnerable_timer == game.invulnerable_duration
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_game_continues_with_health_remaining(self, mock_load, mock_display, pygame_init):
        """Test game continues playing when health is above zero"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.state = 'playing'
        game.player_health = 2
        
        # Position player and enemy to collide
        game.player.rect.x = 100
        game.player.rect.y = 100
        game.enemy.rect.x = 100
        game.enemy.rect.y = 100
        
        game.update()
        
        assert game.state == 'playing'
        assert game.player_health == 1
    
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_init_game_resets_state(self, mock_load, mock_display, pygame_init):
        """Test init_game resets all game state properly"""
        mock_surface = pygame.Surface((50, 50))
        mock_load.return_value = mock_surface
        mock_display.return_value = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = Game()
        game.player_health = 0
        game.invulnerable = True
        game.invulnerable_timer = 30
        
        game.init_game()
        
        assert game.player_health == 3
        assert game.invulnerable == False
        assert game.invulnerable_timer == 0
