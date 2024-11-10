# get_started.py
import pygame
import os
import sys
from db_manager import create_user, login_user

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DULL_RED = (200, 50, 50)  # Dull version of red for disabled buttons
ORANGE = (255, 165, 0)
GREEN = (144, 238, 144)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Input box class for login/signup
class InputBox:
    def __init__(self, x, y, w, h, placeholder, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = ORANGE
        self.text = ''
        self.txt_surface = None
        self.active = False
        self.placeholder = placeholder
        self.is_password = is_password

    def handle_event(self, event, font):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = GREEN if self.active else ORANGE

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            displayed_text = '*' * len(self.text) if self.is_password else self.text
            self.txt_surface = font.render(displayed_text or self.placeholder, True, BLACK)

    def draw(self, screen, font):
        if not self.txt_surface:
            self.txt_surface = font.render(self.placeholder, True, BLACK)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_filled(self):
        return bool(self.text)

# Function to handle login/signup screen
def get_started_screen(screen):
    # Initialize fonts inside the function
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Load background image
    background_image = pygame.image.load("assets/images/trashpickup.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    current_page = "signup"
    error_message = ""

    # Create input boxes for login and signup
    username_box_signup = InputBox(200, 200, 400, 50, "Username")
    email_box_signup = InputBox(200, 270, 400, 50, "Email Address")
    password_box_signup = InputBox(200, 340, 400, 50, "Password", is_password=True)
    confirm_password_box_signup = InputBox(200, 410, 400, 50, "Confirm Password", is_password=True)

    email_box_login = InputBox(200, 250, 400, 50, "Email Address")
    password_box_login = InputBox(200, 320, 400, 50, "Password", is_password=True)

    # Sliding animation variables
    slide_offset = 0
    slide_target = 0
    slide_speed = 20
    transitioning = False

    while True:
        # Draw background image
        screen.blit(background_image, (0, 0))

        # Handle sliding animation
        if transitioning:
            if slide_offset < slide_target:
                slide_offset = min(slide_offset + slide_speed, slide_target)
            elif slide_offset > slide_target:
                slide_offset = max(slide_offset - slide_speed, slide_target)
            else:
                transitioning = False  # End transition when target reached

        # Draw the appropriate form based on the current page
        if current_page == "login":
            email_box_login.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset
            password_box_login.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset
            email_box_login.draw(screen, font)
            password_box_login.draw(screen, font)

            # Set button color based on field completion
            login_button_color = RED if email_box_login.is_filled() and password_box_login.is_filled() else DULL_RED
            login_button = draw_button(screen, "Login", 325 + slide_offset, 400, 150, 50, login_button_color, WHITE, font)
            toggle_text = small_font.render("Don't have an account? Sign up", True, BLACK)
            toggle_rect = toggle_text.get_rect(center=(400 + slide_offset, 480))
            screen.blit(toggle_text, toggle_rect)

        elif current_page == "signup":
            username_box_signup.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset
            email_box_signup.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset
            password_box_signup.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset
            confirm_password_box_signup.rect.x = SCREEN_WIDTH // 2 - 200 + slide_offset

            username_box_signup.draw(screen, font)
            email_box_signup.draw(screen, font)
            password_box_signup.draw(screen, font)
            confirm_password_box_signup.draw(screen, font)

            # Set button color based on field completion
            signup_button_color = RED if all([username_box_signup.is_filled(), email_box_signup.is_filled(),
                                              password_box_signup.is_filled(), confirm_password_box_signup.is_filled()]) else DULL_RED
            signup_button = draw_button(screen, "Sign Up", 325 + slide_offset, 500, 150, 50, signup_button_color, WHITE, font)
            toggle_text = small_font.render("Already have an account? Log in", True, BLACK)
            toggle_rect = toggle_text.get_rect(center=(400 + slide_offset, 580))
            screen.blit(toggle_text, toggle_rect)

        # Display error message if any
        if error_message:
            error_text = small_font.render(error_message, True, RED)
            screen.blit(error_text, (400 - error_text.get_width() // 2, 550))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input box events
            if current_page == "login" and not transitioning:
                email_box_login.handle_event(event, font)
                password_box_login.handle_event(event, font)
            elif current_page == "signup" and not transitioning:
                username_box_signup.handle_event(event, font)
                email_box_signup.handle_event(event, font)
                password_box_signup.handle_event(event, font)
                confirm_password_box_signup.handle_event(event, font)

            # Handle button click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_page == "login" and login_button.collidepoint(event.pos) and email_box_login.is_filled() and password_box_login.is_filled():
                    user = login_user(email_box_login.text, password_box_login.text)
                    if user:
                        return "main_lobby"  # Move to main lobby on successful login
                    else:
                        error_message = "Invalid email or password!"

                elif current_page == "signup" and signup_button.collidepoint(event.pos) and all([username_box_signup.is_filled(), email_box_signup.is_filled(),
                                                                                                 password_box_signup.is_filled(), confirm_password_box_signup.is_filled()]):
                    if password_box_signup.text != confirm_password_box_signup.text:
                        error_message = "Passwords do not match!"
                    else:
                        try:
                            create_user(email_box_signup.text, password_box_signup.text, username_box_signup.text)
                            error_message = ""
                            current_page = "login"  # Go to login page after successful signup
                            slide_target = 0  # Reset slide animation target
                        except Exception as e:
                            error_message = "Email already exists!"

                if toggle_rect.collidepoint(event.pos):
                    target_offset = SCREEN_WIDTH if current_page == "login" else 0
                    current_page = "signup" if current_page == "login" else "login"

        pygame.display.flip()

# Helper function to draw buttons
def draw_button(screen, text, x, y, width, height, color, text_color, font):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=20)
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)
    return button_rect
