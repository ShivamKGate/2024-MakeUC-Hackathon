import pygame
import sys
from db_manager import get_all_achievements  # Import the function to fetch achievements

# Colors
FADED_OCHRE_YELLOW = (245, 222, 179)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BACKGROUND = (30, 30, 30)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Function to display level-specific facts
def display_level_facts(screen, font, level, facts, screen_width, screen_height):
    # Background color
    screen.fill(DARK_BACKGROUND)
    
    # Title for Level Facts
    title = font.render(f"Level {level} Facts", True, RED)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 30))

    # Overlay background for facts section
    overlay_rect = pygame.Rect(50, 80, screen_width - 100, screen_height - 180)
    overlay_surface = pygame.Surface(overlay_rect.size)
    overlay_surface.set_alpha(200)  # Semi-transparent overlay
    overlay_surface.fill(FADED_OCHRE_YELLOW)
    screen.blit(overlay_surface, overlay_rect.topleft)

    # Display each fact with a smaller font
    fact_font = pygame.font.Font(None, 24)
    y_position = 100
    for fact in facts:
        fact_text = fact_font.render(fact, True, DARK_BACKGROUND)
        screen.blit(fact_text, (overlay_rect.left + 20, y_position))
        y_position += 40  # Spacing between facts
        if y_position > overlay_rect.bottom - 40:
            break  # Avoid overflowing the overlay area
    
    # Back button
    back_button_rect = pygame.Rect(20, screen_height - 60, 80, 40)
    pygame.draw.rect(screen, RED, back_button_rect)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

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
    screen.fill((30, 30, 30))  # Background color

    # Fetch achievements from the database for the logged-in user
    achievements_data = get_all_achievements(user_data["playerName"])

    # Title
    title = font.render("Achievements", True, RED)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 30))

    # Home button at the top-left corner
    home_button_rect = pygame.Rect(20, 20, 80, 40)
    pygame.draw.rect(screen, RED, home_button_rect)
    home_text = font.render("Home", True, WHITE)
    screen.blit(home_text, home_text.get_rect(center=home_button_rect.center))

    # Arrange level buttons in a 4-4-2 layout
    button_positions = [(100 + (i % 4) * 150, 150 + (i // 4) * 60) for i in range(10)]
    level_buttons = []
    for i, pos in enumerate(button_positions):
        button_rect = pygame.Rect(pos[0], pos[1], 120, 40)
        pygame.draw.rect(screen, FADED_OCHRE_YELLOW, button_rect)
        level_text = font.render(f"Level {i + 1}", True, BLACK)
        screen.blit(level_text, level_text.get_rect(center=button_rect.center))
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
