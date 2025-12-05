# Design Document: Sonic Wave Shooting

## Overview

The sonic wave shooting system adds an offensive capability to the Kiro Shmup game, allowing players to emit expanding circular projectiles that destroy pumpkin enemies on contact. The system integrates seamlessly with the existing game architecture by following the established update-render pattern and leveraging Pygame's collision detection capabilities.

The feature introduces a new `SonicWave` class to represent individual projectiles, manages wave lifecycle within the `Game` class, and implements circle-rectangle collision detection for enemy destruction. The visual design uses expanding ellipses that grow from the player's center position, creating an intuitive and satisfying attack mechanic.

## Architecture

### Component Overview

The sonic wave system consists of three main components:

1. **SonicWave Class**: Represents individual sonic wave projectiles with position, radius, and expansion logic
2. **Game Class Extensions**: Manages wave creation, updates, rendering, and collision detection
3. **Collision System**: Detects overlaps between circular sonic waves and rectangular enemy bounds

### Integration Points

- **Input Handling**: Extends `Game.handle_events()` to detect shoot key presses
- **Update Loop**: Adds sonic wave updates to `Game.update()` during 'playing' state
- **Render Loop**: Adds sonic wave rendering to `Game.draw()` during 'playing' state
- **Enemy Management**: Integrates with existing `self.enemies` list for collision detection

### Data Flow

```
Player Input (Shoot Key)
    ↓
Game.handle_events() - Create SonicWave
    ↓
Game.update() - Expand wave, check collisions
    ↓
Collision Detection - Remove enemies on hit
    ↓
Game.draw() - Render wave as ellipse
```

## Components and Interfaces

### SonicWave Class

```python
class SonicWave:
    def __init__(self, x, y, max_radius):
        """
        Initialize a sonic wave at the given position.
        
        Args:
            x: Center x-coordinate (player center)
            y: Center y-coordinate (player center)
            max_radius: Maximum radius before wave disappears (player height)
        """
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.expansion_rate = 3  # pixels per frame
        
    def update(self):
        """
        Expand the wave radius.
        
        Returns:
            True if wave should continue existing, False if at max radius
        """
        self.radius += self.expansion_rate
        return self.radius < self.max_radius
        
    def draw(self, screen):
        """
        Render the sonic wave as an ellipse.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw ellipse with current radius
        # Use PURPLE_500 with transparency for visual effect
        
    def collides_with(self, rect):
        """
        Check if wave overlaps with a rectangular enemy.
        
        Args:
            rect: Pygame Rect object representing enemy bounds
            
        Returns:
            True if circle overlaps rectangle, False otherwise
        """
        # Implement circle-rectangle collision detection
```

### Game Class Extensions

**New Attributes:**
- `self.sonic_wave`: Optional[SonicWave] - Currently active wave (None if no wave)
- `self.shoot_key_pressed`: bool - Tracks shoot key state to prevent holding

**Modified Methods:**

```python
def init_game(self):
    # Add initialization
    self.sonic_wave = None
    self.shoot_key_pressed = False

def handle_events(self):
    # Add shoot key detection
    # Create wave on key press if no active wave
    
def update(self):
    # Add sonic wave update logic
    # Check collisions with enemies
    # Remove wave if at max radius
    
def draw(self):
    # Add sonic wave rendering
```

## Data Models

### SonicWave State

- **Position**: (x, y) coordinates - immutable after creation
- **Radius**: Current radius in pixels - increases each frame
- **Max Radius**: Maximum radius before removal - set to player height
- **Expansion Rate**: Pixels per frame growth - constant at 3

### Game State Extensions

- **Active Wave**: Single optional SonicWave instance
- **Shoot Key State**: Boolean flag for input debouncing

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Single wave constraint

*For any* game state, there should be at most one active sonic wave at any time
**Validates: Requirements 1.3**

### Property 2: Wave expansion monotonicity

*For any* sonic wave, its radius should increase monotonically (never decrease) from 0 to max_radius
**Validates: Requirements 2.1, 2.5**

### Property 3: Wave lifecycle bounds

*For any* sonic wave, when its radius reaches or exceeds the player's height, it should be removed from the game
**Validates: Requirements 2.2**

### Property 4: Collision implies removal

*For any* pumpkin enemy that collides with an active sonic wave, that enemy should be removed from the enemies list
**Validates: Requirements 3.1**

