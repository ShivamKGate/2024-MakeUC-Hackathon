import pygame
import sys
import os
import json
from db_manager import fetch_user, update_current_level, get_current_level, get_currency, fetch_user_data # Assuming fetch_user(email) retrieves user from DB
from factsdb_manager import get_random_facts_by_level
from screens.main_menu import main_menu_screen, load_and_resize_gif
from screens.level_selection import level_selection
from screens.game_screen import game_screen, level_configs, check_level_completion, display_level_up_message
from screens.shop import shop_screen
from screens.get_started import get_started_screen
from screens.end_game import end_game_screen
from screens.achievements import achievements_screen  # Import achievements screen
from fact import environmental_facts
import random


# Pygame initialization
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cleanify")
font = pygame.font.Font(None, 36)
game_state = "main_menu"
scroll_offset = 0  # Initialize scroll offset for scrollable screens
earned_facts = random.sample(environmental_facts, 3)  

user_data = None
level = None
level_data = None
currency = 0

# Load images
player_image = pygame.image.load("assets/images/player.png")
middle_trash_image = pygame.image.load("assets/images/middle_trash.png")
trash_image = pygame.image.load("assets/images/trash_item.png")

# Load and resize GIF frames
gif_path = os.path.join("assets", "images", "trash_picking_animation.gif")
frames = load_and_resize_gif(gif_path, SCREEN_WIDTH, SCREEN_HEIGHT)

# Load background music
bgm_path = os.path.join("assets", "sounds", "energetic-bgm-242515.mp3")
pygame.mixer.music.load(bgm_path)
pygame.mixer.music.play(-1)

# Function to load user data from currentUser.json
# main.py

def load_user_data():
    global user_data
    file_path = "currentUser.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            current_user = json.load(file)
            username = current_user.get("playerName")
            if username:
                user_data = fetch_user_data(username)
            else:
                user_data = None
    else:
        user_data = None


# Load user data at the start of the program
load_user_data()

# Main game loop variables for main menu animation
frame_index = 0
clock = pygame.time.Clock()
random_facts = None

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))
    
    # Main menu and game state handling
    if game_state == "main_menu":
        load_user_data()
        frame_index = main_menu_screen(screen, frames, frame_index, user_data)  # Pass user_data to main menu
        pygame.display.flip()
        clock.tick(20)
        load_user_data()
    
    elif game_state == "login_menu":
        load_user_data()
        result = get_started_screen(screen)
        if result == "main_lobby":
            load_user_data()
            game_state = "level_selection"
    
    elif game_state == "level_selection":
        load_user_data()
        selected_action = level_selection(screen, user_data)
        if selected_action == "quit":
            load_user_data()
            running = False
        elif selected_action == "logout":
            load_user_data()
            game_state = "main_menu"
        elif selected_action == "shop":
            load_user_data()
            game_state = "shop"
        elif selected_action == "achievements":
            load_user_data()
            game_state = "achievements"
        elif isinstance(selected_action, int):  # If a level number is returned
            load_user_data()
            level = selected_action
            level_data = level_configs.get(level)
            if level_data:
                game_state = "game_screen"
    
    elif game_state == "game_screen" and level_data is not None:
        load_user_data()
        score, action = game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT, level_data, level, user_data)
        # Check if player leveled up after game completion
        load_user_data()
        if action == "restart":
            load_user_data()
            game_state = "game_screen"
        elif action == "home":
            load_user_data()
            game_state = "level_selection"
        elif action == "end_game":
            if check_level_completion(user_data["playerName"], score):
                display_level_up_message(user_data["playerName"], screen)  # Show level-up message
            load_user_data()
            game_state = "end_game"
    
    elif game_state == "shop":
        load_user_data()
        currency = shop_screen(screen, font, user_data["currentCurrency"], user_data)
        if currency == -101010101:
            load_user_data()
            game_state = "shop"
        elif currency == 101010101:
            load_user_data()
            game_state = "achievements"
        else:
            load_user_data()
            game_state = "level_selection"
    elif game_state == "end_game":
        load_user_data()
        # Unpack four values if end_game_screen returns four values
        action, frame_index, random_facts, scroll_offset = end_game_screen(
            screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT, frames, frame_index, random_facts, scroll_offset
        )
        load_user_data()
        if action == "replay":
            load_user_data()
            game_state = "game_screen"
        elif action == "level_selection":
            load_user_data()
            game_state = "level_selection"
        elif action == "main_menu":
            load_user_data()
            game_state = "main_menu"
        elif action == "quit":
            running = False
        elif action == "achievements":
            load_user_data()
            game_state = "achievements"  # Go to achievements screen

    elif game_state == "achievements":
        load_user_data()
        # Display achievements screen
        result = achievements_screen(screen, font, earned_facts, SCREEN_WIDTH, SCREEN_HEIGHT, scroll_offset)
        if result == "back":
            load_user_data()
            game_state = "level_selection"  # Return to end game screen
    
    # Event handling for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":
                game_state = "login_menu" if user_data is None else "level_selection"  # Check login status
            elif game_state == "login_menu" and result == "main_lobby":
                game_state = "level_selection"
            elif game_state == "end_game":
                # Additional event handling for end game screen if needed
                pass

    pygame.display.flip()
    clock.tick(30)  # Control frame rate

# Quit Pygame after loop
pygame.quit()
sys.exit()
