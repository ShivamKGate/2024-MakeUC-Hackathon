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
random_facts = None

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))
    
    # Main menu and game state handling
    if game_state == "main_menu":
        frame_index = main_menu_screen(screen, frames, frame_index)
        pygame.display.flip()
        clock.tick(10)
    
    elif game_state == "login_menu":
        result = get_started_screen(screen)
        if result == "main_lobby":
            game_state = "level_selection"
    
    elif game_state == "level_selection":
        selected_level = level_selection(screen)
        if selected_level == "quit":
            running = False
        elif selected_level is not None:
            level = selected_level
            level_data = level_configs.get(selected_level)
            if level_data:
                game_state = "game_screen"
    
    elif game_state == "game_screen" and level_data is not None:
        currency = game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT, level_data, level)
        game_state = "end_game"
    
    elif game_state == "shop":
        currency = shop_screen(screen, font, currency)
        game_state = "main_menu"
    
    elif game_state == "end_game":
# Unpack four values if end_game_screen returns four values
        action, frame_index, random_facts, scroll_offset = end_game_screen(
    screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT, frames, frame_index, random_facts
)
        if action == "replay":
            game_state = "game_screen"
        elif action == "level_selection":
            game_state = "level_selection"
        elif action == "main_menu":
            game_state = "main_menu"
        elif action == "quit":
            running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":
                game_state = "login_menu"  # Move to login menu on click
                game_state = "level_selection"
            elif game_state == "login_menu":
                if result == "main_lobby":
                    game_state = "level_selection"
            elif game_state == "end_game":
                # Additional event handling can go here if needed in the future
                pass

    pygame.display.flip()
    clock.tick(30)  # Control frame rate

