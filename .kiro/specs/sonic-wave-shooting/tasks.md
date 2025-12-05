# Implementation Plan: Sonic Wave Shooting

- [x] 1. Implement SonicWave class
  - Create SonicWave class with initialization, update, and draw methods
  - Initialize wave with position (x, y), radius=0, max_radius, and expansion_rate
  - Implement update() method to expand radius and return lifecycle status
  - Implement draw() method to render ellipse using pygame.draw.ellipse
  - Implement collides_with() method for circle-rectangle collision detection
  - _Requirements: 1.2, 2.1, 2.2, 2.3, 2.5, 3.2_

- [ ]* 1.1 Write property test for wave expansion monotonicity
  - **Property 2: Wave expansion monotonicity**
  - **Validates: Requirements 2.1, 2.5**

- [ ]* 1.2 Write property test for wave position immutability
  - **Property 5: Wave position immutability**
  - **Validates: Requirements 2.5**

- [ ]* 1.3 Write property test for wave lifecycle bounds
  - **Property 3: Wave lifecycle bounds**
  - **Validates: Requirements 2.2**

- [x] 2. Integrate sonic wave into Game class
  - Add self.sonic_wave = None attribute to Game.__init__()
  - Add self.shoot_key_pressed = False attribute to Game.__init__()
  - Reset sonic_wave and shoot_key_pressed in init_game() method
  - _Requirements: 1.1, 1.3, 1.4, 4.4_

- [x] 3. Implement shoot input handling
  - Extend Game.handle_events() to detect shoot key press (e.g., pygame.K_x or pygame.K_z)
  - Create new SonicWave at player center position when shoot key pressed and no active wave
  - Set max_radius to player.rect.height
  - Implement key debouncing using shoot_key_pressed flag
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 3.1 Write property test for single wave constraint
  - **Property 1: Single wave constraint**
  - **Validates: Requirements 1.3**

- [ ]* 3.2 Write property test for wave creation precondition
  - **Property 7: Wave creation precondition**
  - **Validates: Requirements 1.3, 1.4**

- [x] 4. Implement sonic wave update logic
  - In Game.update(), check if self.sonic_wave exists during 'playing' state
  - Call sonic_wave.update() and remove wave if it returns False (reached max radius)
  - Ensure wave updates happen before collision detection
  - _Requirements: 2.1, 2.2, 2.5_

- [x] 5. Implement collision detection and enemy removal
  - In Game.update(), iterate through self.enemies list when sonic_wave exists
  - Call sonic_wave.collides_with(enemy.rect) for each enemy
  - Remove enemies from list where collision detected (use list comprehension)
  - Ensure wave continues expanding after destroying enemies
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 5.1 Write property test for collision implies removal
  - **Property 4: Collision implies removal**
  - **Validates: Requirements 3.1**

- [ ]* 5.2 Write property test for multiple enemy destruction
  - **Property 6: Multiple enemy destruction**
  - **Validates: Requirements 3.4**

- [x] 6. Implement sonic wave rendering
  - In Game.draw(), check if self.sonic_wave exists during 'playing' state
  - Call sonic_wave.draw(self.screen) after drawing enemies
  - Use PURPLE_500 color for wave ellipse
  - Draw wave as filled ellipse with current radius
  - _Requirements: 1.5, 2.3, 2.4_

- [x] 7. Implement state transition cleanup
  - In Game.init_game(), ensure self.sonic_wave is set to None
  - Verify wave is cleared on game over and restart
  - Test wave cleanup when transitioning between game states
  - _Requirements: 4.4, 4.5_

- [ ]* 7.1 Write unit test for state transition cleanup
  - Test wave is cleared when game transitions to 'gameOver'
  - Test wave is cleared when init_game() is called
  - _Requirements: 4.4_

- [ ] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Update start screen instructions
  - Add shoot key instruction to Game.draw_start_screen()
  - Display "Press X to shoot" or similar message
  - Maintain visual consistency with existing UI
  - _Requirements: 1.5_

- [ ]* 9.1 Write unit test for non-regression of existing features
  - Verify Player movement and jumping still work correctly
  - Verify Enemy behavior unchanged except for sonic wave destruction
  - _Requirements: 4.1, 4.2_
