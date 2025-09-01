import pygame
import random
pygame.init()

# VARIABLES
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Sebs Snake Game')
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
smlfont = pygame.font.SysFont("arial", 20)
medfont = pygame.font.SysFont("franklingothicmediumcond", 50)
lgefont = pygame.font.SysFont("arial", 70)
appleThickness = 35
block_size = 20
FPS = 15
direction = "up"

# IMAGES
snHead = pygame.image.load('snakeHead.png')
apple = pygame.image.load('apple.png')


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False    

        gameDisplay.fill(black)
        message_to_screen("Welcome to Sebs Snake Game!", white, -200, "medium")
        message_to_screen("The objective of the game is to eat the apples", white, -50, "small")
        message_to_screen("The more apples you eat, the longer you get", white, 0, "small")
        message_to_screen("If you run into yourself, or the edges, you DIE!", red, 50, "small")
        message_to_screen("Press space to continue", green, 150, "large")
        pygame.display.update()
        clock.tick(15)

# PAUSE
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        message_to_screen("Paused", black, -100, size="large")
        message_to_screen("Press C to continue, or Q to Quit", black, -1,)
        pygame.display.update()
        clock.tick(5)



# SCORE
def score(score):
    text = smlfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [20,20])

# APPLE
def randAppleGen ():
    ranAppleX = round(random.randrange(0,display_width-appleThickness))#/20.0)*20.0
    ranAppleY = round(random.randrange(0,display_height-appleThickness))#/20.0)*20.0

    return ranAppleX, ranAppleY


# SNAKE
def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(snHead, 270)
    if direction == "left":
        head = pygame.transform.rotate(snHead, 90)
    if direction == "up":
        head = snHead
    if direction == "down":
        head = pygame.transform.rotate(snHead, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smlfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = lgefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

# MESSAGE
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

# GAME LOOP
def gameLoop():
    global direction
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    ranAppleX, ranAppleY = randAppleGen()    
    snakeList = []
    snakeLength = 1

    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("GAME OVER!", red, -50, size="large")
            message_to_screen("Press spacebar to play again or Q to quit", white, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0 
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y <0:
            gameOver = True       

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)
        gameDisplay.blit(apple, (ranAppleX, ranAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        score(snakeLength-1)
        pygame.display.update()

        if lead_x > ranAppleX and lead_x < ranAppleX + appleThickness or lead_x + block_size > ranAppleX and lead_x + block_size < ranAppleX + appleThickness:
            
            if lead_y > ranAppleY and lead_y < ranAppleY + appleThickness:
                ranAppleX, ranAppleY = randAppleGen()    
                snakeLength += 1
                
            elif lead_y + block_size > ranAppleY and lead_y + block_size < ranAppleY + appleThickness:
                ranAppleX, ranAppleY = randAppleGen()    
                snakeLength += 1

        clock.tick(FPS+(snakeLength*0.5))

    pygame.quit()
    quit()

game_intro()
gameLoop()