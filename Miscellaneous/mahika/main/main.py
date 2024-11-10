import pygame
from PIL import Image, ImageSequence
import os

# Initialize Pygame
pygame.init()

# Load GIF frames using PIL
gif_path = "..\..\\assets\\images\\trash_picking_animation.gif"
gif = Image.open(gif_path)
frames = [pygame.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA") 
          for frame in ImageSequence.Iterator(gif)]
frame_index = 0

# Set up Pygame window size based on GIF frame size
window_width, window_height = frames[0].get_size()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game with Animated Background")

# Define font for the centered text
font = pygame.font.SysFont("Comic Sans MS", 32, bold=True, italic=True)

# Function to draw the text with a transparent background
def draw_text(surface, text, pos):
    text_surface = font.render(text, True, (255, 255, 255))  # White text color
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)

# Main loop to display animated GIF background and text
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw current frame
    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)  # Loop through frames

    # Draw the "Press Here to Start" text in the center of the window
    draw_text(screen, "Press Here to Start", (window_width // 2, window_height // 2))

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # Adjust the frame rate for the GIF

# Quit Pygame
pygame.quit()
