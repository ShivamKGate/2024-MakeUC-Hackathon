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

    # Display the message directing the player to the achievements page
    achievements_message = font.render("Go to Achievements Page to unlock your achievements or prizes!", True, text_color)
    achievements_message_rect = achievements_message.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(achievements_message, achievements_message_rect)

    # Button setup
    achievements_button_text = font.render("Achievements", True, text_color)
    replay_button_text = font.render("Replay Level", True, text_color)
    main_menu_button_text = font.render("Level Selection", True, text_color)
    exit_button_text = font.render("Exit", True, text_color)
    
    achievements_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200), (200, 40))
    replay_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150), (200, 40))
    main_menu_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100), (200, 40))
    exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50), (200, 40))
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw Achievements Button with hover effect
    if achievements_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, achievements_button_rect)
    else:
        pygame.draw.rect(screen, button_color, achievements_button_rect)
    screen.blit(achievements_button_text, achievements_button_text.get_rect(center=achievements_button_rect.center))

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

    # Handle button click events
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
            elif achievements_button_rect.collidepoint(event.pos):
                return "achievements", frame_index, random_facts, scroll_offset
    
    return None, frame_index, random_facts, scroll_offset
