# screens/main_menu.py
import pygame
from utils import draw_button  # Import draw_button from utils

def main_menu_screen(screen, font, screen_width, screen_height):
    screen.fill((255, 255, 255))
    play_button_rect = draw_button(screen, "Play Game", (screen_width // 2, screen_height // 2 - 80), (0, 128, 255), font)
    prev_games_button_rect = draw_button(screen, "Previous Games", (screen_width // 2, screen_height // 2), (0, 128, 255), font)
    achievements_button_rect = draw_button(screen, "Achievements", (screen_width // 2, screen_height // 2 + 80), (0, 128, 255), font)
    return play_button_rect, prev_games_button_rect, achievements_button_rect