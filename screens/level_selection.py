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
BLACK = (0, 0, 0)  # Black color for the text

# Font (set to bold)
font = pygame.font.Font(None, 36)  # Default font size
bold_font = pygame.font.Font(None, 36)
bold_font.set_bold(True)  # Make the font bold

# Level positions (coordinates based on the desired layout)
level_positions = [
    (530, 560), (450, 565), (350, 555),  (310, 510), (400, 475),
    (475, 455), (420, 420), (350, 400), (380, 360), (395, 315)
]

# Load background image (replace with your image path)
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
    # Candy body size and position
    candy_width = 35
    candy_height = 30
    candy_rect = pygame.Rect(position[0] - candy_width // 2, position[1] - candy_height // 2, candy_width, candy_height)

    # Draw the candy body as a solid faded ochre yellow color
    pygame.draw.ellipse(screen, FADED_OCHRE_YELLOW, candy_rect)

    # Draw the wrapping (softly curved ends) using red ellipses
    wrapper_width = 10
    wrapper_height = 5
    pygame.draw.ellipse(screen, RED, (position[0] - candy_width // 2 - wrapper_width, position[1] - wrapper_height // 2, wrapper_width, wrapper_height))
    pygame.draw.ellipse(screen, RED, (position[0] + candy_width // 2, position[1] - wrapper_height // 2, wrapper_width, wrapper_height))

    # Render level number text in red and bold, centered on the candy
    text = bold_font.render(str(level_num), True, RED)
    screen.blit(text, text.get_rect(center=position))

    # Return the button rectangle for click detection
    button_rect = pygame.Rect(position[0] - candy_width // 2, position[1] - candy_height // 2, candy_width, candy_height)
    return button_rect

# Draw logout button on the screen
def draw_logout_button(screen):
    logout_text = font.render("Logout", True, FADED_OCHRE_YELLOW)
    logout_button_rect = pygame.Rect(SCREEN_WIDTH - 100, 10, 80, 40)  # Top right position
    pygame.draw.rect(screen, RED, logout_button_rect)  # Red rectangle for the logout button
    screen.blit(logout_text, logout_text.get_rect(center=logout_button_rect.center))
    return logout_button_rect

# Level selection function
def level_selection(screen):
    if background_image is None:
        init_background()  # Initialize the background if not already done

    # Display the background
    screen.blit(background_image, (0, 0))

    # Draw level buttons and store button rects for click detection
    level_buttons = []
    for i, pos in enumerate(level_positions):
        button_rect = draw_candy_button(screen, i + 1, pos)
        level_buttons.append((button_rect, i + 1))  # Store button and level number

    # Draw the logout button
    logout_button_rect = draw_logout_button(screen)

    # Handle events for button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return "quit"  # Signal to quit the main loop if quit event is detected

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if logout button is clicked
            if logout_button_rect.collidepoint(mouse_pos):
                update_current_user()  # Update currentUser.json to reset user data
                return "logout"  # Return logout signal for handling in main

            # Check if any level button is clicked
            for button_rect, level_num in level_buttons:
                if button_rect.collidepoint(mouse_pos):
                    print(f"Level {level_num} selected")  # Placeholder action for level selection
                    return level_num  # Return selected level number for handling in main

    # Refresh the screen
    pygame.display.flip()
    return None  # No action if no button was clicked
