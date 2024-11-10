import pygame
import sys

# Achievements screen to display all earned facts
def achievements_screen(screen, font, earned_facts, SCREEN_WIDTH, SCREEN_HEIGHT, scroll_offset=0):
    screen.fill((255, 255, 255))  # Set background color to white
    
    title_text = font.render("Achievements - Earned Facts", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Scroll box area for displaying facts
    scroll_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 100, 400, 400)
    pygame.draw.rect(screen, (255, 255, 255), scroll_box_rect)  # White background for scroll area
    pygame.draw.rect(screen, (0, 0, 0), scroll_box_rect, 2)  # Black border for the scroll area

    # Render each earned fact within the scroll box area
    y_offset = scroll_box_rect.top - scroll_offset + 10  # Initial position for the text
    line_height = 24  # Height of each line of text
    text_color = (0, 0, 0)  # Black text color

    for fact in earned_facts:
        fact_text = font.render(fact, True, text_color)
        fact_text_rect = fact_text.get_rect(midtop=(SCREEN_WIDTH // 2, y_offset))
        
        # Only display facts that fit within the scrollable area
        if scroll_box_rect.top <= fact_text_rect.bottom <= scroll_box_rect.bottom:
            screen.blit(fact_text, fact_text_rect)
        
        y_offset += line_height  # Move y_offset for the next line

    # Back button to return to the main menu or previous screen
    back_button_text = font.render("Home", True, (0, 0, 0))
    back_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 60), (100, 40))
    pygame.draw.rect(screen, (200, 200, 200), back_button_rect)  # Light grey background for button
    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2)  # Black border for button
    screen.blit(back_button_text, back_button_text.get_rect(center=back_button_rect.center))
    
    pygame.display.flip()  # Update the display

    # Handle scrolling and button interaction
    max_scroll_offset = max(0, y_offset - scroll_box_rect.bottom)  # Limit the scroll offset
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):
                return "back"  # Return to main menu or previous screen
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                scroll_offset = min(scroll_offset + 20, max_scroll_offset)
            elif event.key == pygame.K_UP:
                scroll_offset = max(scroll_offset - 20, 0)
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset = max(0, min(scroll_offset - event.y * 20, max_scroll_offset))
    
    return None, scroll_offset
