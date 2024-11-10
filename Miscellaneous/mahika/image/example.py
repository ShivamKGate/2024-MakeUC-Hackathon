from PIL import Image, ImageDraw, ImageSequence, ImageFont
import os

# Load the park scene and character images
park_scene_path = "image/trashpickup.jpg"  # Replace with your path
character_path = "image/human_charac.png"  # Replace with your path

# Open the images
park_scene = Image.open(park_scene_path).convert("RGBA")
character = Image.open(character_path).convert("RGBA")

# Set up GIF frames list
frames = []

# Define scattered jump paths across the entire scene
jump_paths = [
    [(50, 450), (70, 420), (90, 400), (110, 420), (130, 450)],   # Bottom-left area
    [(400, 300), (420, 270), (440, 250), (460, 270), (480, 300)], # Center-right area
    [(600, 500), (620, 470), (640, 450), (660, 470), (680, 500)], # Bottom-right area
    [(200, 200), (220, 170), (240, 150), (260, 170), (280, 200)], # Upper-left area
    [(500, 100), (520, 80), (540, 60), (560, 80), (580, 100)],    # Upper-center area
]

# Loop through each jump path to simulate character jumping to scattered positions
for jump_path in jump_paths:
    for pos in jump_path:
        # Create a new frame based on park scene
        frame = park_scene.copy()
        
        # Dynamic character resizing based on Y-position (higher in image -> smaller character)
        # Adjust size to create perspective (size decreases as character moves higher in the scene)
        resize_factor = max(50, 200 - pos[1] // 5)  # Adjust size dynamically based on position
        character_resized = character.resize((resize_factor, int(resize_factor * 1.33)), Image.Resampling.LANCZOS)
        
        # Paste character onto frame at specified position
        frame.paste(character_resized, pos, character_resized)
        
        # Add frame to list
        frames.append(frame)

# Save as GIF with slight variation in frame duration for natural effect
output_path = "trash_picking_animation.gif"  # Replace with your desired output path
frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)
