# Implementation Plan

- [x] 1. Add boundary behavior attributes to Enemy class
  - Add `boundary_timer` attribute initialized to 0
  - Add `boundary_direction` attribute initialized to 0
  - Position these after existing AI attributes in `__init__`
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement boundary detection logic
  - Add boundary detection at the start of Enemy.update method
  - Check if enemy is at left boundary (rect.x <= 0) and timer is 0
  - Check if enemy is at right boundary (rect.x >= SCREEN_WIDTH - rect.width) and timer is 0
  - Set boundary_timer to 60 and boundary_direction appropriately when boundary is hit
  - _Requirements: 1.1, 1.2_

- [x] 3. Implement boundary timer countdown and movement override
  - Add timer decrement logic that runs every frame
  - When timer > 0, set move_direction to boundary_direction
  - When timer > 0, skip the normal random direction change logic
  - When timer reaches 0, allow normal random movement to resume
  - _Requirements: 1.3, 1.4_

- [x] 4. Write unit tests for boundary behavior
  - Test that hitting left boundary sets timer to 60 and direction to 1
  - Test that hitting right boundary sets timer to 60 and direction to -1
  - Test that boundary_timer decrements each frame
  - Test that enemy moves in boundary_direction while timer is active
  - Test that timer expiration restores normal random movement
  - Test that movement speed remains consistent during boundary movement
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 5. Write property test for boundary activation
  - **Property 1: Boundary triggers center-directed movement**
  - **Validates: Requirements 1.1, 1.2**

- [ ]* 6. Write property test for timer override behavior
  - **Property 2: Boundary timer prevents random direction changes**
  - **Validates: Requirements 1.3**

- [ ]* 7. Write property test for timer expiration
  - **Property 3: Timer expiration restores normal behavior**
  - **Validates: Requirements 1.4**

- [ ]* 8. Write property test for movement speed consistency
  - **Property 4: Movement speed consistency**
  - **Validates: Requirements 1.5**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
