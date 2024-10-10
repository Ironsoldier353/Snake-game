import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Custom Colors
purple = (128, 0, 128)

food_color = red  

# Screen dimensions
width = 800
height = 600

# Load a background image for the game window
bg_image_path = r'J:\projects\snake-game\891ee9a180d14aa4cb2f71100d7b3a987215d384.jpg'
bg_image = pygame.image.load(bg_image_path)
bg_image = pygame.transform.scale(bg_image, (width, height))

# Create the game window
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock object to control the speed of the game
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 25

# Load default fonts for score and messages
font_style = pygame.font.SysFont("comicsansms", 30)  # Using Comic Sans
score_font = pygame.font.SysFont("comicsansms", 35)  # Using Comic Sans

# Sound effects
eat_sound_path = r'J:\projects\snake-game\pow-90398.mp3'  # Eating sound
game_over_sound_path = r'J:\projects\snake-game\mixkit-retro-arcade-game-over-470.wav'  # Game over sound
eat_sound = pygame.mixer.Sound(eat_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# Function to display the score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)  # Change score color to black
    display.blit(value, [10, 10])

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, purple, [x[0], x[1], snake_block, snake_block], border_radius=8)

# Message display function
def message(msg, color, x_pos, y_pos):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [x_pos, y_pos])

# Main game loop
def gameLoop(snake_speed):
    game_over = False
    game_close = False

    # Initial position of the snake
    x = width / 2
    y = height / 2

    # Variables to control direction
    x_change = 0
    y_change = 0

    # Initial snake properties
    snake_list = []
    length_of_snake = 1

    # Food position
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    sound_played = False  # Flag to control sound playback

    while not game_over:

        # Game Over state
        while game_close:
            display.blit(bg_image, (0, 0))  # Draw the background image
            message("You Lost! Press C-Play Again or Q-Quit", red, width / 6, height / 3)
            your_score(length_of_snake - 1)

            if not sound_played:  # Play sound only once
                pygame.mixer.Sound.play(game_over_sound)
                sound_played = True

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(snake_speed)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        # Boundaries
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        display.blit(bg_image, (0, 0)) 

        # Draw the food
        pygame.draw.rect(display, food_color, [food_x, food_y, snake_block, snake_block], border_radius=5)  

        # Update the snake's body
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collision with itself
        if snake_head in snake_list[:-1]:
            game_close = True

        # Draw the snake and display the score
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        # Check if the snake eats the food using rectangle collision detection
        snake_rect = pygame.Rect(x, y, snake_block, snake_block)  # Snake head rectangle
        food_rect = pygame.Rect(food_x, food_y, snake_block, snake_block)  # Food rectangle

        if snake_rect.colliderect(food_rect):  # Check if the snake head collides with the food
            pygame.mixer.Sound.play(eat_sound)  # Play sound when eating food
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        # Set the speed of the game
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Get difficulty level from the user
def choose_difficulty():
    difficulty = input("Choose difficulty (Easy/Medium/Hard): ").lower()
    
    if difficulty == 'easy':
        return 7  # slow speed for easy level
    elif difficulty == 'medium':
        return 15  # normal speed for medium level
    elif difficulty == 'hard':
        return 25  # fast speed for hard level
    else:
        print("Invalid choice! Defaulting to Medium.")
        return 15  # default medium speed if the input is invalid

# Start the game with user-selected difficulty
snake_speed = choose_difficulty()
gameLoop(snake_speed)
