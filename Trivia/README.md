# My Trivia Game

A fun and challenging trivia game built with Pygame! Test your knowledge with 80+ questions across various topics, earn points, and climb the ranks from Novice to Trivia Genius!

## Features

- **Extensive Question Bank**: Over 80 multiple-choice questions covering geography, science, literature, history, pop culture, and more.
- **Scoring System**: Earn 1 point for each correct answer; track your score and total questions answered.
- **Trivia Levels**: Progress from Novice (0–5 points) to Trivia Genius (46+ points) based on your score.
- **Interactive UI**:
  - Clear question display with text wrapping for long questions.
  - Highlighted answer options (A, B, C, D) when selected.
  - Feedback screen with "Correct!" or "No good" messages in green or red.
  - Score and trivia level displayed in the top-left corner.
- **Game States**:
  - Intro screen with instructions.
  - Playing state for answering questions.
  - Feedback state showing answer results.
  - Game Over screen with final score and level.
- **Responsive Controls**: Use A, B, C, D keys to select answers, with Space and Q for navigation.

## Controls

- **Select Answer**: A, B, C, D keys
- **Start/Replay**: Spacebar (from intro or game over)
- **Continue (from feedback)**: Enter
- **Quit**: Q (from intro or game over)
- **Exit Game**: Close window

## How to Play

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run the Game**: `python main.py`
3. **Objective**: Answer as many trivia questions correctly as possible to maximize your score and achieve a high trivia level.
4. **Strategy**:
   - Read each question carefully and select the correct answer (A, B, C, or D).
   - Review feedback after each answer to learn from mistakes.
   - Continue through all 80+ questions or quit early if desired.
5. **Game Over**: Reach the end of the question bank or press Q to see your final score and trivia level.

## Game Mechanics

- **Questions**: 80+ randomized multiple-choice questions with four options each, covering topics like capitals, science, literature, and pop culture.
- **Scoring**: +1 point for each correct answer; tally tracks total questions answered.
- **Trivia Levels**: 10 levels (Novice, Beginner, Amateur, Enthusiast, Intermediate, Advanced, Expert, Master, Trivia Guru, Trivia Genius) based on score thresholds (0–46+).
- **Feedback**: After each answer, see "Correct!" (green) or "No good, the correct answer was [X]" (red), with an option to continue.
- **UI**:
  - Questions wrap to fit the 800x600 window.
  - Selected answers are highlighted in blue.
  - Score and level displayed in real-time.
  - Intro, feedback, and game over screens guide the player.
- **Game Flow**: Start at intro, answer questions, receive feedback, and end with a game over screen showing final results.

## Tips

- **Read Carefully**: Some questions are tricky—pay attention to details to avoid mistakes.
- **Stay Calm**: There’s no time limit, so take your time to think through each answer.
- **Learn from Feedback**: Use the feedback screen to understand correct answers and improve.
- **Aim High**: Try to answer all 80+ questions to reach the Trivia Genius level (46+ points).
- **Replay**: Press Spacebar at game over to try again and improve your score.

Enjoy the trivia challenge! 🧠