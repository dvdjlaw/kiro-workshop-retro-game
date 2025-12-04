# Design Document

## Overview

This design enhances the Kiro Shmup game with four key improvements: directional sprite rendering, random enemy AI movement, a health system with visual feedback, and collision damage mechanics. The implementation maintains the existing single-file architecture while adding minimal complexity.

## Architecture

The design follows the existing object-oriented pattern with modifications to the Player and Enemy classes, plus additions to the Game class for health management and asset loading.

### Component Modifications

- **Player class**: Add facing direction tracking and sprite flipping logic
- **Enemy class**: Add random movement AI with boundary checking
- **Game class**: Add health system, heart icon rendering, and collision damage handling with invulnerability frames

### New Assets

- Heart icon (CC0 license) stored in `assets/heart.png`

## Components and Interfaces

### Player Class Enhancements

```python
class Player:
    def __init__(self, x, y, image):
        self.original_image = image  # Store unflipped version
        self.facing_right = True     # Track facing direction
        # ... existing attributes
        
    def update(self, keys, ground_y):
        # Track movement direction and flip sprite accordingly
        # ... existing update logic
```

### Enemy Class Enhancements

```python
class Enemy:
    def __init__(self, x, y, image):
        # ... existing attributes
        self.vel_x = random.choice([-1, 0, 1])
        self.vel_y = random.choice([-1, 0, 1])
        self.direction_timer = 0
        self.direction_change_interval = random.randint(30, 90)  # frames
        
    def update(self):
        # Random movement with boundary checking
        # Periodic direction changes
```

### Game Class Enhancements

```python
class Game:
    def __init__(self):
        # ... existing attributes
        self.heart_image = None  # Loaded heart icon
        
    def init_game(self):
        self.player_health = 1
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 60  # frames (1 second at 60 FPS)
        
    def update(self):
        # Handle collision with health deduction
        # Manage invulnerability frames
        
    def draw_health(self):
        # Render hearts in top left corner
```

## Data Models

### Player State
- `facing_right`: Boolean indicating sprite direction
- `original_image`: Unflipped sprite surface for transformation reference

### Enemy State
- `vel_x`: Horizontal velocity (-1, 0, or 1)
- `vel_y`: Vertical velocity (-1, 0, or 1)
- `direction_timer`: Frame counter for direction changes
- `direction_change_interval`: Random frames between direction changes

### Health System State
- `player_health`: Integer (starts at 1)
- `invulnerable`: Boolean flag for temporary invulnerability
- `invulnerable_timer`: Frame counter for invulnerability duration
- `invulnerable_duration`: Constant frames of invulnerability (60 frames = 1 second)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Sprite direction matches movement

*For any* player movement input (left or right), the sprite's horizontal flip state should match the movement direction (flipped for left, normal for right).

**Validates: Requirements 1.1, 1.2**

### Property 2: Facing direction persists when stationary

*For any* player state with a facing direction, when no movement input is provided, the facing direction should remain unchanged.

**Validates: Requirements 1.3**

### Property 3: Enemy remains in bounds

*For any* enemy position and velocity, after updating position, the enemy should remain within screen boundaries (0 to SCREEN_WIDTH horizontally, ground to top vertically).

**Validates: Requirements 2.2**

### Property 4: Health decreases on collision

*For any* collision between player and enemy when not invulnerable, player health should decrease by exactly 1.

**Validates: Requirements 5.1**

### Property 5: Game over when health depletes

*For any* game state where player health reaches 0, the game state should transition to 'gameOver'.

**Validates: Requirements 5.2**

### Property 6: Game continues when health remains

*For any* collision that leaves player health greater than 0, the game state should remain 'playing'.

**Validates: Requirements 5.3**

### Property 7: Invulnerability prevents damage

*For any* collision that occurs while the invulnerable flag is True, player health should remain unchanged.

**Validates: Requirements 5.4**

### Property 8: Heart display matches health

*For any* player health value, the number of rendered hearts should equal the current health value.

**Validates: Requirements 4.2, 4.3**

## Error Handling

### Asset Loading
- If heart icon fails to load, create a simple red circle as fallback
- Log warning but continue game execution

### Boundary Conditions
- Enemy movement clamped to screen bounds with velocity reversal
- Player health cannot go below 0 or above maximum

### State Management
- Invulnerability timer resets properly after expiration
- Collision detection only active during 'playing' state

## Testing Strategy

### Unit Testing

We'll use pytest for unit testing with the following focus areas:

- **Sprite flipping logic**: Test that facing direction updates correctly based on input
- **Enemy boundary clamping**: Test that enemy stays within screen bounds
- **Health deduction**: Test collision reduces health by 1
- **Invulnerability timing**: Test that invulnerability lasts correct duration
- **Game over trigger**: Test that health = 0 triggers game over state

### Property-Based Testing

We'll use Hypothesis for property-based testing to verify universal properties:

- **Property 1**: Generate random movement sequences, verify sprite always faces movement direction
- **Property 2**: Generate random enemy positions and velocities, verify enemy stays in bounds after update
- **Property 3**: Generate random collision scenarios without invulnerability, verify health decreases
- **Property 4**: Generate game states with health = 0, verify game over state
- **Property 5**: Generate collision scenarios with invulnerability active, verify health unchanged
- **Property 6**: Generate random health values, verify heart count matches

Each property test will run 100 iterations to ensure robust coverage across the input space.

### Integration Testing

- Full game loop with player movement, enemy AI, and collision
- Health system integration with visual feedback
- State transitions from playing to game over based on health

## Implementation Notes

### Sprite Flipping
- Use `pygame.transform.flip(surface, True, False)` for horizontal flipping
- Store original image to avoid cumulative transformation artifacts
- Only flip when direction changes to minimize performance impact

### Random Movement
- Use `random.choice()` for discrete velocity values to keep movement simple
- Change direction every 30-90 frames (0.5-1.5 seconds) for unpredictable but not chaotic movement
- Consider adding slight speed variation for more organic feel

### Health Rendering
- Position hearts at (10, 10) with 40px spacing
- Scale heart icon to 30x30 pixels for visibility
- Consider adding heart outline or background for contrast against dark background

### Invulnerability Feedback
- Optional: Make player sprite flash or semi-transparent during invulnerability
- 1 second (60 frames) provides good balance between fairness and challenge

### Performance
- All changes maintain 60 FPS target
- Sprite flipping is cached, not recalculated every frame
- Random number generation is minimal and not performance-critical
