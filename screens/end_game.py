import pygame
import sys

FADED_OCHRE_YELLOW = (245, 222, 179)  # Faded ochre yellow color

def end_game_screen(screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT, frames, frame_index, end_game_stats, scroll_offset=0):
    # Load background image
    font = pygame.font.Font(None, 18)
    background_image = pygame.image.load("assets/images/trashpickup.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((255, 255, 255))  # Set background color
    screen.blit(background_image, (0, 0))

    # Title
    title = font.render("Game Over", True, (255, 0, 0))  # Red color for title
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
    
    # Colors
    text_color = (0, 0, 0)  # Black text color
    button_color = (255, 165, 0)  # Bright orange button color
    hover_color = (255, 140, 0)   # Darker hover color

    # Display end game message
    end_text = font.render(f"Level {level} Completed!", True, text_color)
    currency_text = font.render(f"Total Trash Collected: {currency}", True, text_color)
    
    # Position end game message texts
    end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    currency_text_rect = currency_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    
    screen.blit(end_text, end_text_rect)
    screen.blit(currency_text, currency_text_rect)

    # Overlay for "Game Over Summary" section
    summary_overlay_rect = pygame.Rect(80, 180, SCREEN_WIDTH - 160, 130)
    summary_overlay = pygame.Surface(summary_overlay_rect.size, pygame.SRCALPHA)
    summary_overlay.fill((*FADED_OCHRE_YELLOW, 180))  # Semi-transparent overlay
    screen.blit(summary_overlay, summary_overlay_rect.topleft)

    # Game Over Summary: Score, Trash Collected, Time Taken
    summary_title = font.render("Game Over Summary", True, (255, 0, 0))  # Gold color
    screen.blit(summary_title, (SCREEN_WIDTH // 2 - summary_title.get_width() // 2, 190))

    # Display detailed stats
    score_text = font.render(f"Score: {end_game_stats['score']}", True, text_color)
    trash_collected_text = font.render(f"Trash Collected: {end_game_stats['trash_collected']}", True, text_color)
    time_taken_text = font.render(f"Time Taken: {end_game_stats['time_taken']} seconds", True, text_color)
    
    # Position detailed stats within overlay
    screen.blit(score_text, (100, 220))
    screen.blit(trash_collected_text, (100, 260))
    screen.blit(time_taken_text, (100, 300))
    
    # Overlay for "Facts Learned" section
    facts_overlay_rect = pygame.Rect(80, 360, SCREEN_WIDTH - 160, 150)
    facts_overlay = pygame.Surface(facts_overlay_rect.size, pygame.SRCALPHA)
    facts_overlay.fill((*FADED_OCHRE_YELLOW, 180))  # Semi-transparent overlay
    screen.blit(facts_overlay, facts_overlay_rect.topleft)

    # Facts Learned Section
    facts_title = font.render("Facts Learned", True, (255, 0, 0))  # Gold color
    screen.blit(facts_title, (SCREEN_WIDTH // 2 - facts_title.get_width() // 2, 370))
    
    # Position the learned facts within overlay
    fact_y_position = 410
    for fact in end_game_stats["level_facts"]:
        fact_text = font.render(fact, True, text_color)
        screen.blit(fact_text, (100, fact_y_position))
        fact_y_position += 40  # Adjust position for each fact

    # Button texts and rects
    achievements_button_text = font.render("Achievements", True, text_color)
    replay_button_text = font.render("Replay Level", True, text_color)
    main_menu_button_text = font.render("Level Selection", True, text_color)

    # Position buttons horizontally
    button_width, button_height = 180, 40
    gap_between_buttons = 20
    start_x = (SCREEN_WIDTH - (3 * button_width + 2 * gap_between_buttons)) // 2
    button_y = SCREEN_HEIGHT - 70

    achievements_button_rect = pygame.Rect((start_x, button_y), (button_width, button_height))
    replay_button_rect = pygame.Rect((start_x + button_width + gap_between_buttons, button_y), (button_width, button_height))
    main_menu_button_rect = pygame.Rect((start_x + 2 * (button_width + gap_between_buttons), button_y), (button_width, button_height))

    # Draw buttons with hover effects
    mouse_pos = pygame.mouse.get_pos()
    
    # Achievements Button
    pygame.draw.rect(screen, hover_color if achievements_button_rect.collidepoint(mouse_pos) else button_color, achievements_button_rect)
    screen.blit(achievements_button_text, achievements_button_text.get_rect(center=achievements_button_rect.center))

    # Replay Button
    pygame.draw.rect(screen, hover_color if replay_button_rect.collidepoint(mouse_pos) else button_color, replay_button_rect)
    screen.blit(replay_button_text, replay_button_text.get_rect(center=replay_button_rect.center))

    # Level Selection Button
    pygame.draw.rect(screen, hover_color if main_menu_button_rect.collidepoint(mouse_pos) else button_color, main_menu_button_rect)
    screen.blit(main_menu_button_text, main_menu_button_text.get_rect(center=main_menu_button_rect.center))

    pygame.display.flip()  # Update the display

    # Handle button click events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if achievements_button_rect.collidepoint(event.pos):
                return "achievements", frame_index, end_game_stats["level_facts"], scroll_offset
            elif replay_button_rect.collidepoint(event.pos):
                return "replay", frame_index, end_game_stats["level_facts"], scroll_offset
            elif main_menu_button_rect.collidepoint(event.pos):
                return "level_selection", frame_index, end_game_stats["level_facts"], scroll_offset

    return None, frame_index, end_game_stats["level_facts"], scroll_offset
