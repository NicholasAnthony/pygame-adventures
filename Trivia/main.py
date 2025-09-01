import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 50, 50)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Trivia Game")
clock = pygame.time.Clock()
FPS = 60

# Fonts
title_font = pygame.font.SysFont("arial", 48, bold=True)
question_font = pygame.font.SysFont("arial", 32)
option_font = pygame.font.SysFont("arial", 28)
score_font = pygame.font.SysFont("arial", 24)
feedback_font = pygame.font.SysFont("arial", 28)

# Game states
INTRO = 0
PLAYING = 1
FEEDBACK = 2
GAME_OVER = 3

def get_trivia_level(score):
    if score <= 5:
        return "Novice"
    elif score <= 10:
        return "Beginner"
    elif score <= 15:
        return "Amateur"
    elif score <= 20:
        return "Enthusiast"
    elif score <= 25:
        return "Intermediate"
    elif score <= 30:
        return "Advanced"
    elif score <= 35:
        return "Expert"
    elif score <= 40:
        return "Master"
    elif score <= 45:
        return "Trivia Guru"
    else:
        return "Trivia Genius"

class TriviaGame:
    def __init__(self):
        self.questions = [
            ("What is the capital of France?", "A) Paris", "B) Berlin", "C) Beijing", "D) Tokyo", "A"),
            ("What is the capital of Germany?", "A) Paris", "B) Berlin", "C) Beijing", "D) Tokyo", "B"),
            ("Who painted the Mona Lisa?", "A) Michelangelo", "B) Leonardo da Vinci", "C) Pablo Picasso", "D) Vincent van Gogh", "B"),
            ("What is the chemical symbol for water?", "A) H2O", "B) CO2", "C) O2", "D) NaCl", "A"),
            ("Which planet is known as the Red Planet?", "A) Mars", "B) Jupiter", "C) Venus", "D) Saturn", "A"),
            ("Who wrote 'To Kill a Mockingbird'?", "A) Harper Lee", "B) J.K. Rowling", "C) Ernest Hemingway", "D) F. Scott Fitzgerald", "A"),
            ("What is the largest mammal in the world?", "A) Elephant", "B) Blue whale", "C) Giraffe", "D) Hippopotamus", "B"),
            ("Which country is known as the Land of the Rising Sun?", "A) China", "B) Japan", "C) India", "D) Australia", "B"),
            ("What is the smallest bone in the human body?", "A) Femur", "B) Tibia", "C) Stapes", "D) Humerus", "C"),
            ("Who discovered penicillin?", "A) Alexander Fleming", "B) Louis Pasteur", "C) Marie Curie", "D) Albert Einstein", "A"),
            ("What is the primary ingredient in guacamole?", "A) Avocado", "B) Tomato", "C) Onion", "D) Garlic", "A"),
            ("Which country is home to the kangaroo?", "A) Australia", "B) Brazil", "C) South Africa", "D) Argentina", "A"),
            ("Who wrote 'Romeo and Juliet'?", "A) William Shakespeare", "B) Charles Dickens", "C) Jane Austen", "D) Mark Twain", "A"),
            ("What is the tallest mountain in the world?", "A) Mount Everest", "B) Mount Kilimanjaro", "C) Mount McKinley", "D) Mount Fuji", "A"),
            ("What is the capital of Australia?", "A) Sydney", "B) Melbourne", "C) Canberra", "D) Brisbane", "C"),
            ("Who invented the telephone?", "A) Alexander Graham Bell", "B) Thomas Edison", "C) Nikola Tesla", "D) Samuel Morse", "A"),
            ("What is the main ingredient in hummus?", "A) Chickpeas", "B) Lentils", "C) Black beans", "D) Kidney beans", "A"),
            ("What is the largest ocean on Earth?", "A) Pacific Ocean", "B) Atlantic Ocean", "C) Indian Ocean", "D) Arctic Ocean", "A"),
            ("What is the chemical symbol for gold?", "A) Au", "B) Ag", "C) Fe", "D) Pb", "A"),
            ("Which city hosted the 2016 Summer Olympics?", "A) Rio de Janeiro", "B) Tokyo", "C) London", "D) Beijing", "A"),
            ("Who painted the ceiling of the Sistine Chapel?", "A) Leonardo da Vinci", "B) Raphael", "C) Michelangelo", "D) Donatello", "C"),
            ("What is the capital of South Africa?", "A) Johannesburg", "B) Cape Town", "C) Pretoria", "D) Durban", "C"),
            ("Who wrote '1984'?", "A) George Orwell", "B) Aldous Huxley", "C) J.D. Salinger", "D) Franz Kafka", "A"),
            ("What is the largest organ in the human body?", "A) Liver", "B) Heart", "C) Skin", "D) Lungs", "C"),
            ("What is the chemical symbol for silver?", "A) Ag", "B) Si", "C) S", "D) Sl", "A"),
            ("Which planet is known as the Morning Star and Evening Star?", "A) Mars", "B) Venus", "C) Mercury", "D) Jupiter", "B"),
            ("Who is known as the Father of Geometry?", "A) Pythagoras", "B) Euclid", "C) Archimedes", "D) Aristotle", "B"),
            ("What is the national sport of Japan?", "A) Sumo wrestling", "B) Judo", "C) Karate", "D) Kendo", "A"),
            ("What is the capital of Brazil?", "A) Rio de Janeiro", "B) Sao Paulo", "C) Brasilia", "D) Salvador", "C"),
            ("Who discovered gravity when an apple fell on his head?", "A) Albert Einstein", "B) Isaac Newton", "C) Galileo Galilei", "D) Johannes Kepler", "B"),
            ("What is the chemical symbol for carbon?", "A) Cb", "B) Cr", "C) Co", "D) C", "D"),
            ("Which country is known as the Land of the Midnight Sun?", "A) Norway", "B) Russia", "C) Sweden", "D) Finland", "A"),
            ("Who wrote 'The Great Gatsby'?", "A) F. Scott Fitzgerald", "B) Ernest Hemingway", "C) Mark Twain", "D) William Faulkner", "A"),
            ("What is the longest river in the world?", "A) Amazon River", "B) Nile River", "C) Yangtze River", "D) Mississippi River", "B"),
            ("What is the capital of Canada?", "A) Toronto", "B) Vancouver", "C) Ottawa", "D) Montreal", "C"),
            ("Who was the first woman to fly solo across the Atlantic Ocean?", "A) Amelia Earhart", "B) Bessie Coleman", "C) Harriet Quimby", "D) Jacqueline Cochran", "A"),
            ("What is the chemical symbol for sodium?", "A) S", "B) Na", "C) N", "D) Sn", "B"),
            ("Which continent is the largest by land area?", "A) Asia", "B) Africa", "C) North America", "D) Europe", "A"),
            ("Who painted 'Starry Night'?", "A) Pablo Picasso", "B) Vincent van Gogh", "C) Claude Monet", "D) Salvador Dali", "B"),
            ("What is the largest desert in the world?", "A) Sahara Desert", "B) Gobi Desert", "C) Antarctic Desert", "D) Arabian Desert", "A"),
            ("What is the capital of Italy?", "A) Rome", "B) Milan", "C) Florence", "D) Venice", "A"),
            ("Who wrote 'The Catcher in the Rye'?", "A) J.D. Salinger", "B) John Steinbeck", "C) F. Scott Fitzgerald", "D) Ernest Hemingway", "A"),
            ("What is the chemical symbol for iron?", "A) Ir", "B) Fe", "C) I", "D) In", "B"),
            ("What is the largest bird in the world?", "A) Ostrich", "B) Bald eagle", "C) Condor", "D) Albatross", "A"),
            ("What is the capital of China?", "A) Shanghai", "B) Beijing", "C) Hong Kong", "D) Guangzhou", "B"),
            ("Who wrote 'The Odyssey'?", "A) Homer", "B) Virgil", "C) Plato", "D) Aristotle", "A"),
            ("What is the chemical symbol for potassium?", "A) K", "B) Po", "C) P", "D) Ka", "A"),
            ("Which planet is known as the Jewel of the Solar System?", "A) Venus", "B) Earth", "C) Saturn", "D) Uranus", "C"),
            ("Who is credited with discovering the theory of relativity?", "A) Isaac Newton", "B) Albert Einstein", "C) Galileo Galilei", "D) Nikola Tesla", "B"),
            ("What is the capital of Spain?", "A) Barcelona", "B) Madrid", "C) Valencia", "D) Seville", "B"),
            ("Who wrote 'Hamlet'?", "A) William Shakespeare", "B) Charles Dickens", "C) Jane Austen", "D) Mark Twain", "A"),
            ("What is the chemical symbol for helium?", "A) He", "B) H", "C) Ha", "D) Hel", "A"),
            ("What is the deepest part of the ocean?", "A) Challenger Deep", "B) Mariana Trench", "C) Puerto Rico Trench", "D) Tonga Trench", "B"),
            ("What is the capital of Russia?", "A) Moscow", "B) Saint Petersburg", "C) Novosibirsk", "D) Yekaterinburg", "A"),
            ("Who wrote 'Pride and Prejudice'?", "A) Jane Austen", "B) Emily Bronte", "C) Charlotte Bronte", "D) Agatha Christie", "A"),
            ("Which one of the following scientists invented the World Wide Web?", "A) Tim Berners-Lee", "B) Stephen Hawking", "C) Alan Turing", "D) James D. Watson", "A"),
            ("What is the equivalent of 100 Celsius in Fahrenheit?", "A) 152", "B) 182", "C) 212", "D) 232", "C"),
            ("What is the main ingredient of gnocchi?", "A) Rice", "B) Potato", "C) Pasta", "D) Chocolate", "B"),
            ("What is the oldest university in the UK?", "A) Cambridge", "B) Manchester", "C) Bath", "D) Oxford", "D"),
            ("Which country is the James Bond Girl Léa Seydoux from?", "A) Luxembourg", "B) France", "C) Belgium", "D) Canada", "B"),
            ("Dom Pérignon is known as the Father of what?", "A) Computing science", "B) Telephone", "C) Champagne", "D) Electricity", "C"),
            ("What shape is the constellation Ursa Major known to have?", "A) A bear", "B) A ladle", "C) A circle", "D) A book", "B"),
            ("In which country is Machu Picchu?", "A) Bolivia", "B) Argentina", "C) Colombia", "D) Peru", "D"),
            ("Besides white, how many colours are on the flag of Jordan?", "A) 2", "B) 3", "C) 4", "D) 5", "B"),
            ("In the sitcom Gavin and Stacey, where is Gavin from?", "A) Sussex", "B) Essex", "C) Wales", "D) Cornwall", "B"),
            ("What is the largest internal organ in the human body?", "A) Lungs", "B) Heart", "C) Kidneys", "D) Liver", "D"),
            ("What is the percentage of the Earth covered by water?", "A) 51%", "B) 61%", "C) 71%", "D) 81%", "C"),
            ("What was the name of Drakes 2023 album?", "A) Take Care", "B) Scorpion", "C) For All the Dogs", "D) Views", "C"),
            ("Which of the following British presenters never presented Strictly Comes Dancing?", "A) Claudia Winkleman", "B) Tess Daly", "C) Andrea Hamilton", "D) Stacey Dooley", "D"),
            ("Which country is the band AC/DC from?", "A) New Zealand", "B) UK", "C) USA", "D) Australia", "D"),
            ("When was the Cuban Missile Crisis?", "A) 1952", "B) 1972", "C) 1982", "D) 1962", "D"),
            ("Which of the following is not a Japanese dish?", "A) Sushi", "B) Ramen", "C) Babi guling", "D) Udon", "C"),
            ("Which sports is Steve Redgrave known for?", "A) Swimming", "B) Rowing", "C) Football", "D) Basketball", "B"),
            ("Which member of the Spice Girls was known as Sporty Spice?", "A) Melanie Chisholm", "B) Emma Bunton", "C) Geri Halliwell", "D) Victoria Adams", "A"),
            ("What is the atomic number of Hydrogen?", "A) 1", "B) 2", "C) 3", "D) 4", "A"),
            ("'Onze' is the French number for?", "A) 3", "B) 8", "C) 9", "D) 11", "D"),
            ("Which month is the aquamarine the birthstone of?", "A) January", "B) March", "C) June", "D) September", "B"),
            ("Which natural landmark is not in Australia?", "A) Moeraki Boulders", "B) The Great Barrier Reef", "C) Uluru", "D) 12 Apostles", "A"),
            ("Which one of the following islands is not in Scotland?", "A) Isle of Skye", "B) Islay", "C) Isle of Mull", "D) Caladesi Island", "D"),
            ("Who was the 40th President of the United States?", "A) Franklin D. Roosevelt", "B) Ronald Reagan", "C) Bill Clinton", "D) George W. Bush", "B"),
            ("How many players are in a cricket team?", "A) 8", "B) 9", "C) 10", "D) 11", "D"),
            ("Which actress played Sally Draper in Mad Men?", "A) January Jones", "B) Christina Hendricks", "C) January Jones", "D) Elisabeth Moss", "A"),
            ("What does NASA stand for?", "A) National Aeronautics and Space Administration", "B) Nautical And Space Association", "C) National Aeronautics and Space Association", "D) New Aeronautics and Spacial Administration", "A"),
            ("What is 'the Marbella' in Jane the Virgin?", "A) A dance", "B) A telenovela", "C) A hotel", "D) A police operation code name", "C"),
            ("Which ballroom dance originated in Germany and Austria?", "A) Salsa", "B) Waltz", "C) Jive", "D) Cha Cha", "B"),
            ("What is the capital of Iraq?", "A) Baghdad", "B) Islamabad", "C) Tehran", "D) Amman", "A"),
            ("Which country won the first Football World Cup in 1930?", "A) Brazil", "B) Portugal", "C) Italy", "D) Uruguay", "D"),
            ("In which country is the baht the currency?", "A) Vietnam", "B) Malaysia", "C) Indonesia", "D) Thailand", "D"),
            ("In which city were the 2000 Summer Olympics held?", "A) London", "B) Paris", "C) Barcelona", "D) Sydney", "D"),
            ("What colour is the 'm' from the McDonalds logo?", "A) Blue", "B) Red", "C) Yellow", "D) Black", "C"),
            ("In which city was Martin Luther King Jr. assassinated?", "A) New York", "B) Austin", "C) Miami", "D) Memphis", "D"),
            ("What is the name of the dog in Tintin?", "A) Snowy", "B) Flakes", "C) Dottie", "D) Luna", "A"),
            ("Who released the song 'Girls Just Want To Have Fun' in the 80s?", "A) Blondie", "B) Cyndi Lauper", "C) A-ha", "D) Bonnie Tyler", "B")
        ]
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.tally = 0
        self.state = INTRO
        self.feedback_message = ""
        self.feedback_color = BLACK
        self.selected_option = None

    def next_question(self):
        if self.current_question < len(self.questions):
            self.current_question += 1
            self.selected_option = None
            self.feedback_message = ""
            self.state = PLAYING
        else:
            self.state = GAME_OVER

    def handle_answer(self, answer):
        if self.current_question >= len(self.questions):
            self.state = GAME_OVER
            return

        question, a, b, c, d, correct = self.questions[self.current_question]
        self.tally += 1
        if answer == correct:
            self.score += 1
            self.feedback_message = "Correct! Nice one!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"No good, the correct answer was {correct}"
            self.feedback_color = RED
        self.state = FEEDBACK

