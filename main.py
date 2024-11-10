import pygame
import sys
import os
from screens.main_menu import main_menu_screen, load_and_resize_gif
from screens.game_screen import game_screen
from screens.game_screen import level_configs
from screens.level_selection import level_selection

from screens.shop import shop_screen

# Pygame initialization
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cleanify")
font = pygame.font.Font(None, 36)
game_state = "main_menu"  # Possible states: login_menu, main_menu, level_selection, game_screen, shop
user_data = None
level = None  # Initialize level to None
level_data = None  # Initialize level_data to None
currency = 0  # Initialize currency (collected trash) for the player

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
pygame.mixer.music.play(-1)  # Play in an infinite loop

# Main game loop variables for main menu animation
frame_index = 0
clock = pygame.time.Clock()

# Main game loop
while True:
    screen.fill((255, 255, 255))
    
    # Main menu and game state handling
    if game_state == "main_menu":
        # Display animated main menu screen
        frame_index = main_menu_screen(screen, frames, frame_index)
        pygame.display.flip()
        clock.tick(10)  # Adjust frame rate for GIF animation
    
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
        # Start the game screen with the selected level data
        currency = game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT, level_data, level)
        game_state = "main_menu"  # Return to main menu after level ends

    elif game_state == "shop":
        # Open the shop screen
        currency = shop_screen(screen, font, currency)
        game_state = "main_menu"  # Return to main menu after visiting shop

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":
                game_state = "level_selection"  # Move to level selection screen if clicked
                # if play_button_rect.collidepoint(event.pos):
                #     game_state = "level_selection"  # Move to level selection screen if play is clicked
                # elif shop_button_rect.collidepoint(event.pos):
                #     game_state = "shop"  # Move to shop screen if shop is clicked
    
    pygame.display.flip()
