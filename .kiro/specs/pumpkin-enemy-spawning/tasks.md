# Implementation Plan

- [x] 1. Add spawn system constants and initialize enemy pool
  - Add MAX_ENEMIES, MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL, and MIN_SPAWN_DISTANCE constants to the Game class
  - Initialize empty enemy list in __init__ method
  - Initialize spawn_timer and spawn_interval attributes
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 6.3_

- [x] 2. Implement spawn position validation
  - [x] 2.1 Create is_valid_spawn_position method
    - Check horizontal distance from player position
    - Return True if distance >= MIN_SPAWN_DISTANCE, False otherwise
    - _Requirements: 1.3_

  - [ ]* 2.2 Write property test for spawn distance validation
    - **Property 3: Minimum spawn distance from player**
    - **Validates: Requirements 1.3**

  - [x] 2.3 Create get_random_spawn_position method
    - Generate random x-coordinate within screen bounds
    - Validate position using is_valid_spawn_position
    - Retry up to 10 times if position invalid
    - Return valid position or None if no valid position found
    - _Requirements: 1.2, 1.3_

  - [ ]* 2.4 Write property test for ground positioning
    - **Property 2: Spawn position on ground**
    - **Validates: Requirements 1.2**

- [x] 3. Implement enemy spawning logic
  - [x] 3.1 Create attempt_spawn method
    - Check if game state is 'playing'
    - Check if enemy pool size < MAX_ENEMIES
    - Get valid spawn position
    - Create new Enemy instance at spawn position
    - Add enemy to pool
    - Reset spawn timer with new random interval
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [ ]* 3.2 Write property test for pool capacity management
    - **Property 4: Pool capacity management**
    - **Validates: Requirements 1.4, 2.2**

  - [ ]* 3.3 Write property test for state-based spawning
    - **Property 5: No spawning outside playing state**
    - **Validates: Requirements 1.5**

  - [x] 3.4 Create update_spawn_timer method
    - Decrement spawn_timer each frame
    - Call attempt_spawn when timer reaches 0
    - _Requirements: 1.1_

  - [ ]* 3.5 Write property test for spawn timing
    - **Property 1: Spawn timing in playing state**
    - **Validates: Requirements 1.1**

- [x] 4. Implement enemy pool cleanup
  - [x] 4.1 Create remove_offscreen_enemies method
    - Iterate through enemy pool
    - Check if enemy's entire rect is beyond screen boundaries (x + width < 0 or x > SCREEN_WIDTH)
    - Remove off-screen enemies from pool
    - _Requirements: 2.1, 2.3_

  - [ ]* 4.2 Write property test for off-screen removal
    - **Property 6: Off-screen enemy removal**
    - **Validates: Requirements 2.1, 2.3**

- [x] 5. Integrate spawn system into game loop
  - [x] 5.1 Modify init_game method
    - Clear enemy pool (set to empty list)
    - Initialize spawn_timer to 0
    - Set initial spawn_interval
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ]* 5.2 Write property tests for game initialization
    - **Property 11: State transition clears enemies**
    - **Property 12: Playing state resets spawn timer**
    - **Property 13: Initialization creates empty pool**
    - **Validates: Requirements 6.1, 6.2, 6.3**

  - [x] 5.3 Modify update method to manage spawning
    - Call update_spawn_timer when state is 'playing'
    - Update all enemies in pool (iterate and call enemy.update)
    - Call remove_offscreen_enemies after enemy updates
    - _Requirements: 1.1, 2.1_

  - [x] 5.4 Modify collision detection to check all enemies
    - Replace single enemy collision check with loop through enemy pool
    - Apply existing damage logic for each collision
    - Respect invulnerability for all enemies
    - _Requirements: 4.1, 4.2, 4.3_

  - [ ]* 5.5 Write property tests for collision system
    - **Property 9: Collision with any enemy causes damage**
    - **Property 10: Invulnerability prevents all damage**
    - **Validates: Requirements 4.1, 4.3**

  - [x] 5.6 Modify draw method to render all enemies
    - Replace single enemy draw with loop through enemy pool
    - Call draw on each enemy in pool
    - _Requirements: 3.3_

  - [ ]* 5.7 Write property test for enemy rendering
    - **Property 8: All enemies rendered**
    - **Validates: Requirements 3.3**

- [x] 6. Add pumpkin enemy sprite support
  - [x] 6.1 Load pumpkin sprite asset in __init__
    - Attempt to load 'assets/pumpkin.png'
    - Fallback to orange placeholder surface if not found
    - Secondary fallback to existing enemy sprite
    - _Requirements: 3.1, 3.2_

  - [ ]* 6.2 Write property test for sprite consistency
    - **Property 7: Enemy sprite consistency**
    - **Validates: Requirements 3.1**

  - [x] 6.3 Update attempt_spawn to use pumpkin sprite
    - Pass pumpkin_image to Enemy constructor instead of enemy_image
    - _Requirements: 3.1_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 8. Create property-based test infrastructure
  - Set up Hypothesis testing framework
  - Create test fixtures for Game instance
  - Create Hypothesis strategies for random game states
  - Create helper functions for property test assertions
  - _Requirements: All_

- [ ]* 9. Write unit tests for edge cases
  - Test empty pool rendering
  - Test spawn with player at screen edges
  - Test spawn when pool is at max capacity
  - Test all enemies off-screen simultaneously
  - Test collision during invulnerability with multiple enemies
  - _Requirements: All_
