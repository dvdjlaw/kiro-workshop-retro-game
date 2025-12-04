# Requirements Document

## Introduction

This feature enhances the visual distinction between the player and enemy characters by applying a spooky green color tint to enemy sprites. This improves gameplay clarity by making it immediately obvious which character is hostile.

## Glossary

- **Player**: The player-controlled character sprite (purple Kiro logo)
- **Enemy**: The AI-controlled hostile character sprite
- **Color Tint**: A color overlay applied to a sprite using blend modes
- **BLEND_MULT**: Pygame blending mode that multiplies sprite colors with overlay color
- **Spooky Green**: A bright lime green color (RGB: 50, 205, 50) that creates an eerie, hostile appearance

## Requirements

### Requirement 1

**User Story:** As a player, I want enemies to be visually distinct from my character, so that I can quickly identify threats during gameplay.

#### Acceptance Criteria

1. WHEN the game initializes an enemy THEN the Enemy SHALL apply a green color tint to the sprite
2. WHEN the enemy sprite is rendered THEN the Enemy SHALL display with a spooky green appearance
3. WHEN the enemy changes direction THEN the Enemy SHALL maintain the green color tint on the flipped sprite
4. WHEN comparing player and enemy sprites THEN the visual difference SHALL be immediately apparent
5. WHEN the green tint is applied THEN the Enemy SHALL preserve the original sprite's shape and details
