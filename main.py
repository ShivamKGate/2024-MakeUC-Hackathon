# main.py
import pygame
import sys
from db_manager import login_user
# from screens.login_screen import login_screen
from screens.main_menu import main_menu_screen
from screens.game_screen import game_screen

# Pygame initialization
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beach Cleanup Adventure")
font = pygame.font.Font(None, 36)
game_state = "main_menu"  # Possible states: login_menu, main_menu, game_screen
user_data = None

# Load images
player_image = pygame.image.load("assets/images/player.png")
middle_trash_image = pygame.image.load("assets/images/middle_trash.png")
trash_image = pygame.image.load("assets/images/trash_item.png")

while True:
    screen.fill((255, 255, 255))
    
    # if game_state == "login_menu":
    #     login_button_rect, signup_button_rect = login_screen(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
        
    if game_state == "main_menu":
        play_button_rect, prev_games_button_rect, achievements_button_rect = main_menu_screen(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
        
    elif game_state == "game_screen":
        game_screen(screen, font, player_image, middle_trash_image, trash_image, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "login_menu" and login_button_rect.collidepoint(event.pos):
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                user_data = login_user(email, password)
                if user_data:
                    game_state = "main_menu"
            elif game_state == "main_menu" and play_button_rect.collidepoint(event.pos):
                game_state = "game_screen"
    
    pygame.display.flip()