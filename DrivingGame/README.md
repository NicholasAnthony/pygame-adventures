# In-Car Racer

A fast-paced 3D-style racing game built with Pygame! Steer your car through a winding road, avoid traffic and roadside obstacles, and reach the finish line in a 5,000-meter course!

## Features

- **Realistic Driving**: Accelerate (up to 260 km/h), brake, and steer with smooth, responsive controls.
- **Dynamic Road**: Procedurally generated road with smooth curves that change every 5.6–12.8 seconds.
- **Obstacles**: Dodge cars in two lanes and avoid trees/signs on the road's edges.
- **Score System**: Earn 1 point for each car passed without crashing.
- **Progress Tracking**: 5,000-meter course with a progress bar and a checkered finish line banner.
- **Immersive Visuals**:
  - Perspective-based 3D road rendering with dashed center lines and shoulders.
  - Animated steering wheel with visual rotation (up to 180°).
  - Speedometer with needle and digital km/h display.
  - Parallax-effect mountains and a sky gradient background.
- **Cockpit View**: Dashboard overlay with gear indicator (P, N, D), score, and progress bar.
- **Game Over Conditions**: Crash into cars or stray too far off-road into trees/signs.
- **Restart**: Press R to restart after crashing or finishing.

## Controls

- **Accelerate**: W or Up Arrow (up to 260 km/h)
- **Brake**: S or Down Arrow
- **Steer Left/Right**: A/D or Left/Right Arrows
- **Restart**: R (after crash or finish)
- **Quit**: Escape

## How to Play

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run the Game**: `python main.py`
3. **Objective**: Drive 5,000 meters to the finish line while avoiding cars and roadside obstacles.
4. **Strategy**:
   - Accelerate to pass cars but slow down for sharp curves.
   - Steer smoothly to stay in your lane and avoid obstacles.
   - Watch the road's curve to anticipate turns.
5. **Win Condition**: Reach the 5,000-meter finish line without crashing.

## Game Mechanics

- **Driving Physics**:
  - Acceleration: Up to 260 km/h at 120 km/h per second.
  - Braking: 220 km/h per second; natural coasting at 80 km/h per second.
  - Steering: Smooth, speed-dependent steering (less agile at high speeds).
  - Road curves influence car position, requiring counter-steering.
- **Road Generation**: Two-lane road with dynamic curves (left/right) and dashed center lines.
- **Obstacles**:
  - Cars spawn every 3.5–7 seconds in random lanes with slight offsets.
  - Trees and signs spawn every 1.08–2.88 seconds on road edges.
  - Collisions occur if you overlap with cars or veer too far off-road.
- **Score**: Gain 1 point for each car passed safely.
- **Visuals**:
  - 3D perspective road with scrolling animation.
  - Colorful cars (red, blue, green, yellow) with window details.
  - Trees (green with brown trunks) and yellow signs on posts.
  - Checkered finish line banner with "FINISH" text when close.
- **UI**: Displays speed (km/h), gear (P, N, D), score, progress bar, and control hints.

## Tips

- **Balance Speed**: Accelerate to pass cars but slow down for tight curves to avoid crashes.
- **Watch the Road**: The road curves every 5.6–12.8 seconds—steer opposite the curve to stay centered.
- **Avoid Edges**: Stay within the two lanes to avoid hitting trees or signs.
- **Use the Speedometer**: Monitor your speed to judge steering agility (faster = less responsive).
- **Quick Recovery**: If you crash, press R to restart and try again.

Enjoy the race! 🏎️