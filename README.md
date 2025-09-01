# Pygame Adventures

Welcome to **Pygame Adventures**, a collection of fun and engaging 2D games built with Pygame! This repository showcases four unique games: a Super Mario-style platformer, a 3D-style racing game, a classic snake game, and a trivia challenge. Each game offers distinct mechanics and challenges, perfect for players and developers looking to explore Pygame's capabilities.

## Games Included

### Super Mario Style Platformer
A thrilling 2D platformer where you navigate a 10,000px-wide world, collect coins, shoot enemies, and avoid obstacles to reach the finish line.

- **Features**: 
  - Smooth movement and jumping with animated character legs.
  - Shooting mechanics to defeat varied enemies (basic, flying, fast, shooter).
  - Health system (100% max, heal with hearts), multiple lives, and a cheat code (`idkfa` for invincibility).
  - Dynamic world with grass, ice, and stone platforms, plus parallax scrolling backgrounds.
  - Score points for coins (10) and enemies (25).
- **Controls**: Arrow Keys/WASD (move), Space (jump), F (shoot), = (cheat code), R (restart).
- **Objective**: Reach the end of the world while collecting coins and surviving enemies.
- **Directory**: `platformer/`

### In-Car Racer
A pseudo-3D racing game where you drive through a winding two-lane road, dodge traffic, and avoid roadside obstacles to complete a 5,000-meter course.

- **Features**:
  - Realistic driving with acceleration (up to 260 km/h), braking, and speed-dependent steering.
  - Dynamic road with curves changing every 5.6–12.8 seconds.
  - Obstacles like cars, trees, and signs, with a checkered finish line banner.
  - Immersive cockpit view with a rotating steering wheel, speedometer, and progress bar.
  - Score points for each car passed safely.
- **Controls**: W/Up (accelerate), S/Down (brake), A/D or Left/Right (steer), R (restart), Esc (quit).
- **Objective**: Reach the 5,000-meter finish line without crashing.
- **Directory**: `Driving Game/`

### Seb's Snake Game
A classic snake game where you guide a snake to eat apples, grow longer, and achieve a high score while avoiding collisions with yourself or the screen edges.

- **Features**:
  - Grid-based movement with a rotating snake head sprite.
  - Apple collection increases length and score, with dynamic speed (FPS +0.5 per apple).
  - Custom sprites for the snake head (`snakeHead.png`) and apples (`apple.png`).
  - Pause menu and intro screen for an engaging experience.
- **Controls**: Arrow Keys (move), P (pause), C (continue), Q (quit), Space (start/replay).
- **Objective**: Eat as many apples as possible without crashing into the edges or yourself.
- **Directory**: `snake/`

### My Trivia Game
A knowledge-testing trivia game with over 80 multiple-choice questions across various topics, aiming to maximize your score and climb trivia ranks.

- **Features**:
  - 80+ randomized questions on geography, science, literature, history, and pop culture.
  - Scoring system (1 point per correct answer) with 10 trivia levels (Novice to Trivia Genius).
  - Interactive UI with text wrapping, highlighted answers, and feedback (Correct/No good).
  - Intro, feedback, and game over screens for a polished experience.
- **Controls**: A/B/C/D (select answer), Space (start/replay), Enter (continue), Q (quit).
- **Objective**: Answer questions correctly to achieve a high score and top trivia rank.
- **Directory**: `trivia/`

## Installation

To play any of the games in this repository, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/pygame-adventures.git
   cd pygame-adventures
