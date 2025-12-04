# Design Document

## Overview

This design adds visual differentiation between player and enemy characters by applying a spooky green color tint to enemy sprites. The implementation modifies the Enemy class initialization to apply a color overlay using Pygame's blending capabilities, ensuring enemies are immediately recognizable as hostile while maintaining sprite detail and quality.

## Architecture

The design follows the existing object-oriented pattern with a focused modification to the Enemy class's `__init__` method. The change is isolated to sprite initialization and does not affect game logic, collision detection, or other systems.

### Component Modifications

- **Color Constants**: Add `SPOOKY_GREEN` constant to the color definitions
- **Enemy class**: Modify `__init__` to apply green color tint during sprite initialization
- **No changes required**: Player, Game, or other classes remain unchanged

## Components and Interfaces

### Color Constant Addition

```python
# Add to existing color constants
SPOOKY_GREEN = (50, 205, 50)  # Lime green for spooky enemies
```

### Enemy Class Enhancement

```python
class Enemy:
    def __init__(self, x, y, image):
        # Scale the image first
        scaled_image = pygame.transform.scale(image, (50, 50))
        
        # Create a copy to apply color tint
        self.original_image = scaled_image.copy()
        
        # Create green overlay surface
        green_overlay = pygame.Surface((50, 50))
        green_overlay.fill(SPOOKY_GREEN)
        
        # Apply green tint using multiplicative blending
        self.original_image.blit(green_overlay, (0, 0), special_flags=pygame.BLEND_MULT)
        
        # Set as current image
        self.image = self.original_image
        # ... rest of initialization
```

## Data Models

### Enemy Sprite State
- `original_image`: Sprite surface with green tint applied (used for flipping reference)
- `image`: Current displayed sprite (either original_image or its flipped version)

### Color Definition
- `SPOOKY_GREEN`: RGB tuple (50, 205, 50) - bright lime green for hostile appearance

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Green tint is applied during initialization

*For any* enemy instance created with a valid sprite image, the resulting sprite should contain green color components indicating the tint was applied.

**Validates: Requirements 1.1**

### Property 2: Sprite dimensions preserved after tinting

*For any* enemy sprite after green tint application, the sprite dimensions should remain 50x50 pixels as specified.

**Validates: Requirements 1.5**

## Error Handling

### Sprite Loading
- If the original sprite image fails to load, the existing fallback mechanism (purple square) will be used
- The green tint will still be applied to the fallback sprite

### Blending Operations
- `BLEND_MULT` mode is well-supported in Pygame and should not fail
- If blending fails for any reason, the enemy will display with the original sprite (graceful degradation)

### Performance
- Color tinting occurs once during initialization, not every frame
- No performance impact on game loop or rendering

## Testing Strategy

### Unit Testing

We'll use pytest for unit testing with the following focus areas:

- **Color tint application**: Test that enemy sprite has green color components after initialization
- **Sprite dimensions**: Test that sprite remains 50x50 after tinting
- **Flipped sprite tinting**: Test that flipped enemy sprites maintain green tint
- **Initialization**: Test that Enemy class initializes successfully with tinted sprite

### Property-Based Testing

We'll use Hypothesis for property-based testing to verify universal properties:

- **Property 1**: Generate random sprite images, verify green tint is present after Enemy initialization
- **Property 2**: Generate random sprite images, verify dimensions remain 50x50 after tinting

Each property test will run 100 iterations to ensure robust coverage across the input space.

### Integration Testing

- Visual verification that enemies appear green in-game
- Verify green tint persists during enemy movement and direction changes
- Confirm player sprite remains purple while enemy is green

## Implementation Notes

### Color Blending Approach
- Use `pygame.BLEND_MULT` for multiplicative blending
- This preserves sprite details while applying color tint
- Multiplicative blending darkens the sprite slightly, enhancing the "spooky" effect

### Color Choice
- Lime green (50, 205, 50) provides strong contrast against purple player
- Bright enough to be visible against dark background
- Green is universally associated with "alien" or "hostile" in gaming

### Sprite Transformation Order
1. Scale sprite to 50x50
2. Create copy of scaled sprite
3. Apply green overlay with BLEND_MULT
4. Store as original_image for flipping reference

### Alternative Approaches Considered
- **Color replacement**: Would lose sprite detail
- **Additive blending**: Would make sprite too bright
- **Hue shifting**: More complex, unnecessary for this use case

### Performance Considerations
- Tinting happens once per enemy during initialization
- No per-frame overhead
- Flipping uses the pre-tinted original_image, so tint is preserved automatically

### Visual Quality
- BLEND_MULT preserves alpha channel and transparency
- Sprite details remain visible through the tint
- Color intensity can be adjusted by changing SPOOKY_GREEN RGB values
