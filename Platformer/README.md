# Super Mario Style Platformer

A thrilling 2D platformer game built with Pygame! Navigate a vast world, collect coins, shoot enemies, and avoid obstacles to reach the end!

## Features

- **Player Movement**: Use arrow keys or WASD to move left/right, with animated character legs.
- **Jumping**: Press SPACE to jump with realistic gravity and collision physics.
- **Shooting**: Press F to fire bullets and defeat enemies, with a cooldown to balance gameplay.
- **Coin Collection**: Collect yellow coins to boost your score.
- **Health System**: 100% health bar, reduced by enemy hits (20% damage) or enemy bullets (10% damage). Heal with floating hearts.
- **Multiple Lives**: Start with 3 lives; lose one if health reaches 0 or you fall off-screen.
- **Enemy Variety**:
  - Basic (red, patrols platforms).
  - Flying (purple, moves freely).
  - Fast (orange, quick patrols).
  - Shooter (red, fires bullets at the player).
- **Enemy AI**: Patrol platforms or shoot at the player with timed attacks.
- **Hearts**: Collect floating hearts to restore 40% health.
- **Cheat Code**: Enter `idkfa` (via = key) for infinite invincibility with a rainbow player effect.
- **Dynamic World**: Procedurally generated platforms (grass, stone, ice) across a 10,000px-wide world.
- **Explosions**: Visual effects when enemies are hit by bullets.
- **Enhanced Visuals**: Animated coins, hearts, parallax scrolling background with clouds, trees, and mountains.
- **Score System**: Earn 10 points per coin, 25 points per enemy defeated.
- **Win Condition**: Reach the end of the world (10,000px) to win.

## Controls

- **Left/Right Movement**: Arrow Keys or A/D
- **Jump**: Spacebar
- **Shoot**: F
- **Cheat Code Input**: Press = to open input, type `idkfa`, press Enter to activate, or Escape to cancel
- **Restart**: R (when game over or won)

## How to Play

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run the Game**: `python main.py`
3. **Objective**: Reach the end of the 10,000px world while collecting coins and defeating enemies.
4. **Strategy**:
   - Use platforms to navigate gaps and reach higher areas.
   - Shoot enemies or time movements to avoid them and their bullets.
   - Collect hearts to restore health after taking damage.
5. **Win Condition**: Travel to the world’s end before losing all lives.

## Game Mechanics

- **Gravity**: Realistic falling physics with platform collisions.
- **Health and Damage**: Lose 20% health from enemy collisions, 10% from enemy bullets. Heal 40% with hearts.
- **Invincibility**: 1-second invincibility after taking damage (flashing white) or infinite with cheat code (rainbow effect).
- **Platform Types**: Grass (early game), ice (mid-game), stone (late game) with varying visuals.
- **Enemy AI**: Patrol-based movement for most enemies; shooter enemies aim and fire at the player.
- **World Generation**: Dynamic platforms, enemies, coins, and hearts in 800px chunks, with gaps and varied terrain.
- **Visuals**: Animated player legs, coins, and hearts; parallax scrolling with sky gradient, clouds, trees, and mountains.
- **UI**: Displays score, coins collected, lives, health bar, and progress.

## Tips

- **Plan Jumps**: Time jumps to clear gaps and reach platforms.
- **Enemy Patterns**: Watch enemy patrol and shooting patterns to dodge or attack.
- **Conserve Health**: Grab hearts strategically to survive tougher areas.
- **Use Shooting**: Eliminate enemies with bullets to clear paths and earn points.
- **Cheat Code**: Use `idkfa` for an easier experience if the game feels tough.
- **Explore**: The world is vast—use platforms to explore and find all coins and hearts.

Enjoy the adventure! 🎮