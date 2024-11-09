# end_game.py
import pygame
import sys
from screens.game_screen import level_selection

def end_game_screen(screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT):
    screen.fill((255, 255, 255))  # Set background color
    text_color = (0, 0, 0)
    button_color = (200, 200, 200)
    hover_color = (150, 150, 150)
    
    # Display end game message
    end_text = font.render(f"Level {level} Completed!", True, text_color)
    currency_text = font.render(f"Total Trash Collected: {currency}", True, text_color)
    
    # Position texts
    end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
    currency_text_rect = currency_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    
    screen.blit(end_text, end_text_rect)
    screen.blit(currency_text, currency_text_rect)
    
    # Button setup
    replay_button_text = font.render("Replay Level", True, text_color)
    main_menu_button_text = font.render("Level Selection", True, text_color)
    exit_button_text = font.render("Exit", True, text_color)
    
    replay_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20), (200, 40))
    main_menu_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80), (200, 40))
    exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140), (200, 40))
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw Replay Button with hover effect
    if replay_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, replay_button_rect)
    else:
        pygame.draw.rect(screen, button_color, replay_button_rect)
    screen.blit(replay_button_text, replay_button_text.get_rect(center=replay_button_rect.center))
    
    # Draw Level Selection Button with hover effect
    if main_menu_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, main_menu_button_rect)
    else:
        pygame.draw.rect(screen, button_color, main_menu_button_rect)
    screen.blit(main_menu_button_text, main_menu_button_text.get_rect(center=main_menu_button_rect.center))
    
    # Draw Exit Button with hover effect
    if exit_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, exit_button_rect)
    else:
        pygame.draw.rect(screen, button_color, exit_button_rect)
    screen.blit(exit_button_text, exit_button_text.get_rect(center=exit_button_rect.center))
    
    pygame.display.flip()  # Update the display
    
    # Event handling for button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button_rect.collidepoint(event.pos):
                return "replay"
            elif main_menu_button_rect.collidepoint(event.pos):
                return level_selection(screen, font)
            elif exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    
    return None
