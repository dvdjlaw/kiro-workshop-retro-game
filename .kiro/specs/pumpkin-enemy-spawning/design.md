# Design Document

## Overview

The pumpkin enemy spawning system transforms the game from a single static enemy to a dynamic multi-enemy experience. The design introduces a spawn manager within the Game class that handles enemy lifecycle: creation at random intervals, position validation, pool management, and cleanup. This system integrates seamlessly with existing enemy AI, collision detection, and health mechanics while maintaining 60 FPS performance.

## Architecture

### Component Structure

```
Game (existing)
├── Enemy Pool (new) - List of active Enemy instances
├── Spawn Manager (new) - Handles spawn timing and logic
│   ├── Spawn Timer
│   ├── Spawn Interval (randomized)
│   └── Position Validator
├── Player (existing)
└── Collision System (modified) - Now checks all enemies
```

### Data Flow

1. **Spawn Cycle**: Game loop → Spawn Manager checks timer → Validates conditions → Creates Enemy → Adds to Pool
2. **Update Cycle**: Game loop → Updates all enemies in Pool → Checks boundaries → Removes off-screen enemies
3. **Collision Cycle**: Game loop → Iterates Enemy Pool → Checks player collision → Applies damage if valid

## Components and Interfaces

### Spawn Manager (integrated into Game class)

**Attributes:**
- `enemies: List[Enemy]` - Active enemy pool
- `spawn_timer: int` - Frames until next spawn attempt
- `spawn_interval: int` - Current randomized interval (120-300 frames = 2-5 seconds at 60 FPS)
- `MAX_ENEMIES: int = 5` - Maximum simultaneous enemies
- `MIN_SPAWN_DISTANCE: int = 100` - Minimum pixels from player
- `MIN_SPAWN_INTERVAL: int = 120` - Minimum frames between spawns (2 seconds)
- `MAX_SPAWN_INTERVAL: int = 300` - Maximum frames between spawns (5 seconds)

**Methods:**
- `attempt_spawn() -> None` - Checks conditions and spawns enemy if valid
- `get_random_spawn_position() -> int` - Returns valid x-coordinate for spawn
- `is_valid_spawn_position(x: int) -> bool` - Validates position is far enough from player
- `remove_offscreen_enemies() -> None` - Cleans up enemies beyond screen bounds
- `update_spawn_timer() -> None` - Decrements timer and triggers spawn attempts

### Enemy Class (existing, no changes needed)

The existing Enemy class already supports:
- Physics-based movement with gravity
- Random AI behavior
- Boundary collision detection
- Sprite rendering

### Modified Game Methods

**`init_game()`** - Initialize empty enemy pool and spawn timer
**`update()`** - Update all enemies, check collisions with all enemies, manage spawning
**`draw()`** - Render all enemies in the pool

## Data Models

### Enemy Pool Structure
```python
# List-based pool for simple iteration and management
enemies: List[Enemy] = []

# Example state:
# [Enemy(x=600, y=500), Enemy(x=300, y=500), Enemy(x=750, y=500)]
```

