# Technology Stack

## Language & Framework
- **Python 3.10+**: Primary development language
- **Pygame 2.5.0+**: Game development framework for 2D graphics, input handling, and game loop

## Build System
- **uv**: Python package manager for dependency management
- **pyproject.toml**: Project configuration and dependency specification

## Testing
- **pytest 7.4.0+**: Testing framework for unit tests
- **unittest.mock**: Mocking library for isolating components in tests
- Test files located in `tests/` directory
- 25 unit tests covering Player, Enemy, and Game classes

## Development Workflow

### Task Implementation Process
1. Implement the task changes
2. Run tests to validate: `uv run pytest`
3. Fix any failing tests
4. Wait for user's explicit acceptance of the task
5. Upon acceptance, commit changes using conventional commit format with Kiro co-author

### Commit Format
Use conventional commits with co-author attribution:
```
<type>(<scope>): <description>

[optional body]

Co-authored-by: Kiro <kiro@kiro.dev>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

Example:
```bash
git commit -m "test: add comprehensive unit tests for game mechanics

Added 25 unit tests covering Player, Enemy, and Game classes.
Tests validate movement, collision, health system, and AI behavior.

Co-authored-by: Kiro <kiro@kiro.dev>"
```

## Common Commands

### Setup
```bash
# Install dependencies
uv sync

# Install with dev dependencies (includes pytest)
uv sync --extra dev
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

### Testing
```bash
# Run all tests (do this after each task implementation)
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test class
uv run pytest tests/test_main.py::TestPlayer -v
```

## Key Libraries
- **pygame**: Core game engine
  - Display management
  - Event handling
  - Sprite rendering
  - Collision detection
  - Clock/FPS management
- **pytest**: Testing framework
  - Fixtures for test setup
  - Parametrized testing
  - Mocking support

## Assets
- **assets/kiro-logo.png**: Primary sprite asset used for player and enemy characters
- **assets/heart.png**: Health icon for UI display
- Fallback: Purple square placeholder if image not found

## Performance Target
- 60 FPS gameplay
- 800x600 resolution
