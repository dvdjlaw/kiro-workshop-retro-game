# Project Structure

## Root Directory
```
.
├── .git/                 # Version control
├── .kiro/               # Kiro AI assistant configuration
│   └── steering/        # AI guidance documents
├── .venv/               # Python virtual environment
├── assets/              # Game assets
│   └── kiro-logo.png    # Game sprite asset
├── src/                 # Source code
│   └── main.py          # Main game entry point
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock              # Locked dependency versions
└── README.md            # Project documentation
```

## Code Organization

### src/main.py
Single-file architecture containing all game logic:

- **Constants**: Screen dimensions, FPS, colors, physics values
- **Player class**: Character movement, jumping, collision with ground
- **Enemy class**: Static enemy sprite rendering
- **Game class**: Main game loop, state management, rendering
  - State machine: 'start' → 'playing' → 'gameOver'
  - Event handling
  - Update loop
  - Draw/render methods

## Architecture Pattern
- **Object-oriented**: Classes for game entities (Player, Enemy, Game)
- **Game loop pattern**: Standard update-draw cycle at 60 FPS
- **State machine**: Simple string-based game state management
- **Component-based entities**: Sprites with rect-based collision

## Conventions
- Class names: PascalCase (Player, Enemy, Game)
- Constants: UPPER_SNAKE_CASE (SCREEN_WIDTH, PURPLE_500)
- Methods: snake_case (init_game, draw_start_screen)
- Kiro brand colors defined as RGB tuples
- Physics constants at module level for easy tuning
