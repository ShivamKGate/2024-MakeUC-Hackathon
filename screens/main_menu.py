# screens/main_menu.py
import pygame
from PIL import Image, ImageSequence
import os
import math

# Color definitions
FADED_OCHRE_YELLOW = (245, 222, 179)  # Faded ochre yellow for shadow
RED = (255, 0, 0)  # Red for main text
DARK_GREEN = (34, 139, 34)  # Dark green for "Press Here to Start" shadow
BLACK = (0, 0, 0)  # Black for main text in "Press Here to Start"

# Load GIF frames using PIL and resize to fit screen dimensions
def load_and_resize_gif(gif_path, screen_width, screen_height):
    try:
        gif = Image.open(gif_path)
        frames = [
            pygame.image.fromstring(
                frame.convert("RGBA").resize((screen_width, screen_height)).tobytes(),
                (screen_width, screen_height),
                "RGBA"
            )
            for frame in ImageSequence.Iterator(gif)
        ]
        return frames
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return []

# Function to draw curvy, candy-like text with dark green color and wave effect
def draw_candy_text(surface, text, pos, frame_index):
    font = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
    main_color = BLACK
    shadow_color = DARK_GREEN
    shadow_offset = 5
    letter_spacing = 40
    amplitude = 10
    frequency = 0.3

    # Centering the text horizontally
    x_offset = pos[0] - (len(text) * letter_spacing) // 2

    for i, char in enumerate(text):
        # Wave effect on Y-axis for each letter
        y_offset = int(amplitude * math.sin(frequency * (frame_index + i * 10)))

        # Draw shadow
        shadow_surface = font.render(char, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(x_offset + i * letter_spacing + shadow_offset, pos[1] + y_offset + shadow_offset))
        surface.blit(shadow_surface, shadow_rect)

        # Draw main text
        letter_surface = font.render(char, True, main_color)
        letter_rect = letter_surface.get_rect(center=(x_offset + i * letter_spacing, pos[1] + y_offset))
        surface.blit(letter_surface, letter_rect)

# Function to draw the app name "Bubbly" with a shadow
def draw_app_name(surface, text, pos):
    app_name_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)

    # Shadow
    shadow_surface = app_name_font.render(text, True, DARK_GREEN)
    shadow_rect = shadow_surface.get_rect(center=(pos[0] + 5, pos[1] + 5))
    surface.blit(shadow_surface, shadow_rect)

    # Main text
    app_name_surface = app_name_font.render(text, True, BLACK)
    app_name_rect = app_name_surface.get_rect(center=pos)
    surface.blit(app_name_surface, app_name_rect)

def draw_cloud_with_text(screen, text, pos, text_color, cloud_color):
    font = pygame.font.SysFont("Arial", 24)
    
    # Draw cloud shape with circles
    cloud_width, cloud_height = 140, 40
    cloud_rect = pygame.Rect(pos[0] - cloud_width // 2, pos[1] - cloud_height // 2, cloud_width, cloud_height)
    
    # Main cloud body (rectangle with rounded ends created by circles)
    pygame.draw.ellipse(screen, cloud_color, cloud_rect.move(-20, 0))  # Left puff
    pygame.draw.ellipse(screen, cloud_color, cloud_rect.move(20, 0))   # Right puff
    pygame.draw.rect(screen, cloud_color, cloud_rect.inflate(-20, 0))  # Center rectangle

    # Render and position text on top of cloud
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

# Function to display the main menu screen with animated GIF background and clickable text
def main_menu_screen(screen, frames, frame_index, user_data):
    # Draw the current frame on the screen
    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)  # Loop through frames

    # Display login status at the top right
    font = pygame.font.SysFont("Arial", 24)
    if user_data:
        login_status_text = f"Logged In As {user_data['playerName']}"
        login_color = (0, 128, 0)  # Green
    else:
        login_status_text = "Not Logged In"
        login_color = (255, 0, 0)  # Red
    
    cloud_width, cloud_height = 140, 40
    cloud_rect = pygame.Rect(screen.get_width() - 80 - cloud_width // 2, 30 - cloud_height // 2, cloud_width, cloud_height)
    
    # Main cloud body (rectangle with rounded ends created by circles)
    pygame.draw.ellipse(screen, FADED_OCHRE_YELLOW, cloud_rect.move(-20, 0))  # Left puff
    pygame.draw.ellipse(screen, FADED_OCHRE_YELLOW, cloud_rect.move(20, 0))   # Right puff
    pygame.draw.rect(screen, FADED_OCHRE_YELLOW, cloud_rect.inflate(-20, 0))  # Center rectangle

    # Render main text on top of shadow
    login_status_surface = font.render(login_status_text, True, login_color)
    login_status_rect = login_status_surface.get_rect(topright=(screen.get_width() - 10, 13))
    screen.blit(login_status_surface, login_status_rect)

    app_name_pos = (screen.get_width() // 2, screen.get_height() // 2 - 150)
    draw_app_name(screen, "Welcome To Cleanify", app_name_pos)

    # Draw the stylized "Press Here to Start" text with curvy effect
    text_pos = (screen.get_width() // 2, screen.get_height() // 2)
    draw_candy_text(screen, "Press Here to Start", text_pos, frame_index)

    # Check for clicks
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if login_status_rect.collidepoint(event.pos):
                return "level_selection" if user_data else "login_menu"
            elif text_pos[0] - 100 < event.pos[0] < text_pos[0] + 100 and text_pos[1] - 40 < event.pos[1] < text_pos[1] + 40:
                return "start_game"

    return frame_index