def wrap_text(text, font, max_width):
    """Wrap text to fit within a maximum width."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def main():
    game = TriviaGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game.state == INTRO:
                    if event.key == pygame.K_SPACE:
                        game.state = PLAYING
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif game.state == PLAYING:
                    if event.key == pygame.K_a:
                        game.selected_option = "A"
                    elif event.key == pygame.K_b:
                        game.selected_option = "B"
                    elif event.key == pygame.K_c:
                        game.selected_option = "C"
                    elif event.key == pygame.K_d:
                        game.selected_option = "D"
                    elif event.key == pygame.K_q:
                        game.state = GAME_OVER
                    if game.selected_option:
                        game.handle_answer(game.selected_option)
                elif game.state == FEEDBACK:
                    if event.key == pygame.K_RETURN:
                        game.next_question()
                elif game.state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        game = TriviaGame()  # Reset game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        screen.fill(WHITE)

        # Draw score and level in top-left corner
        score_text = score_font.render(f"Score: {game.score}/{game.tally}", True, BLACK)
        level_text = score_font.render(f"Level: {get_trivia_level(game.score)}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        if game.state == INTRO:
            title = title_font.render("My Trivia Game!", True, BLACK)
            instructions1 = question_font.render("Press SPACE to start, Q to quit", True, BLACK)
            instructions2 = question_font.render("Use A, B, C, D to answer", True, BLACK)
            screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 200))
            screen.blit(instructions1, (WINDOW_WIDTH // 2 - instructions1.get_width() // 2, 300))
            screen.blit(instructions2, (WINDOW_WIDTH // 2 - instructions2.get_width() // 2, 350))

        elif game.state == PLAYING or game.state == FEEDBACK:
            if game.current_question < len(game.questions):
                question, a, b, c, d, correct = game.questions[game.current_question]
                
                # Wrap and render question text
                question_lines = wrap_text(question, question_font, WINDOW_WIDTH - 40)
                for i, line in enumerate(question_lines):
                    q_text = question_font.render(line, True, BLACK)
                    screen.blit(q_text, (WINDOW_WIDTH // 2 - q_text.get_width() // 2, 100 + i * 40))
                
                # Render answer options with highlighting
                options = [a, b, c, d]
                for i, option in enumerate(options):
                    color = BLUE if game.selected_option == option[0] else BLACK
                    opt_text = option_font.render(option, True, color)
                    screen.blit(opt_text, (WINDOW_WIDTH // 2 - opt_text.get_width() // 2, 250 + i * 50))
                
                # Draw feedback
                if game.state == FEEDBACK:
                    feedback_text = feedback_font.render(game.feedback_message, True, game.feedback_color)
                    screen.blit(feedback_text, (WINDOW_WIDTH // 2 - feedback_text.get_width() // 2, 450))
                    continue_text = score_font.render("Press ENTER to continue", True, BLACK)
                    screen.blit(continue_text, (WINDOW_WIDTH // 2 - continue_text.get_width() // 2, 500))

        elif game.state == GAME_OVER:
            game_over_text = title_font.render("Game Over!", True, BLACK)
            final_score = question_font.render(f"Final Score: {game.score}/{game.tally}", True, BLACK)
            final_level = question_font.render(f"Trivia Level: {get_trivia_level(game.score)}", True, BLACK)
            replay_text = question_font.render("Press SPACE to replay, Q to quit", True, BLACK)
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 200))
            screen.blit(final_score, (WINDOW_WIDTH // 2 - final_score.get_width() // 2, 300))
            screen.blit(final_level, (WINDOW_WIDTH // 2 - final_level.get_width() // 2, 350))
            screen.blit(replay_text, (WINDOW_WIDTH // 2 - replay_text.get_width() // 2, 400))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()