# Kiro Shmup

An arcade-style side-scrolling game built with Python and Pygame as part of the AWS re:Invent workshop.

## Overview

Kiro Shmup is a simple platformer/shmup hybrid featuring the Kiro logo as the player character. Players navigate a 2D environment, avoiding enemies while demonstrating basic game mechanics like movement, jumping, and collision detection.

## Features

- Player movement and jumping mechanics
- Sonic wave shooting mechanic with rapid-fire capability
- Dynamic enemy spawning system with fast respawn
- Random enemy AI with physics-based movement
- Health system with visual heart display
- Invulnerability frames after taking damage
- Game state management (start, playing, game over)
- Kiro brand visual identity integration
- 60 FPS smooth gameplay

## Setup

### Prerequisites

- Python 3.10+
- uv (Python package manager)

### Installation

Install dependencies:

```bash
uv sync
```

For development (includes testing tools):

```bash
uv sync --extra dev
```

## Running the Game

```bash
uv run python src/main.py
```

Or activate the virtual environment first:

```bash
source .venv/bin/activate
python src/main.py
```

## Controls

- **Arrow Keys** or **WASD**: Move left/right
- **Space** or **Up Arrow** or **W**: Jump
- **X** or **Z**: Shoot sonic waves
- **Space** or **Click**: Start game / Restart after game over

## Testing

This project uses pytest for unit testing. The test suite covers core game mechanics including player movement, enemy AI, health system, and collision detection.

### Run All Tests

```bash
uv run pytest
```

Or with verbose output:

```bash
uv run pytest -v
```

### Run Specific Test Classes

```bash
# Test only Player class
uv run pytest tests/test_main.py::TestPlayer -v

# Test only Enemy class
uv run pytest tests/test_main.py::TestEnemy -v

# Test only Game class
uv run pytest tests/test_main.py::TestGame -v
```

### Run Specific Tests

```bash
# Test player movement
uv run pytest tests/test_main.py::TestPlayer::test_player_move_left -v

# Test health system
uv run pytest tests/test_main.py::TestGame::test_health_decreases_on_collision -v
```

### Test Coverage

The test suite includes 25 tests covering:

**Player Tests (9 tests)**
- Initialization
- Left/right movement
- Screen boundary checking
- Jumping mechanics
- Gravity application
- Ground collision
- Sprite direction persistence

**Enemy Tests (7 tests)**
- Initialization
- Screen boundary checking
- Gravity application
- Ground collision
- Random movement AI
- Direction timer mechanics

**Game Tests (9 tests)**
- Game initialization
- Health decrease on collision
- Game over when health reaches zero
- Invulnerability mechanics
- Invulnerability timer
- Collision damage system
- Game state management
- State reset functionality

### Writing New Tests

When adding new features, follow these patterns:

1. Create test fixtures for common setup
2. Use descriptive test names that explain what is being tested
3. Test both positive and negative cases
4. Mock pygame display and image loading for Game tests
5. Test edge cases and boundary conditions

## Project Structure

```
.
├── .kiro/               # Kiro AI assistant configuration
│   └── steering/        # AI guidance documents
├── assets/              # Game assets
│   ├── heart.png        # Health icon
│   └── kiro-logo.png    # Game sprite asset
├── src/                 # Source code
│   └── main.py          # Main game entry point
├── tests/               # Test suite
│   └── test_main.py     # Unit tests
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # This file
```

## Technology Stack

- **Python 3.10+**: Primary development language
- **Pygame 2.5.0+**: Game development framework
- **pytest 7.4.0+**: Testing framework
- **uv**: Python package manager

## Performance

- Target: 60 FPS gameplay
- Resolution: 800x600

## License

Built for the AWS re:Invent workshop.
