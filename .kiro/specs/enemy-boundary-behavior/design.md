# Design Document

## Overview

This design enhances enemy AI behavior by adding boundary detection and forced center-directed movement when enemies reach screen edges. The implementation modifies the Enemy class's update method to detect boundary collisions and override random movement with center-directed movement for a minimum duration, preventing enemies from lingering at screen edges.

## Architecture

The design follows the existing Enemy class architecture with focused modifications to the update method. The change adds state tracking for boundary detection and timer management without affecting other game systems.

### Component Modifications

- **Enemy class**: Add boundary detection logic and timer state to the `update` method
- **No changes required**: Player, Game, or other classes remain unchanged

## Components and Interfaces

### Enemy Class Enhancement

```python
class Enemy:
    def __init__(self, x, y, image):
        # ... existing initialization ...
        
        # Boundary behavior attributes
        self.boundary_timer = 0
        self.boundary_direction = 0  # -1 = move left, 1 = move right, 0 = no boundary override
        
    def update(self, ground_y):
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
            self.move_direction = self.boundary_direction
            # Skip normal direction change logic while boundary timer is active
        else:
            # Normal random movement logic
            self.direction_timer += 1
            if self.direction_timer >= self.direction_change_interval:
                # ... existing random direction change logic ...
        
        # ... rest of update method (sprite flipping, movement, physics) ...
```

## Data Models

### Enemy Boundary State
- `boundary_timer`: Integer countdown (0-60 frames), tracks remaining frames of forced center movement
- `boundary_direction`: Integer (-1, 0, 1), indicates forced movement direction when timer is active
  - `-1`: Move left (away from right boundary)
  - `0`: No boundary override (normal behavior)
  - `1`: Move right (away from left boundary)

### Timing Constants
- `60 frames`: Minimum duration for boundary escape movement (1 second at 60 FPS)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Boundary triggers center-directed movement

*For any* enemy at a screen boundary (x=0 or x=SCREEN_WIDTH-width), if the boundary timer is not already active, the enemy should set the boundary timer to 60 and set movement direction toward the center.

**Validates: Requirements 1.1, 1.2**

### Property 2: Boundary timer prevents random direction changes

*For any* enemy with an active boundary timer (boundary_timer > 0), the enemy should maintain the boundary_direction and not execute random direction changes.

**Validates: Requirements 1.3**

### Property 3: Timer expiration restores normal behavior

*For any* enemy with boundary_timer = 1, after one update cycle the boundary_timer should be 0 and the enemy should resume normal random movement behavior.

**Validates: Requirements 1.4**

### Property 4: Movement speed consistency

*For any* enemy movement (boundary-directed or random), the horizontal velocity should equal MOVE_SPEED * direction, ensuring consistent movement speed.

**Validates: Requirements 1.5**

## Error Handling

### Boundary Detection
- Boundary detection uses existing rect collision logic (rect.x comparisons)
- No additional error handling needed as boundaries are deterministic

### Timer Management
- Timer decrements to 0 and stops (no negative values)
- Timer only resets when enemy reaches boundary AND timer is 0 (prevents re-triggering during active timer)

### Edge Cases
- If enemy is spawned exactly at boundary, timer activates immediately on first update
- If enemy is pushed to boundary by external force, timer activates normally
- Timer countdown is frame-based, independent of actual time elapsed

## Testing Strategy

### Unit Testing

We'll use pytest for unit testing with the following focus areas:

- **Boundary detection**: Test that hitting left/right boundaries activates the timer
- **Timer countdown**: Test that boundary_timer decrements each frame
- **Forced movement**: Test that enemy moves in boundary_direction while timer is active
- **Timer expiration**: Test that timer reaching 0 restores normal random movement
- **Movement speed**: Test that boundary movement uses same speed as normal movement

### Property-Based Testing

We'll use Hypothesis for property-based testing to verify universal properties:

- **Property 1**: Generate random enemy positions at boundaries, verify timer activation and correct direction
- **Property 2**: Generate random enemy states with active timers, verify no random direction changes occur
- **Property 3**: Generate random enemy states with timer=1, verify timer expires and normal behavior resumes
- **Property 4**: Generate random enemy movement states, verify speed consistency

Each property test will run 100 iterations to ensure robust coverage across the input space.

### Integration Testing

- Visual verification that enemies bounce away from screen edges
- Verify enemies don't get stuck at boundaries during extended gameplay
- Confirm timer duration feels appropriate (1 second minimum)

## Implementation Notes

### Boundary Detection Logic
- Check boundaries at the start of update method before movement
- Only activate timer if `boundary_timer == 0` to prevent re-triggering
- Use existing `rect.x` position for boundary detection

### Timer Management
- Timer decrements every frame regardless of other state
- When timer > 0, skip normal direction change logic entirely
- When timer reaches 0, enemy immediately resumes random behavior

### Movement Priority
1. Boundary timer (highest priority)
2. Random movement (normal priority)
3. Physics and collision (always applied)

### Alternative Approaches Considered
- **Velocity-based**: Push enemy away from boundary with velocity - more complex, unnecessary
- **Teleport**: Move enemy away from boundary instantly - feels unnatural
- **Elastic collision**: Bounce enemy off boundary - too chaotic for this game style

### Performance Considerations
- Two additional integer comparisons per frame per enemy (negligible)
- Two additional integer attributes per enemy (8 bytes total)
- No impact on frame rate or memory usage

### Tuning Parameters
- `60 frames` (1 second) is the minimum duration
- Can be adjusted by changing the timer initialization value
- Longer durations = more predictable enemy movement
- Shorter durations = more chaotic enemy movement
