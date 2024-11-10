import pygame
import sys
import os
from screens.main_menu import main_menu_screen, load_and_resize_gif
from screens.level_selection import level_selection
from screens.game_screen import game_screen, level_configs
from screens.shop import shop_screen
from screens.get_started import get_started_screen
from screens.end_game import end_game_screen

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

# Main game loop variables for main menu animation
frame_index = 0
clock = pygame.time.Clock()

# Main game loop
while True:
    screen.fill((255, 255, 255))
    
    # Main menu and game state handling
    if game_state == "main_menu":
        frame_index = main_menu_screen(screen, frames, frame_index)
        pygame.display.flip()
        clock.tick(10)
    
        
    elif game_state == "login_menu":
        # Call get_started_screen function to show login/signup screen
        result = get_started_screen(screen)
        if result == "main_lobby":
            game_state = "level_selection"  # Set game state to main menu after login success
    
    elif game_state == "level_selection":
        # Level selection screen
        # Call the level selection screen and handle level selection
        selected_level = level_selection(screen)
        if selected_level == "quit":
            running = False  # Quit the game if the quit event was received
        elif selected_level is not None:
            print(f"Starting Level {selected_level}")
        level_data = level_configs.get(selected_level)  # Retrieve configuration for the selected level
        if level_data:  # Ensure level_data is valid
            game_state = "game_screen"  # Move to game screen after selection

    elif game_state == "game_screen" and level_data is not None:
        currency = game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT, level_data, level)
        game_state = "end_game"  # Move to end game screen after level ends

    elif game_state == "shop":
        currency = shop_screen(screen, font, currency)
        game_state = "main_menu"

    elif game_state == "end_game":
        # Display end game screen with GIF animation
        action, frame_index = end_game_screen(screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT, frames, frame_index)
        if action == "replay":
            game_state = "game_screen"  # Restart level
        elif action == "level_selection":
            game_state = "level_selection"  # Go back to level selection
        elif action == "main_menu":
            game_state = "main_menu"  # Go back to main menu

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":
                game_state = "login_menu"  # Move to level selection screen if clicked
                # if play_button_rect.collidepoint(event.pos):
                #     game_state = "level_selection"  # Move to level selection screen if play is clicked
                # elif shop_button_rect.collidepoint(event.pos):
                #     game_state = "shop"  # Move to shop screen if shop is clicked
    
    pygame.display.flip()