### Spawn State
```python
spawn_timer: int = 0  # Counts down each frame
spawn_interval: int = random.randint(120, 300)  # Randomized each spawn
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Spawn timing in playing state

*For any* game session in 'playing' state, when sufficient time has elapsed, the spawn system should create new enemies at intervals between 2 and 5 seconds.

**Validates: Requirements 1.1**

### Property 2: Spawn position on ground

*For any* spawn attempt, the newly created enemy should be positioned with its bottom edge at the ground level.

**Validates: Requirements 1.2**

### Property 3: Minimum spawn distance from player

*For any* player position and any spawned enemy, the horizontal distance between the player and the newly spawned enemy should be at least 100 pixels.

**Validates: Requirements 1.3**

### Property 4: Pool capacity management

*For any* game state, when the enemy pool is at maximum capacity, spawn attempts should not increase the pool size, and when an enemy is removed from a full pool, a new spawn should be possible.

**Validates: Requirements 1.4, 2.2**

### Property 5: No spawning outside playing state

*For any* game state other than 'playing', the spawn system should not create new enemies regardless of time elapsed.

**Validates: Requirements 1.5**

### Property 6: Off-screen enemy removal

*For any* enemy in the pool, when the enemy's entire hitbox moves beyond the left or right screen boundary, that enemy should be removed from the pool.

**Validates: Requirements 2.1, 2.3**

### Property 7: Enemy sprite consistency

*For any* spawned enemy, the enemy should use the pumpkin sprite asset (or fallback if unavailable).

**Validates: Requirements 3.1**

### Property 8: All enemies rendered

*For any* game frame in 'playing' state, the number of enemies drawn to the screen should equal the number of enemies in the active pool.

**Validates: Requirements 3.3**

### Property 9: Collision with any enemy causes damage

*For any* enemy in the pool, when the player collides with that enemy and is not invulnerable, the player's health should decrease.

**Validates: Requirements 4.1**

### Property 10: Invulnerability prevents all damage

*For any* enemy in the pool, when the player is invulnerable and collides with that enemy, the player's health should not decrease.

**Validates: Requirements 4.3**

### Property 11: State transition clears enemies

*For any* enemy pool state, when the game transitions to 'start' state, the enemy pool should become empty.

**Validates: Requirements 6.1**

### Property 12: Playing state resets spawn timer

*For any* spawn timer value, when the game transitions to 'playing' state, the spawn timer should be reset to trigger the first spawn.

**Validates: Requirements 6.2**

### Property 13: Initialization creates empty pool

*For any* game initialization, the enemy pool should be empty immediately after initialization.

**Validates: Requirements 6.3**

## Error Handling

### Spawn Position Validation
- If no valid spawn position exists (player occupies entire screen), skip spawn attempt
- Log warning if spawn attempts fail repeatedly (indicates configuration issue)

### Asset Loading
- Gracefully fallback to orange placeholder if pumpkin sprite not found
- Use existing enemy sprite as secondary fallback
- Ensure game continues even with missing assets

### Pool Management
- Prevent negative pool sizes through defensive checks
- Cap pool at MAX_ENEMIES even if removal logic fails
- Handle empty pool gracefully in collision and render loops

### Performance
- Limit enemy updates to active pool only
- Use list comprehension for efficient off-screen removal
- Avoid creating new lists each frame (modify in place when possible)

## Testing Strategy

### Unit Testing

The unit testing approach will verify specific scenarios and edge cases:

**Spawn System Tests:**
- Test spawn at exact timer expiration
- Test spawn with player at screen edges
- Test spawn when pool is at max capacity
- Test spawn in non-playing states

**Pool Management Tests:**
- Test adding enemies to empty pool
- Test removing specific enemies from pool
- Test clearing entire pool on state change

**Collision Tests:**
- Test collision with first enemy in pool
- Test collision with last enemy in pool
- Test collision during invulnerability

**Edge Cases:**
- Empty pool rendering
- Single enemy in pool
- All enemies off-screen simultaneously

### Property-Based Testing

The property-based testing approach will verify universal properties across many randomized inputs using **Hypothesis** (Python's property-based testing library).

**Configuration:**
- Each property test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate random game states
- Each test will be tagged with the format: `**Feature: pumpkin-enemy-spawning, Property {number}: {property_text}**`

**Test Generators:**
- Random player positions (0 to SCREEN_WIDTH)
- Random enemy pool sizes (0 to MAX_ENEMIES + 2)
- Random game states ('start', 'playing', 'gameOver')
- Random spawn timer values (0 to MAX_SPAWN_INTERVAL + 50)
- Random enemy positions (including off-screen)

**Property Test Coverage:**
- Property 1: Spawn timing verification across random game durations
- Property 2: Ground positioning for all spawned enemies
- Property 3: Distance validation for all player/enemy combinations
- Property 4: Capacity constraints across random pool operations
- Property 5: State-based spawn prevention
- Property 6: Boundary detection for all enemy positions
- Property 7: Sprite assignment verification
- Property 8: Render count matching pool size
- Property 9: Damage application for all enemies
- Property 10: Invulnerability across all enemies
- Property 11: Pool clearing on state transitions
- Property 12: Timer reset verification
- Property 13: Initialization state verification

Each correctness property will be implemented as a single property-based test that validates the universal behavior across the generated input space.

## Implementation Notes

### Integration Points

1. **Game.__init__()**: Add enemy pool and spawn timer initialization
2. **Game.init_game()**: Reset pool and timer for new games
3. **Game.update()**: Add spawn management and multi-enemy collision checks
4. **Game.draw()**: Iterate and render all enemies in pool
5. **Enemy class**: No changes needed (already supports required behavior)

### Performance Considerations

- Target: Maintain 60 FPS with 5 active enemies
- Each enemy update is O(1), total enemy updates O(n) where n ≤ 5
- Collision checks: O(n) iteration through enemy pool
- Off-screen removal: O(n) single pass with list comprehension
- Expected performance impact: Negligible (< 1ms per frame for 5 enemies)

### Configuration Tuning

Difficulty can be adjusted by modifying constants:
- Increase MAX_ENEMIES for more challenge
- Decrease MIN_SPAWN_INTERVAL for faster spawning
- Decrease MIN_SPAWN_DISTANCE for more aggressive spawns
- Add spawn rate acceleration over time (future enhancement)
