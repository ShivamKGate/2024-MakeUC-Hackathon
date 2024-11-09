# screens/login_screen.py
import pygame
from db_manager import create_user, login_user

def draw_button(screen, text, center, color, font, text_color=(255, 255, 255)):
    button_text = font.render(text, True, text_color)
    button_rect = button_text.get_rect(center=center)
    pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    return button_rect

def login_screen(screen, font, screen_width, screen_height):
    screen.fill((255, 255, 255))
    login_button_rect = draw_button(screen, "Login", (screen_width // 2, screen_height // 2 - 50), (0, 128, 255), font)
    signup_button_rect = draw_button(screen, "Sign Up", (screen_width // 2, screen_height // 2 + 50), (0, 128, 255), font)
    return login_button_rect, signup_button_rect