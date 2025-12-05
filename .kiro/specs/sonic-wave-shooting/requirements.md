# Requirements Document

## Introduction

This feature adds a shooting mechanic to the Kiro Shmup game, allowing the player to emit sonic waves that destroy pumpkin enemies on collision. The sonic waves are visual ellipses that emanate from Kiro's position and expand outward, creating an engaging attack mechanism that fits the game's audio-visual theme.

## Glossary

- **Player**: The Kiro character controlled by the user
- **Sonic Wave**: An expanding elliptical projectile emitted by the Player
- **Pumpkin Enemy**: Enemy entities that can be destroyed by Sonic Waves
- **Game System**: The main game loop and state management system
- **Collision System**: The subsystem responsible for detecting overlaps between game entities

## Requirements

### Requirement 1

**User Story:** As a player, I want to shoot sonic waves at enemies, so that I can actively defend myself and clear obstacles.

#### Acceptance Criteria

1. WHEN the player presses the shoot key, THEN the Game System SHALL create a new Sonic Wave at the Player's current position
2. WHEN a Sonic Wave is created, THEN the Game System SHALL initialize it with zero radius and the Player's center coordinates
3. WHEN the player presses the shoot key while a Sonic Wave is active, THEN the Game System SHALL prevent creation of additional Sonic Waves
4. WHERE the player has released the shoot key and no Sonic Wave is active, the Game System SHALL allow creation of a new Sonic Wave
5. WHEN the shoot key is pressed, THEN the Game System SHALL provide immediate visual feedback through Sonic Wave rendering

### Requirement 2

**User Story:** As a player, I want to see the sonic wave expand from Kiro, so that I can understand the attack's range and timing.

#### Acceptance Criteria

1. WHEN a Sonic Wave exists, THEN the Game System SHALL increase its radius each frame until reaching maximum size
2. WHEN a Sonic Wave reaches maximum radius equal to the Player's height, THEN the Game System SHALL remove the Sonic Wave
3. WHEN rendering a Sonic Wave, THEN the Game System SHALL draw it as an ellipse centered on its origin position
4. WHEN rendering a Sonic Wave, THEN the Game System SHALL use a visually distinct color that contrasts with the background
5. WHILE a Sonic Wave is expanding, the Game System SHALL maintain its center position at the emission point

### Requirement 3

**User Story:** As a player, I want sonic waves to destroy pumpkin enemies on contact, so that I can eliminate threats effectively.

#### Acceptance Criteria

1. WHEN a Sonic Wave collides with a Pumpkin Enemy, THEN the Collision System SHALL remove that Pumpkin Enemy from the game
2. WHEN checking collisions, THEN the Collision System SHALL test overlap between the Sonic Wave's circular area and each Pumpkin Enemy's rectangular bounds
3. WHEN a Sonic Wave destroys a Pumpkin Enemy, THEN the Game System SHALL continue expanding the Sonic Wave normally
4. WHEN multiple Pumpkin Enemies overlap with a Sonic Wave, THEN the Collision System SHALL remove all overlapping enemies
5. WHILE a Sonic Wave is expanding, the Collision System SHALL continuously check for collisions with all active Pumpkin Enemies

### Requirement 4

**User Story:** As a developer, I want the sonic wave system to integrate cleanly with existing game code, so that the feature is maintainable and doesn't break existing functionality.

#### Acceptance Criteria

1. WHEN the Sonic Wave system is added, THEN the Player class SHALL remain unchanged in its core movement and collision behavior
2. WHEN the Sonic Wave system is added, THEN the existing Pumpkin Enemy behavior SHALL remain unchanged except for destruction by Sonic Waves
3. WHEN managing Sonic Waves, THEN the Game System SHALL use the same update-render pattern as other game entities
4. WHEN a game state transition occurs, THEN the Game System SHALL properly clean up any active Sonic Waves
5. WHILE in the 'playing' state, the Game System SHALL update and render Sonic Waves alongside other game entities
