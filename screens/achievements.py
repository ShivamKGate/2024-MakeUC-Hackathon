import pygame
import sys
from db_manager import get_all_achievements  # Import the function to fetch achievements

# Colors
SOFT_YELLOW = (255, 223, 186)
RED = (255, 0, 0)  # Red for all text
WHITE = (255, 223, 186)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load background image at the start
background_image = pygame.image.load('assets/images/level_selection.png')  # Change this to the path of your new cute background image
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen

# Function to display level-specific facts
def display_level_facts(screen, font, level, facts, screen_width, screen_height):
    # Draw the background image
    screen.blit(background_image, (0, 0))  # Draw the background image at the top-left corner
    
    # Title for Level Facts
    title = font.render(f"Level {level} Facts", True, RED)
    title_rect = title.get_rect(center=(screen_width // 2, 30))
    pygame.draw.rect(screen, WHITE, title_rect, border_radius=10)  # Soft white background with rounded corners
    screen.blit(title, title_rect.topleft)

    # Overlay for facts section with a soft background
    overlay_rect = pygame.Rect(50, 80, screen_width - 100, screen_height - 180)
    overlay_surface = pygame.Surface(overlay_rect.size)
    overlay_surface.set_alpha(200)  # Semi-transparent overlay
    overlay_surface.fill(SOFT_YELLOW)  # Soft yellow background for the overlay
    screen.blit(overlay_surface, overlay_rect.topleft)

    # Display each fact with a smaller font
    fact_font = pygame.font.Font(None, 24)
    y_position = 100
    for fact in facts:
        fact_text = fact_font.render(fact, True, RED)
        fact_text_rect = fact_text.get_rect(topleft=(overlay_rect.left + 20, y_position))

        # Only draw the white rounded background if the fact is not "No facts earned at this level yet."
        if fact != "No facts earned at this level yet.":
            pygame.draw.rect(screen, WHITE, fact_text_rect, border_radius=5)  # White rounded background for each fact
        
        # Display the fact text
        screen.blit(fact_text, fact_text_rect.topleft)
        y_position += 40  # Spacing between facts
        if y_position > overlay_rect.bottom - 40:
            break  # Avoid overflowing the overlay area
    
    # Back button with softer colors and rounded corners
    back_button_rect = pygame.Rect(20, screen_height - 60, 80, 40)
    pygame.draw.rect(screen, SOFT_YELLOW, back_button_rect, border_radius=10)
    back_text = font.render("Back", True, RED)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    screen.blit(back_text, back_text_rect.topleft)

    pygame.display.flip()

    # Event loop for the facts screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    return "back"  # Return "back" action to switch back to achievements screen

# Display achievements screen
def achievements_screen(screen, font, earned_facts, screen_width, screen_height, scroll_offset, user_data):
    # Draw the background image
    screen.blit(background_image, (0, 0))  # Draw the background image at the top-left corner

    # Fetch achievements from the database for the logged-in user
    achievements_data = get_all_achievements(user_data["playerName"])

    # Title with red color
    title = font.render("Achievements", True, RED)
    title_rect = title.get_rect(center=(screen_width // 2, 30))
    pygame.draw.rect(screen, WHITE, title_rect, border_radius=10)  # White rounded background for the title
    screen.blit(title, title_rect.topleft)

    # Home button with a soft look and rounded corners
    home_button_rect = pygame.Rect(20, 20, 80, 40)
    pygame.draw.rect(screen, WHITE, home_button_rect, border_radius=10)  # White background with rounded corners
    home_text = font.render("Menu", True, RED)  # Red text for the "Menu" button
    home_text_rect = home_text.get_rect(center=home_button_rect.center)
    screen.blit(home_text, home_text_rect.topleft)

    # Arrange level buttons in a soft, pastel color scheme with rounded corners
    button_positions = [(100 + (i % 4) * 150, 150 + (i // 4) * 60) for i in range(10)]
    level_buttons = []
    for i, pos in enumerate(button_positions):
        button_rect = pygame.Rect(pos[0], pos[1], 120, 40)
        level_text = font.render(f"Level {i + 1}", True, RED)
        level_text_rect = level_text.get_rect(center=button_rect.center)

        # Draw each level button with a pastel background and rounded edges
        pygame.draw.rect(screen, SOFT_YELLOW, button_rect, border_radius=10)
        screen.blit(level_text, level_text_rect.topleft)
        
        level_buttons.append((button_rect, i + 1))  # Store button rect and level number

    pygame.display.flip()

    # Main event loop for achievements screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if home button is clicked
                if home_button_rect.collidepoint(mouse_pos):
                    return "home"

                # Check level buttons to display level-specific facts
                for button_rect, level in level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        # Fetch the level-specific facts from the user's achievements
                        facts = achievements_data.get(str(level), ["No facts earned at this level yet."])
                        action = display_level_facts(screen, font, level, facts, SCREEN_WIDTH, SCREEN_HEIGHT)
                        if action == "back":
                            return "back"

        pygame.display.flip()

# Main game initialization
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Achievements")
    font = pygame.font.Font(None, 36)

    # Dummy user data for testing
    user_data = {"playerName": "TestUser"}
    earned_facts = {}

    achievements_screen(screen, font, earned_facts, SCREEN_WIDTH, SCREEN_HEIGHT, 0, user_data)

if __name__ == "__main__":
    main()
