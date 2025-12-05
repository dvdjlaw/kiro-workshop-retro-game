# Requirements Document

## Introduction

This feature introduces a dynamic enemy spawning system that randomly generates pumpkin enemies during gameplay. Instead of a single static enemy, the game will continuously spawn new pumpkin enemies at random intervals and positions, creating a more challenging and engaging gameplay experience. The spawning system will manage enemy lifecycle, prevent overcrowding, and ensure enemies appear in valid gameplay positions.

## Glossary

- **Game System**: The main game controller that manages game state, entities, and the game loop
- **Pumpkin Enemy**: A hostile game entity that moves randomly, collides with the player, and can be spawned dynamically
- **Spawn Point**: A valid screen position where a new enemy can be created
- **Enemy Pool**: The collection of all active enemy entities currently in the game
- **Spawn Interval**: The time duration between enemy spawn attempts
- **Max Enemy Count**: The maximum number of enemies that can exist simultaneously

## Requirements

### Requirement 1

**User Story:** As a player, I want enemies to spawn randomly during gameplay, so that the game becomes progressively more challenging and engaging.

#### Acceptance Criteria

1. WHEN the game state is 'playing' THEN the Game System SHALL attempt to spawn new enemies at random intervals between 2 and 5 seconds
2. WHEN a spawn attempt occurs THEN the Game System SHALL create a new Pumpkin Enemy at a random horizontal position on the ground
3. WHEN spawning an enemy THEN the Game System SHALL ensure the spawn position is at least 100 pixels away from the player's current position
4. WHEN the maximum enemy count is reached THEN the Game System SHALL prevent new enemy spawns until an enemy is removed
5. WHILE the game state is not 'playing' THEN the Game System SHALL not spawn any new enemies

### Requirement 2

**User Story:** As a player, I want enemies to be removed when they are no longer relevant, so that the game performance remains smooth and the screen doesn't become overcrowded.

#### Acceptance Criteria

1. WHEN an enemy moves off the left or right edge of the screen THEN the Game System SHALL remove that enemy from the Enemy Pool
2. WHEN an enemy is removed THEN the Game System SHALL update the active enemy count to allow new spawns
3. WHEN checking for off-screen enemies THEN the Game System SHALL verify the enemy's entire hitbox is beyond the screen boundaries

### Requirement 3

**User Story:** As a player, I want to see visual variety in enemies, so that I can distinguish between different enemy instances.

#### Acceptance Criteria

1. WHEN a Pumpkin Enemy is spawned THEN the Game System SHALL use the pumpkin enemy sprite asset
2. WHERE the pumpkin sprite asset is not available THEN the Game System SHALL use a fallback orange-colored placeholder
3. WHEN rendering enemies THEN the Game System SHALL display all active enemies from the Enemy Pool

### Requirement 4

**User Story:** As a player, I want collision detection to work with all spawned enemies, so that the health system functions correctly with multiple threats.

#### Acceptance Criteria

1. WHEN the player collides with any enemy in the Enemy Pool THEN the Game System SHALL apply damage according to existing health mechanics
2. WHEN checking collisions THEN the Game System SHALL iterate through all active enemies in the Enemy Pool
3. WHEN the player is invulnerable THEN the Game System SHALL not apply damage from any enemy collision

### Requirement 5

**User Story:** As a developer, I want the spawning system to be configurable, so that I can tune gameplay difficulty and performance.

#### Acceptance Criteria

1. THE Game System SHALL define a maximum enemy count constant that limits simultaneous enemies
2. THE Game System SHALL define minimum and maximum spawn interval constants
3. THE Game System SHALL define a minimum spawn distance constant to prevent spawning too close to the player
4. WHEN the game is initialized THEN the Game System SHALL set the maximum enemy count to 5
5. WHEN the game is initialized THEN the Game System SHALL set the minimum spawn distance to 100 pixels

### Requirement 6

**User Story:** As a player, I want the game to reset properly, so that starting a new game provides a fresh experience.

#### Acceptance Criteria

1. WHEN the game transitions to 'start' state THEN the Game System SHALL clear all enemies from the Enemy Pool
2. WHEN the game transitions to 'playing' state THEN the Game System SHALL reset the spawn timer
3. WHEN initializing a new game THEN the Game System SHALL create an empty Enemy Pool
