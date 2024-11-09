import pygame
import sys
import os
from screens.main_menu import main_menu_screen, load_and_resize_gif
from screens.game_screen import game_screen, level_selection, level_configs
from screens.shop import shop_screen
from screens.end_game import end_game_screen  # Import the end game screen

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
    
    elif game_state == "level_selection":
        level = level_selection(screen, font)
        level_data = level_configs.get(level)
        if level_data:
            game_state = "game_screen"

    elif game_state == "game_screen" and level_data is not None:
        currency = game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT, level_data, level)
        game_state = "end_game"  # Move to end game screen after level ends

    elif game_state == "shop":
        currency = shop_screen(screen, font, currency)
        game_state = "main_menu"

    elif game_state == "end_game":
        # Display end game screen and handle responses
        action = end_game_screen(screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT)
        if action == "replay":
            game_state = "game_screen"  # Restart level
        elif action == "main_menu":
            game_state = "main_menu"  # Go back to main menu

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":
                game_state = "level_selection"
    
    pygame.display.flip()
