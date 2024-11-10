# level_selection.py

import pygame

# Initialize Pygame and font module
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (255, 0, 0)  # Color for the logout button

# Font
font = pygame.font.Font(None, 36)

# Level positions (coordinates based on the desired layout)
level_positions = [
    (600, 550), (500, 550), (400, 550), (460, 550), (200, 550),
    (400, 250), (460, 230), (520, 210), (580, 190), (100, 550)
]

# Load background image (replace with your image path)
background_image_path = "assets/images/level_selection.png"
background_image = None

# Initialize function to set up background image
def init_background():
    global background_image
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw level buttons on the screen
def draw_level_button(screen, level_num, position):
    text = font.render(str(level_num), True, WHITE)
    button_rect = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)
    pygame.draw.circle(screen, BLUE, position, 20)  # Circle as the button
    screen.blit(text, text.get_rect(center=position))
    return button_rect

# Draw logout button on the screen
def draw_logout_button(screen):
    logout_text = font.render("Logout", True, WHITE)
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
        button_rect = draw_level_button(screen, i + 1, pos)
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
                print("Logout button clicked")  # Placeholder for logout action
                return "logout"  # Return logout signal for handling in main

            # Check if any level button is clicked
            for button_rect, level_num in level_buttons:
                if button_rect.collidepoint(mouse_pos):
                    print(f"Level {level_num} selected")  # Placeholder action for level selection
                    return level_num  # Return selected level number for handling in main

    # Refresh the screen
    pygame.display.flip()
    return None  # No action if no button was clicked

# Main function to run the level selection screen
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level Selection")

    running = True
    while running:
        selected_action = level_selection(screen)

        if selected_action == "quit":
            running = False
        elif selected_action == "logout":
            print("Logging out...")  # Placeholder for actual logout logic
            running = False  # Close the screen after logging out
        elif isinstance(selected_action, int):  # If a level number is returned
            print(f"Proceeding to Level {selected_action}")
            # Placeholder for transitioning to the selected level

    pygame.quit()

if __name__ == "__main__":
    main()
