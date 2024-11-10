import json
import os
import pygame
import math

# Initialize Pygame and font module
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
FADED_OCHRE_YELLOW = (245, 222, 179)  # Faded ochre yellow for the candy body
RED = (255, 0, 0)  # Red for text and the wrapper
ORANGE = (255, 165, 0)  # Orange for the "Menu" button
BLACK = (0, 0, 0)  # Black color for text
WHITE = (255, 255, 255)  # White for text

# Font (set to bold)
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 48)
bold_font.set_bold(True)

# Level positions (coordinates based on the desired layout)
level_positions = [
    (530, 560), (450, 565), (350, 555), (310, 510), (400, 475),
    (475, 455), (420, 420), (350, 400), (380, 360), (395, 315)
]

# Load background image
background_image_path = "assets/images/level_selection.png"
background_image = None

# Initialize function to set up background image
def init_background():
    global background_image
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to update currentUser.json on logout
def update_current_user():
    file_path = "currentUser.json"
    default_user_data = {"username": "", "email": "", "currentLevel": 0}
    with open(file_path, "w") as file:
        json.dump(default_user_data, file)
    print("User logged out, currentUser.json updated.")

# Function to draw a simple candy button
def draw_candy_button(screen, level_num, position):
    candy_width = 35
    candy_height = 30
    candy_rect = pygame.Rect(position[0] - candy_width // 2, position[1] - candy_height // 2, candy_width, candy_height)
    pygame.draw.ellipse(screen, FADED_OCHRE_YELLOW, candy_rect)
    pygame.draw.ellipse(screen, RED, (position[0] - candy_width // 2 - 10, position[1] - 5, 10, 5))
    pygame.draw.ellipse(screen, RED, (position[0] + candy_width // 2, position[1] - 5, 10, 5))
    text = font.render(str(level_num), True, RED)
    screen.blit(text, text.get_rect(center=position))
    return candy_rect  # Return the rectangle for click detection

# Draw the logout button
def draw_logout_button(screen):
    logout_text = font.render("Logout", True, RED)
    logout_button_rect = pygame.Rect(SCREEN_WIDTH - 100, 10, 100, 40)
    pygame.draw.rect(screen, FADED_OCHRE_YELLOW, logout_button_rect)
    screen.blit(logout_text, logout_text.get_rect(center=logout_button_rect.center))
    return logout_button_rect

# Draw the top-left Menu button
def draw_menu_button(screen):
    menu_text = font.render("Menu", True, RED)
    menu_button_rect = pygame.Rect(10, 10, 80, 40)
    pygame.draw.rect(screen, FADED_OCHRE_YELLOW, menu_button_rect)
    screen.blit(menu_text, menu_text.get_rect(center=menu_button_rect.center))
    return menu_button_rect

# Draw welcome message
def draw_welcome_message(screen, player_name):
    # Render the shadow text in FADED_OCHRE_YELLOW with a slight offset
    shadow_text = bold_font.render(f"Welcome Back, {player_name}!", True, FADED_OCHRE_YELLOW)
    shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 247))  # Slight offset for shadow
    screen.blit(shadow_text, shadow_rect)

    # Render the main text in RED, positioned on top of the shadow
    welcome_text = bold_font.render(f"Welcome Back, {player_name}!", True, RED)
    welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250))
    screen.blit(welcome_text, welcome_rect)

# Display the menu with options
def display_menu(screen):
    menu_options = ["Back", "Shop", "Unlocked Facts", "Quit"]
    button_rects = []
    for i, option in enumerate(menu_options):
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, 150 + i * 70, 200, 50)
        pygame.draw.rect(screen, FADED_OCHRE_YELLOW, button_rect)
        text_surf = font.render(option, True, RED)
        screen.blit(text_surf, text_surf.get_rect(center=button_rect.center))
        button_rects.append((button_rect, option))
    pygame.display.flip()
    return button_rects

# Level selection function
def level_selection(screen, user_data):
    if background_image is None:
        init_background()  # Initialize the background if not already done

    screen.blit(background_image, (0, 0))
    level_buttons = []
    for i, pos in enumerate(level_positions):
        button_rect = draw_candy_button(screen, i + 1, pos)
        level_buttons.append((button_rect, i + 1))

    logout_button_rect = draw_logout_button(screen)
    menu_button_rect = draw_menu_button(screen)
    draw_welcome_message(screen, user_data["playerName"] if user_data else "Player")

    in_menu = False
    while True:
        if in_menu:
            button_rects = display_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button_rect, option in button_rects:
                        if button_rect.collidepoint(mouse_pos):
                            if option == "Back":
                                in_menu = False
                            elif option == "Shop":
                                return "shop"
                            elif option == "Unlocked Facts":
                                return "achievements"
                            elif option == "Quit":
                                pygame.quit()
                                return "quit"
            pygame.display.flip()
            continue  # Skip further handling to stay in menu loop

        # Draw level buttons and other elements when not in menu
        screen.blit(background_image, (0, 0))
        for button_rect, level_num in level_buttons:
            draw_candy_button(screen, level_num, level_positions[level_num - 1])
        draw_logout_button(screen)
        draw_menu_button(screen)
        draw_welcome_message(screen, user_data["playerName"] if user_data else "Player")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if logout_button_rect.collidepoint(mouse_pos):
                    update_current_user()
                    return "logout"
                if menu_button_rect.collidepoint(mouse_pos):
                    in_menu = True
                for button_rect, level_num in level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        return level_num  # Return selected level number for main loop

        pygame.display.flip()
