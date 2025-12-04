# Technology Stack

## Language & Framework
- **Python 3.10+**: Primary development language
- **Pygame 2.5.0+**: Game development framework for 2D graphics, input handling, and game loop

## Build System
- **uv**: Python package manager for dependency management
- **pyproject.toml**: Project configuration and dependency specification

## Common Commands

### Setup
```bash
# Install dependencies
uv sync
```

### Running the Game
```bash
# Run with uv (recommended)
uv run python src/main.py
```

### Development
```bash
# Run game with uv
uv run python src/main.py

# Or activate virtual environment first
source .venv/bin/activate
python src/main.py
```

## Key Libraries
- **pygame**: Core game engine
  - Display management
  - Event handling
  - Sprite rendering
  - Collision detection
  - Clock/FPS management

## Assets
- **assets/kiro-logo.png**: Primary sprite asset used for player and enemy characters
- Fallback: Purple square placeholder if image not found

## Performance Target
- 60 FPS gameplay
- 800x600 resolution
