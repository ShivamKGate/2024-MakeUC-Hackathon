import pygame

# Colors
FADED_OCHRE_YELLOW = (245, 222, 179)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Dummy achievements data
achievements_data = [
    "Collected 100 pieces of trash",
    "Completed 5 levels without losing",
    "Unlocked all environmental facts",
]

# Display achievements screen
def achievements_screen(screen, font, earned_facts, screen_width, screen_height, scroll_offset):
    screen.fill((30, 30, 30))  # Background color

    # Title
    title = font.render("Achievements", True, RED)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 30))

    # Display achievements with regular font size
    for i, achievement in enumerate(achievements_data):
        y_position = 100 + i * 70
        achievement_text = font.render(achievement, True, FADED_OCHRE_YELLOW)
        screen.blit(achievement_text, (70, y_position + scroll_offset))

    # Use a smaller font for facts
    fact_font = pygame.font.Font(None, 24)  # Smaller font for facts
    fact_margin = 5  # Margin of 5px between each fact

    # Display earned facts
    y_start = 300 + scroll_offset
    for i, fact in enumerate(earned_facts):
        y_position = y_start + i * (fact_font.get_height() + fact_margin)
        fact_text = fact_font.render(f"Fact: {fact}", True, WHITE)
        screen.blit(fact_text, (70, y_position))

    # Exit button
    exit_button_rect = pygame.Rect(screen_width - 100, screen_height - 60, 80, 40)
    pygame.draw.rect(screen, RED, exit_button_rect)
    exit_text = font.render("Exit", True, WHITE)
    screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

    pygame.display.flip()

    # Handle events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if exit button is clicked
                if exit_button_rect.collidepoint(mouse_pos):
                    return "back"

        pygame.display.flip()