### Property 5: Wave position immutability

*For any* sonic wave, its center position (x, y) should remain constant throughout its lifetime
**Validates: Requirements 2.5**

### Property 6: Multiple enemy destruction

*For any* set of pumpkin enemies overlapping with a sonic wave in a single frame, all overlapping enemies should be removed
**Validates: Requirements 3.4**

### Property 7: Wave creation precondition

*For any* shoot key press event, a new sonic wave should be created if and only if no sonic wave currently exists
**Validates: Requirements 1.3, 1.4**

## Error Handling

### Input Edge Cases

- **Rapid key presses**: Debounce shoot key to prevent multiple waves
- **Key held down**: Track key state to require release before next shot
- **Multiple input methods**: Support both spacebar and dedicated shoot key

### Collision Edge Cases

- **Empty enemy list**: Collision check should handle empty list gracefully
- **Enemy removal during iteration**: Use list comprehension or reverse iteration
- **Simultaneous collisions**: Process all collisions in single frame

### State Transition Edge Cases

- **Game over with active wave**: Clear wave on state transition
- **Restart with active wave**: Reset wave to None in `init_game()`
- **Pause/resume**: Wave should continue expanding (or clear on pause)

## Testing Strategy

### Unit Testing

The unit testing approach will verify specific behaviors and edge cases:

**SonicWave Class Tests:**
- Wave initialization with correct position and zero radius
- Wave expansion increases radius by expected amount
- Wave returns False when reaching max radius
- Wave position remains constant during expansion

**Game Integration Tests:**
- Wave creation on shoot key press
- No wave creation when wave already active
- Wave removal when reaching max radius
- Enemy removal on collision with wave

**Edge Case Tests:**
- Empty enemy list collision check
- Multiple enemies destroyed in single frame
- Wave cleanup on game state transitions

### Property-Based Testing

The property-based testing approach will verify universal correctness properties using Hypothesis (Python's PBT library). Each test will run a minimum of 100 iterations with randomly generated inputs.

**Testing Framework:** Hypothesis 6.0+

**Property Test Configuration:**
- Minimum iterations: 100 per property
- Random seed: Configurable for reproducibility
- Shrinking: Enabled to find minimal failing examples

**Property Tests to Implement:**

1. **Single Wave Constraint Test**
   - Generate random sequences of shoot key presses
   - Verify at most one wave exists after each input
   - **Feature: sonic-wave-shooting, Property 1: Single wave constraint**

2. **Wave Expansion Monotonicity Test**
   - Generate random initial wave states
   - Simulate multiple update frames
   - Verify radius never decreases
   - **Feature: sonic-wave-shooting, Property 2: Wave expansion monotonicity**

3. **Wave Lifecycle Bounds Test**
   - Generate random max_radius values
   - Update wave until completion
   - Verify wave removed when radius >= max_radius
   - **Feature: sonic-wave-shooting, Property 3: Wave lifecycle bounds**

4. **Collision Implies Removal Test**
   - Generate random enemy positions and wave states
   - Check collisions and verify enemy removal
   - **Feature: sonic-wave-shooting, Property 4: Collision implies removal**

5. **Wave Position Immutability Test**
   - Generate random initial positions
   - Update wave multiple times
   - Verify (x, y) unchanged
   - **Feature: sonic-wave-shooting, Property 5: Wave position immutability**

6. **Multiple Enemy Destruction Test**
   - Generate random enemy lists with varying overlap
   - Process single frame collision
   - Verify all overlapping enemies removed
   - **Feature: sonic-wave-shooting, Property 6: Multiple enemy destruction**

7. **Wave Creation Precondition Test**
   - Generate random game states (with/without active wave)
   - Simulate shoot key press
   - Verify wave created iff no existing wave
   - **Feature: sonic-wave-shooting, Property 7: Wave creation precondition**

**Test Generators:**
- Enemy position generator: Random (x, y) within screen bounds
- Wave state generator: Random radius between 0 and max_radius
- Input sequence generator: Random shoot key press patterns
- Enemy list generator: Random lists of 0-10 enemies with varied positions

### Integration Testing

- Full gameplay loop with shooting mechanics
- Wave-enemy interaction across multiple frames
- State transitions with active waves
- Performance testing with maximum enemies and active wave
