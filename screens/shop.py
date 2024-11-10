import pygame
from db_manager import purchase_item, update_currency
import time

# Colors
FADED_OCHRE_YELLOW = (245, 222, 179)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Shop items - these are the items available for purchase
shop_items = [
    {"name": "2-Environmental Facts", "price": 50, "description": "Unlocks 2 Unknown Environmental Facts."},
    {"name": "5-Environmental Facts", "price": 100, "description": "Unlocks 5 Unknown Environmental Facts."},
    {"name": "10-Environmental Facts", "price": 150, "description": "Unlocks 10 Unknown Environmental Facts."},
    {"name": "8-Environmental Facts", "price": 80, "description": "CHEAPEST! Unlocks 8 Unknown Environmental Facts."},
]

# Function to display purchase confirmation screen
def show_purchase_confirmation(screen, font, item_name):
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(200)  # Semi-transparent overlay
    overlay.fill((0, 0, 0))  # Black overlay

    # Display the purchase message in the center of the screen
    message = f"Purchased: {item_name}"
    message_text = font.render(message, True, FADED_OCHRE_YELLOW)
    screen.blit(overlay, (0, 0))
    screen.blit(message_text, (screen.get_width() // 2 - message_text.get_width() // 2, screen.get_height() // 2 - message_text.get_height() // 2))
    pygame.display.flip()

    # Wait for 2 seconds or until user clicks
    start_time = time.time()
    while time.time() - start_time < 2:  # 2-second display duration
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                pass

# Function to draw shop screen
def shop_screen(screen, font, currency, user_data):
    screen.fill((30, 30, 30))  # Background color
    title = font.render("Shop", True, RED)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))

    # Draw currency
    currency_text = font.render(f"Your Currency: {user_data['currentCurrency']}", True, (0, 128, 0))
    screen.blit(currency_text, (50, 50))

    # Display items
    item_rects = []
    for i, item in enumerate(shop_items):
        y_position = 100 + i * 100

        # Draw item background
        item_rect = pygame.Rect(50, y_position, screen.get_width() - 100, 80)
        pygame.draw.rect(screen, FADED_OCHRE_YELLOW, item_rect)
        
        # Draw item details
        name_text = font.render(item["name"], True, RED)
        screen.blit(name_text, (70, y_position + 10))
        
        price_text = font.render(f"Price: {item['price']}", True, BLACK)
        screen.blit(price_text, (screen.get_width() - 200, y_position + 10))

        description_text = font.render(item["description"], True, BLACK)
        screen.blit(description_text, (70, y_position + 40))

        item_rects.append((item_rect, item))

    # Exit button
    exit_button_rect = pygame.Rect(screen.get_width() - 100, screen.get_height() - 60, 80, 40)
    pygame.draw.rect(screen, RED, exit_button_rect)
    exit_text = font.render("Exit", True, WHITE)
    screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

    achievements_button_rect = pygame.Rect(screen.get_width() // 2 - 60, screen.get_height() - 90, 200, 40)
    pygame.draw.rect(screen, RED, achievements_button_rect)
    achievements_text = font.render("Achievements", True, WHITE)
    screen.blit(achievements_text, achievements_text.get_rect(center=achievements_button_rect.center))
    
    pygame.display.flip()

    # Handle events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if exit button is clicked
                if exit_button_rect.collidepoint(mouse_pos):
                    return currency  # Return updated currency
                
                if achievements_button_rect and achievements_button_rect.collidepoint(mouse_pos):
                    return 101010101  # Return a value to change game state to achievements

                # Check if any item is clicked
                for item_rect, item in item_rects:
                    if item_rect.collidepoint(mouse_pos):
                        if user_data["currentCurrency"] >= item["price"]:  # Check if user has enough currency
                            # Purchase the item
                            purchase_item(user_data["playerName"], item["price"])
                            user_data["currentCurrency"] -= item["price"]
                            # update_currency(user_data["playerName"], -item["price"])  # Update currency in DB
                            show_purchase_confirmation(screen, font, item["name"])  # Show purchase confirmation
                            return -101010101

                            # Update displayed currency after purchase
                            currency_text = font.render(f"Your Currency: {user_data['currentCurrency']}", True, (0, 128, 0))
                            screen.fill((30, 30, 30))  # Clear screen
                            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))
                            screen.blit(currency_text, (100, 50))  # Display updated currency
                            for rect, item in item_rects:
                                pygame.draw.rect(screen, FADED_OCHRE_YELLOW, rect)  # Redraw item backgrounds
                            screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))
                        else:
                            # Not enough currency
                            print("Not enough currency!")
        pygame.display.flip()
