# Seb's Snake Game

A classic 2D snake game built with Pygame! Guide your snake to eat apples, grow longer, and achieve a high score while avoiding collisions with yourself or the screen edges.

## Features

- **Snake Movement**: Control the snake's direction with arrow keys, with smooth grid-based movement.
- **Apple Collection**: Eat apples to grow longer and increase your score.
- **Dynamic Speed**: Game speed increases slightly as the snake grows (FPS increases by 0.5 per apple).
- **Visuals**:
  - Custom snake head sprite that rotates based on direction.
  - Apple sprite for food, with a 35x35 pixel size.
  - Green snake body and white background for a clean look.
- **Score System**: Score equals the number of apples eaten (snake length minus 1).
- **Game Over**: Collide with the screen edges or the snake's body to end the game.
- **Pause Menu**: Pause the game to take a break or quit.
- **Intro Screen**: Welcoming screen with instructions before starting.
- **Game Over Screen**: Option to restart or quit after losing.

## Controls

- **Move**: Arrow Keys (Left, Right, Up, Down)
- **Pause**: P
- **Continue (from pause)**: C
- **Quit (from pause or game over)**: Q
- **Start/Replay (from intro or game over)**: Spacebar
- **Quit Game**: Close window

## How to Play

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run the Game**: `python main.py`
3. **Objective**: Eat as many apples as possible to grow the snake and increase your score.
4. **Strategy**:
   - Navigate the snake to collect apples, which spawn randomly on the 800x600 grid.
   - Avoid hitting the screen edges or the snake's own body.
   - Pause with P to take a break when needed.
5. **Game Over**: Collide with the screen edges or yourself to lose; press Spacebar to replay or Q to quit.

## Game Mechanics

- **Movement**: Snake moves in 20x20 pixel grid steps, controlled by arrow keys, with one direction change per frame.
- **Apple Collection**: Eating an apple increases the snake's length by 1 and spawns a new apple randomly.
- **Collision Detection**:
  - Game over if the snake hits the screen boundaries (800x600).
  - Game over if the snake's head collides with its body.
- **Speed**: Base FPS is 15, increasing by 0.5 per apple eaten, making the game faster as you grow.
- **Visuals**:
  - Snake head uses a rotating `snakeHead.png` sprite (up, down, left, right).
  - Body is drawn as green 20x20 rectangles.
  - Apples use a 35x35 `apple.png` sprite.
- **UI**: Displays score (apples eaten) in the top-left corner, pause menu, intro screen, and game over screen with instructions.

## Tips

- **Plan Your Path**: Anticipate the snake’s growth to avoid trapping yourself in corners.
- **Use Pause**: Press P to pause and strategize if the game feels fast.
- **Watch the Speed**: As you eat apples, the game speeds up—stay focused!
- **Avoid Tight Turns**: Quick direction changes can lead to self-collisions, especially with a long snake.
- **Maximize Space**: Use the full 800x600 grid to give yourself room to maneuver.

Enjoy the challenge! 🐍