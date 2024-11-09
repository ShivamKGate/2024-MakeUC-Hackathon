import pygame
import sys
import random
import time
import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Retrieve the password from the environment variable
mongo_password = os.getenv("MONGO_PASSWORD")

# Initialize pygame
pygame.init()

# MongoDB setup
uri = f"mongodb+srv://Nandini:{mongo_password}@2024-makeuc-hackathon.r3ow1.mongodb.net/?retryWrites=true&w=majority&appName=2024-MakeUC-Hackathon"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["2024MakeUCHackathonDB"]
login_data_collection = db["2024MakeUCHackathon"]

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cleanify")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GRAY = (169, 169, 169)
font = pygame.font.Font(None, 36)

# State management
game_state = "login_menu"  # Possible states: login_menu, main_menu, game_screen

# User session data
user_data = None

def draw_button(text, center, color=BLUE):
    button_text = font.render(text, True, WHITE)
    button_rect = button_text.get_rect(center=center)
    pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    return button_rect

# MongoDB operations
def create_user(email, password, player_name):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = {
        "email": email,
        "password": hashed_password,
        "playerName": player_name,
        "currentLevel": 1,
        "highestScore": 0,
        "previousGames": [],
        "Achievements": []
    }
    login_data_collection.insert_one(new_user)

def login_user(email, password):
    global user_data
    user = login_data_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        user_data = user  # Save user data for session
        return True
    return False

# Login screen
def login_screen():
    screen.fill(WHITE)
    login_button_rect = draw_button("Login", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    signup_button_rect = draw_button("Sign Up", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    return login_button_rect, signup_button_rect

# Main menu after login
def main_menu_screen():
    screen.fill(WHITE)
    play_button_rect = draw_button("Play Game", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    prev_games_button_rect = draw_button("Previous Games", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    achievements_button_rect = draw_button("Achievements", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    return play_button_rect, prev_games_button_rect, achievements_button_rect

# Placeholder game screen
def game_screen():
    # Load assets
    background = pygame.image.load("assets/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image = pygame.image.load("assets/player.png")
    player_image = pygame.transform.scale(player_image, (50, 50))
    middle_trash_image = pygame.image.load("assets/middle_trash.png")
    middle_trash_image = pygame.transform.scale(middle_trash_image, (120, 120))
    trash_image = pygame.image.load("assets/trash_item.png")
    trash_image = pygame.transform.scale(trash_image, (30, 30))

    # Player setup
    player_rect = player_image.get_rect()
    player_rect.topleft = (100, 100)
    player_speed = 3

    # Trash setup
    INITIAL_TRASH_COUNT = 10
    TRASH_RESPAWN_THRESHOLD = INITIAL_TRASH_COUNT // 3
    TRASH_RESPAWN_AMOUNT = 5  # Number of trash items to add when threshold is reached
    trash_positions = [(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(INITIAL_TRASH_COUNT)]
    trash_respawn_time = 2  # Timer to track when to add more trash

    # Middle trash bin setup
    middle_trash_rect = middle_trash_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Timer and gameplay variables
    TIME_LIMIT = 60  # Countdown in seconds
    start_time = time.time()  # Start the timer
    storage = 0
    storage_limit = 10
    score = 0
    streak = 0
    multiplier = 1
    game_over = False

    while not game_over:
        screen.blit(background, (0, 0))
        screen.blit(middle_trash_image, middle_trash_rect)  # Display middle trash bin
        screen.blit(player_image, player_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Continuous movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # Display timer
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(TIME_LIMIT - elapsed_time, 0)

        timer_text = font.render(f"Time Left: {remaining_time}s", True, BLACK)
        screen.blit(timer_text, (10, 10))

        if remaining_time == 0:
            game_over = True

        # Display storage and score
        storage_text = font.render(f"Storage: {storage}/{storage_limit}", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        multiplier_text = font.render(f"Multiplier: x{multiplier}", True, BLACK)
        screen.blit(storage_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(multiplier_text, (10, 130))

        # Trash respawn logic
        if len(trash_positions) < TRASH_RESPAWN_THRESHOLD:
            if trash_respawn_time == 2:
                trash_respawn_time = time.time()
            elif time.time() - trash_respawn_time >= 5:
                for _ in range(TRASH_RESPAWN_AMOUNT):
                    new_trash_x = random.randint(50, SCREEN_WIDTH - 50)
                    new_trash_y = random.randint(50, SCREEN_HEIGHT - 50)
                    trash_positions.append((new_trash_x, new_trash_y))
                trash_respawn_time = 2

        # Draw trash items and handle collection
        for pos in trash_positions[:]:
            trash_rect = pygame.Rect(pos[0], pos[1], 30, 30)
            if player_rect.colliderect(trash_rect):
                trash_positions.remove(pos)
                storage += 1
                score += 1 * multiplier
                streak += 1
                if storage >= storage_limit:
                    storage = storage_limit

                # Update multiplier based on streak within 5 seconds
                if time.time() - trash_respawn_time <= 5:
                    multiplier = streak
                else:
                    streak = 0
                    multiplier = 1

            screen.blit(trash_image, pos)

        # Deposit trash if player collides with middle bin
        if player_rect.colliderect(middle_trash_rect) and storage > 0:
            storage = 0
            streak = 0
            multiplier = 1

        pygame.display.flip()

# Main game loop
running = True
login_button_rect = None
signup_button_rect = None
play_button_rect = None
prev_games_button_rect = None
achievements_button_rect = None

while running:
    screen.fill(WHITE)

    if game_state == "login_menu":
        # Display login and signup options
        login_button_rect, signup_button_rect = login_screen()
        
    elif game_state == "main_menu":
        # Display main menu options
        play_button_rect, prev_games_button_rect, achievements_button_rect = main_menu_screen()

    elif game_state == "game_screen":
        # Placeholder for the actual game screen
        game_screen()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "login_menu":
                if login_button_rect.collidepoint(event.pos):
                    email = input("Enter Email: ")
                    password = input("Enter Password: ")
                    if login_user(email, password):
                        print("Login successful!")
                        game_state = "main_menu"
                    else:
                        print("Invalid login credentials.")
                
                elif signup_button_rect.collidepoint(event.pos):
                    email = input("Enter Email: ")
                    password = input("Enter Password: ")
                    player_name = input("Enter Player Name: ")
                    if not login_data_collection.find_one({"email": email}):
                        create_user(email, password, player_name)
                        print("Signup successful! Please login.")
                    else:
                        print("User already exists.")
            
            elif game_state == "main_menu":
                if play_button_rect.collidepoint(event.pos):
                    game_state = "game_screen"
                elif prev_games_button_rect.collidepoint(event.pos):
                    print("Displaying previous games:", user_data.get("previousGames", []))
                elif achievements_button_rect.collidepoint(event.pos):
                    print("Achievements:", user_data.get("Achievements", []))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()