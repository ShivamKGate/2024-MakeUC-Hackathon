import pygame
import sys
import random
from fact import environmental_facts

# Function to wrap text based on width
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Add the word to the current line and measure the width
        test_line = ' '.join(current_line + [word])
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line if any words remain
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Select random facts (done only once per end screen display)
def select_random_facts():
    return random.sample(environmental_facts, 10)

def end_game_screen(screen, font, currency, level, SCREEN_WIDTH, SCREEN_HEIGHT, frames, frame_index, random_facts=None, scroll_offset=0):
    # Load background image
    background_image = pygame.image.load("assets/images/trashpickup.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if random_facts is None:
        # Select 10 random facts only once
        random_facts = select_random_facts()

    screen.fill((255, 255, 255))  # Set background color
    screen.blit(background_image, (0, 0))
    
    
    # Cycle through GIF frames
    frame_index = (frame_index + 1) % len(frames)
    
    text_color = (0, 0, 0)  # Black text color
    button_color = (255, 165, 0)  # Bright orange button color
    hover_color = (255, 140, 0)   # Darker orange (yellow-orange) hover color

    # Display end game message
    end_text = font.render(f"Level {level} Completed!", True, text_color)
    currency_text = font.render(f"Total Trash Collected: {currency}", True, text_color)
    
    # Position texts
    end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    currency_text_rect = currency_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    
    screen.blit(end_text, end_text_rect)
    screen.blit(currency_text, currency_text_rect)

    # Scroll box area
    # Define the scroll box rectangle
    scroll_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 150, 400, 250)

    # Create a transparent surface
    scroll_box_surface = pygame.Surface((scroll_box_rect.width, scroll_box_rect.height), pygame.SRCALPHA)

    # Fill the surface with transparency (alpha channel set to 0)
    scroll_box_surface.fill((0, 0, 0, 0))  # The last value '0' indicates full transparency

    # Blit the transparent surface to the main screen at the position of the scroll box
    screen.blit(scroll_box_surface, scroll_box_rect.topleft)

    # Draw the border around the scroll box (black)
    pygame.draw.rect(screen, (0, 0, 0), scroll_box_rect, 2)  # Border around scroll box for clarity


    # Render the facts in the scrollable area
    y_offset = scroll_box_rect.top - scroll_offset + 10  # Starting position within the scroll area with padding
    line_height = 24  # Height of each line of text

    for fact in random_facts:
        wrapped_lines = wrap_text(fact, font, scroll_box_rect.width - 20)  # Wrap each fact to fit within the scroll box
        for line in wrapped_lines:
            fact_text = font.render(line, True, text_color)
            fact_text_rect = fact_text.get_rect(midtop=(SCREEN_WIDTH // 2, y_offset))
            
            # Only blit the fact if it's within the scrollable area
            if scroll_box_rect.top <= fact_text_rect.bottom <= scroll_box_rect.bottom:
                screen.blit(fact_text, fact_text_rect)
            
            y_offset += line_height  # Adjust vertical spacing between lines

    # Button setup
    replay_button_text = font.render("Replay Level", True, text_color)
    main_menu_button_text = font.render("Level Selection", True, text_color)
    exit_button_text = font.render("Exit", True, text_color)
    
    replay_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150), (200, 40))
    main_menu_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100), (200, 40))
    exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50), (200, 40))
    
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

    # Handle scrolling events
    max_scroll_offset = max(0, y_offset - scroll_box_rect.bottom)  # Calculate max scroll limit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button_rect.collidepoint(event.pos):
                return "replay", frame_index, random_facts, scroll_offset
            elif main_menu_button_rect.collidepoint(event.pos):
                return "level_selection", frame_index, random_facts, scroll_offset
            elif exit_button_rect.collidepoint(event.pos):
                return "quit", frame_index, random_facts, scroll_offset
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                scroll_offset = min(scroll_offset + 20, max_scroll_offset)
            elif event.key == pygame.K_UP:
                scroll_offset = max(scroll_offset - 20, 0)
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset = max(0, min(scroll_offset - event.y * 20, max_scroll_offset))
    
    return None, frame_index, random_facts, scroll_offset
