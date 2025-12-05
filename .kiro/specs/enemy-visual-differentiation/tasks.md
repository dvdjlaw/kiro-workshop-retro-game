# Implementation Plan

- [x] 1. Add spooky green color constant
  - Add SPOOKY_GREEN = (50, 205, 50) to the color constants section
  - Position it after existing Kiro brand colors
  - _Requirements: 1.1_

- [x] 2. Implement green color tint in Enemy class initialization
  - Modify Enemy.__init__ to scale the sprite first
  - Create a copy of the scaled sprite
  - Create a green overlay surface filled with SPOOKY_GREEN
  - Apply the overlay using pygame.BLEND_MULT blending mode
  - Store the tinted sprite as original_image for flipping reference
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [X] 3. Write unit tests for enemy color tinting
  - Test that enemy sprite has green color components after initialization
  - Test that sprite dimensions remain 50x50 after tinting
  - Test that flipped enemy sprites maintain green tint
  - _Requirements: 1.1, 1.3, 1.5_

- [ ]* 4. Write property test for color tint application
  - **Property 1: Green tint is applied during initialization**
  - **Validates: Requirements 1.1**

- [ ]* 5. Write property test for sprite dimension preservation
  - **Property 2: Sprite dimensions preserved after tinting**
  - **Validates: Requirements 1.5**

- [x] 6. Generate new enemy sprite using MCP server
  - Use an MCP image generation server to create a new enemy sprite
  - Specify that the sprite should match the graphical style of the Kiro logo (pixel art/retro style)
  - Request a pumpkin character design that contrasts with the player character
  - Save the generated image to `assets/enemy.png`
  - Ensure the image is suitable for game use (transparent background, appropriate size)
  - _Requirements: 1.1, 1.2, 1.4_

- [x] 7. Update Enemy class to use new sprite asset
  - Modify the Enemy class initialization to load `assets/enemy.png` instead of reusing the Kiro logo
  - Update the image loading in the Game class to pass the enemy sprite to Enemy instances
  - Remove or comment out the green tint code since the new sprite will have its own distinct appearance
  - Test that the new enemy sprite displays correctly in-game
  - _Requirements: 1.1, 1.2, 1.4_

- [ ]* 8. Write unit tests for new enemy sprite loading
  - Test that Enemy class successfully loads enemy.png when it exists
  - Test that Enemy class falls back to Kiro logo when enemy.png doesn't exist
  - Test that sprite dimensions are correct after loading
  - _Requirements: 1.1, 1.5_
