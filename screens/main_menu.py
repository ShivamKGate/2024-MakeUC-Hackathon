# screens/main_menu.py
import pygame
from PIL import Image, ImageSequence
import os
import math

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
    font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)  # Larger font for a candy-like look

    # Dark green color for the main text
    main_color = (0, 0, 0)
    shadow_color = (34, 139, 34)  # Slightly lighter dark green for the shadow

    # Shadow effect
    shadow_offset = 5  # Offset for shadow
    letter_spacing = 40  # Horizontal spacing between letters
    amplitude = 10  # Amplitude of the wave
    frequency = 0.3  # Frequency of the wave

    # Calculate starting position to center the text
    x_offset = pos[0] - (len(text) * letter_spacing) // 2

    # Draw each letter with a wave effect
    for i, char in enumerate(text):
        # Calculate vertical offset for curvy effect using a sine wave
        y_offset = int(amplitude * math.sin(frequency * (frame_index + i * 10)))

        # Draw shadow
        shadow_surface = font.render(char, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(x_offset + i * letter_spacing + shadow_offset, pos[1] + y_offset + shadow_offset))
        surface.blit(shadow_surface, shadow_rect)

        # Draw main text
        letter_surface = font.render(char, True, main_color)
        letter_rect = letter_surface.get_rect(center=(x_offset + i * letter_spacing, pos[1] + y_offset))
        surface.blit(letter_surface, letter_rect)

# Function to display the main menu screen with animated GIF background
def main_menu_screen(screen, frames, frame_index):
    # Draw the current frame on the screen
    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)  # Loop through frames

    # Draw the stylized "Press Here to Start" text with curvy effect
    draw_candy_text(screen, "Press Here to Start", (screen.get_width() // 2, screen.get_height() // 2), frame_index)

    return frame_index
