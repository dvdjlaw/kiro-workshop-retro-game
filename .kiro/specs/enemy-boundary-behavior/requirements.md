# Requirements Document

## Introduction

This feature improves enemy AI behavior at screen boundaries by ensuring enemies actively move back toward the center when they reach the edge of the screen. This prevents enemies from getting stuck at boundaries and creates more dynamic, engaging gameplay.

## Glossary

- **Enemy**: The AI-controlled hostile character sprite
- **Screen Boundary**: The left (x=0) or right (x=SCREEN_WIDTH - enemy.width) edge of the game screen
- **Center Direction**: Movement toward the horizontal center of the screen (x=SCREEN_WIDTH/2)
- **Boundary Timer**: A countdown timer that enforces minimum duration of center-directed movement
- **Frame**: A single update cycle in the game loop (60 frames per second at 60 FPS)

## Requirements

### Requirement 1

**User Story:** As a player, I want enemies to move away from screen edges, so that gameplay remains dynamic and enemies don't get stuck at boundaries.

#### Acceptance Criteria

1. WHEN an enemy reaches the left screen boundary THEN the Enemy SHALL move right toward the center for at least 60 frames
2. WHEN an enemy reaches the right screen boundary THEN the Enemy SHALL move left toward the center for at least 60 frames
3. WHEN the boundary timer is active THEN the Enemy SHALL ignore random direction changes
4. WHEN the boundary timer expires THEN the Enemy SHALL resume normal random movement behavior
5. WHEN an enemy is moving away from a boundary THEN the Enemy SHALL maintain the same movement speed as normal movement
