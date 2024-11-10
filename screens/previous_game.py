# screens/previous_game.py

import pygame
import sys

# Colors for the theme
FADED_OCHRE_YELLOW = (245, 222, 179)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def previous_game_screen(screen, font, game_data, screen_width, screen_height, user_data):
    # Background
    screen.fill((30, 30, 30))  # Dark background color

    # Title
    title = font.render("Previous Game Stats", True, RED)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 30))

    # Overlay for summary section
    summary_overlay_rect = pygame.Rect(80, 100, screen_width - 160, 150)
    summary_overlay = pygame.Surface(summary_overlay_rect.size, pygame.SRCALPHA)
    summary_overlay.fill((*FADED_OCHRE_YELLOW, 180))
    screen.blit(summary_overlay, summary_overlay_rect.topleft)

    # Display game summary
    summary_title = font.render("Game Summary", True, WHITE)
    screen.blit(summary_title, (screen_width // 2 - summary_title.get_width() // 2, 110))

    # Game details
    score_text = font.render(f"Score: {game_data['score']}", True, (0, 0, 0))
    trash_text = font.render(f"Trash Collected: {game_data['trash_collected']}", True, (0, 0, 0))
    level_text = font.render(f"Level: {game_data['level']}", True, (0, 0, 0))

    screen.blit(score_text, (100, 150))
    screen.blit(trash_text, (100, 190))
    screen.blit(level_text, (100, 230))

    # Overlay for facts section
    facts_overlay_rect = pygame.Rect(80, 300, screen_width - 160, 150)
    facts_overlay = pygame.Surface(facts_overlay_rect.size, pygame.SRCALPHA)
    facts_overlay.fill((*FADED_OCHRE_YELLOW, 180))
    screen.blit(facts_overlay, facts_overlay_rect.topleft)

    # Display learned facts
    facts_title = font.render("Facts Learned", True, WHITE)
    screen.blit(facts_title, (screen_width // 2 - facts_title.get_width() // 2, 310))
    
    fact_font = pygame.font.Font(None, 18)
    y_position = 350
    for fact in game_data.get("facts_learned", []):
        fact_text = fact_font.render(fact, True, (0, 0, 0))
        screen.blit(fact_text, (100, y_position))
        y_position += 30

    # Back button
    back_button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 60, 100, 40)
    pygame.draw.rect(screen, RED, back_button_rect)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

    pygame.display.flip()

    # Event loop for the previous game screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    return "back"  # Indicate to go back to achievements

