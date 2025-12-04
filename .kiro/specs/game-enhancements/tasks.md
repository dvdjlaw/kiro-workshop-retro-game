# Implementation Plan

- [x] 1. Add sprite direction tracking and flipping to Player class
  - Modify Player.__init__ to store original_image and facing_right flag
  - Update Player.update to detect left/right movement and set facing_right accordingly
  - Add sprite flipping logic using pygame.transform.flip when direction changes
  - Ensure sprite maintains last facing direction when stationary
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement random movement AI for Enemy class
  - Add velocity attributes (vel_x, vel_y) to Enemy.__init__ with random initial values
  - Add direction change timer and interval attributes
  - Create Enemy.update method with random movement logic
  - Implement boundary checking to keep enemy within screen bounds
  - Add periodic random direction changes every 30-90 frames
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Add heart_image (assets/heart.png) loading in Game.__init__ with fallback to red circle
  - Scale heart icon to 30x30 pixels for UI display
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Implement health system with visual heart display
  - Add player_health attribute to Game.init_game (initialize to 3)
  - Create Game.draw_health method to render hearts in top left corner
  - Position hearts at (10, 10) with 40px spacing between multiple hearts
  - Call draw_health from Game.draw during playing state
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 5. Add collision damage and invulnerability mechanics
  - Add invulnerable, invulnerable_timer, and invulnerable_duration attributes to Game.init_game
  - Modify collision detection in Game.update to deduct health instead of instant game over
  - Set invulnerable flag and timer when collision occurs
  - Decrement invulnerability timer each frame and clear flag when expired
  - Only trigger game over when health reaches 0
  - Prevent damage during invulnerability period
  - _Requirements: 5.1, 5.2, 5.3, 5.4_
