import pygame
import random

# Initialize Pygame
pygame.init()

# Game screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Snake settings
snake_size = 20
snake_speed = 10

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# List of background images
background_images = ["background1.jpg", "background2.jpg"]

# Load the sound effect
eat_sound = pygame.mixer.Sound("split.mp3")

# Function to load and scale the background image
def load_background_image(index):
    background_image = pygame.image.load(background_images[index])
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    return background_image

# Function to display the score on the screen
def show_score(score):
    font = pygame.font.SysFont(None , 25)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

# Function to draw the snake on the screen
def draw_snake(snake_body):
    for body_part in snake_body:
        pygame.draw.rect(screen, white, [body_part[0], body_part[1], snake_size, snake_size])

# Function to display the game over message and options
def game_over_menu(score):
    game_over = True
    while game_over:
        # Load and display the second background image
        background_image = load_background_image(1)
        screen.blit(background_image, (0, 0))

        font = pygame.font.SysFont(None , 50)
        text = font.render("Game Over!", True, red)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

        # Display the score
        score_text = font.render("Score: " + str(score), True, red)
        screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 - score_text.get_height() / 2 + 50))

        # Display play again and quit options in boxes
        play_again_rect = pygame.Rect(screen_width / 2 - 80, screen_height / 2 + 100, 160, 40)
        quit_rect = pygame.Rect(screen_width / 2 - 80, screen_height / 2 + 160, 160, 40)

        pygame.draw.rect(screen, white, play_again_rect)
        pygame.draw.rect(screen, white, quit_rect)

        font = pygame.font.SysFont(None , 30)
        play_again_text = font.render("Play Again", True, black)
        quit_text = font.render("Quit", True, black)

        screen.blit(play_again_text, (screen_width / 2 - play_again_text.get_width() / 2, screen_height / 2 + 105))
        screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, screen_height / 2 + 165))

        pygame.display.update()

        # Check for user input after game over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_again_rect.collidepoint(mouse_pos):
                    game_loop()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    game_over = False
    game_quit = False

    # Snake position and movement
    x = screen_width // 2
    y = screen_height // 2
    x_change = 0
    y_change = 0

    # Initialize snake body and length
    snake_body = []
    snake_length = 1

    # Generate initial food position
    food_x = round(random.randrange(0, screen_width - snake_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - snake_size) / 20.0) * 20.0

    # Load and display the first background image
    background_image = load_background_image(0)
    screen.blit(background_image, (0, 0))

    while not game_quit:
        while game_over:
            game_over_menu(snake_length - 1)

        # Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_size
                    x_change = 0

        # Update snake position
        x += x_change
        y += y_change

        # Check for collision with boundaries
        if x >= screen_width or x < 0 or y >= screen_height or y < 0:
            game_over = True

        # Update the game screen
        screen.blit(background_image, (0, 0))
        apple_image = pygame.image.load("apple.png")
        apple_image = pygame.transform.scale(apple_image, (snake_size, snake_size))
        screen.blit(apple_image, (food_x, food_y))

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        for body_part in snake_body[:-1]:
            if body_part == snake_head:
                game_over = True

        draw_snake(snake_body)
        show_score(snake_length - 1)
        pygame.display.update()

        # Check for collision with food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, screen_width - snake_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, screen_height - snake_size) / 20.0) * 20.0
            snake_length += 1
            eat_sound.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
