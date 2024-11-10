import pygame
import sys
import os

# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Login and Signup Page")

# Load and play background music
bgm_path = "sounds/energetic-bgm-242515.mp3"  # Path to your music file
pygame.mixer.music.load(bgm_path)
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load background image
background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)         # Updated button color
ORANGE = (255, 165, 0)    # Updated input box color
GREEN = (144, 238, 144)   # Light Green
PINK = (255, 182, 193)
YELLOW = (255, 223, 0)

# Input box class for login/signup
class InputBox:
    def __init__(self, x, y, w, h, placeholder, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = ORANGE  # Set initial color to orange
        self.text = ''
        self.txt_surface = font.render(placeholder, True, BLACK)
        self.active = False
        self.placeholder = placeholder
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = GREEN if self.active else ORANGE  # Toggle color on activation

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                displayed_text = '*' * len(self.text) if self.is_password else self.text
                self.txt_surface = font.render(displayed_text, True, BLACK) if self.text else font.render(self.placeholder, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

# Create input boxes for login
email_box_login = InputBox(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 60, 400, 50, "Email Address")
password_box_login = InputBox(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 400, 50, "Password", is_password=True)

# Create input boxes for signup
username_box_signup = InputBox(SCREEN_WIDTH + SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 130, 400, 50, "Username")
email_box_signup = InputBox(SCREEN_WIDTH + SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 70, 400, 50, "Email Address")
password_box_signup = InputBox(SCREEN_WIDTH + SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 10, 400, 50, "Password", is_password=True)
confirm_password_box_signup = InputBox(SCREEN_WIDTH + SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, 400, 50, "Confirm Password", is_password=True)

# Variables to store user data
users = {}
current_page = "login"
next_page = ""  # Track which page to show after successful login
error_message = ""  # To store the error message
error_color = RED  # Error message color

# Sliding animation variables
offset = 0
target_offset = 0
slide_speed = 20

# Game loop
running = True
clock = pygame.time.Clock()

def draw_button(text, x, y, width, height, color, text_color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=20)
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)
    return button_rect

def welcome_screen():
    screen.fill(WHITE)
    welcome_text = large_font.render("Welcome!", True, BLACK)
    screen.blit(welcome_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)

while running:
    # Draw background image
    screen.blit(background_image, (0, 0))

    # Handle sliding animation
    if offset < target_offset:
        offset += slide_speed
        if offset > target_offset:
            offset = target_offset
    elif offset > target_offset:
        offset -= slide_speed
        if offset < target_offset:
            offset = target_offset

    # Apply offset for sliding effect
    if current_page == "login":
        email_box_login.rect.x = SCREEN_WIDTH // 2 - 150 - offset
        password_box_login.rect.x = SCREEN_WIDTH // 2 - 150 - offset
        email_box_login.draw(screen)
        password_box_login.draw(screen)

        login_button = draw_button("Login", SCREEN_WIDTH // 2 - 75 - offset, SCREEN_HEIGHT // 2 + 100, 150, 50, RED, WHITE)
        toggle_text = small_font.render("Don't have an account? Sign up", True, BLACK)
        toggle_rect = toggle_text.get_rect(center=(SCREEN_WIDTH // 2 - offset, SCREEN_HEIGHT // 2 + 180))
        screen.blit(toggle_text, toggle_rect)

    if current_page == "signup":
        username_box_signup.rect.x = SCREEN_WIDTH // 2 - 150 + SCREEN_WIDTH - offset
        email_box_signup.rect.x = SCREEN_WIDTH // 2 - 150 + SCREEN_WIDTH - offset
        password_box_signup.rect.x = SCREEN_WIDTH // 2 - 150 + SCREEN_WIDTH - offset
        confirm_password_box_signup.rect.x = SCREEN_WIDTH // 2 - 150 + SCREEN_WIDTH - offset

        username_box_signup.draw(screen)
        email_box_signup.draw(screen)
        password_box_signup.draw(screen)
        confirm_password_box_signup.draw(screen)

        signup_button = draw_button("Sign Up", SCREEN_WIDTH // 2 - 75 + SCREEN_WIDTH - offset, SCREEN_HEIGHT // 2 + 200, 150, 50, RED, WHITE)
        toggle_text = small_font.render("Already have an account? Log in", True, BLACK)
        toggle_rect = toggle_text.get_rect(center=(SCREEN_WIDTH // 2 + SCREEN_WIDTH - offset, SCREEN_HEIGHT // 2 + 270))
        screen.blit(toggle_text, toggle_rect)

    # Render error message
    if error_message:
        error_text = small_font.render(error_message, True, error_color)
        screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT // 2 + 320))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_page == "login":
            email_box_login.handle_event(event)
            password_box_login.handle_event(event)
        elif current_page == "signup":
            username_box_signup.handle_event(event)
            email_box_signup.handle_event(event)
            password_box_signup.handle_event(event)
            confirm_password_box_signup.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == "login" and login_button.collidepoint(event.pos):
                if not email_box_login.text or not password_box_login.text:
                    error_message = "Please enter both email and password!"
                elif email_box_login.text in users and users[email_box_login.text] == password_box_login.text:
                    next_page = "welcome"
                    error_message = ""
                else:
                    error_message = "Invalid email or password!"

            if current_page == "signup" and signup_button.collidepoint(event.pos):
                if not username_box_signup.text or not email_box_signup.text or not password_box_signup.text or not confirm_password_box_signup.text:
                    error_message = "Please fill in all fields!"
                elif password_box_signup.text != confirm_password_box_signup.text:
                    error_message = "Passwords do not match!"
                else:
                    users[email_box_signup.text] = password_box_signup.text
                    next_page = "welcome"
                    error_message = ""

            if toggle_rect.collidepoint(event.pos):
                target_offset = SCREEN_WIDTH if current_page == "login" else 0
                current_page = "signup" if current_page == "login" else "login"

    if next_page == "welcome":
        welcome_screen()
        current_page = "login"

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
