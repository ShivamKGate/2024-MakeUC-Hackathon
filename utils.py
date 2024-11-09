# utils.py
import pygame

def draw_button(screen, text, center, color, font, text_color=(255, 255, 255)):
    button_text = font.render(text, True, text_color)
    button_rect = button_text.get_rect(center=center)
    pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    return button_rect