import pygame

# Define environmental facts and their costs
facts = [
    {"fact": "Recycling one aluminum can saves enough energy to run a TV for three hours.", "cost": 10},
    {"fact": "Plastic takes up to 1,000 years to decompose in a landfill.", "cost": 20},
    {"fact": "One reusable bag can replace hundreds of plastic bags.", "cost": 15},
    {"fact": "Recycling one ton of paper saves 17 trees.", "cost": 25},
    {"fact": "The ocean absorbs about 30% of the CO2 produced by humans.", "cost": 30}
]

def shop_screen(screen, font, currency):
    running = True
    purchased_facts = []
    
    while running:
        screen.fill((255, 255, 255))
        title_text = font.render("Environmental Facts Shop", True, (0, 0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))
        
        # Display currency
        currency_text = font.render(f"Trash Collected: {currency}", True, (0, 128, 0))
        screen.blit(currency_text, (10, 50))
        
        # Display facts with buy buttons
        fact_y = 100
        fact_buttons = []
        for i, item in enumerate(facts):
            fact_text = font.render(f"{item['fact']} - Cost: {item['cost']}", True, (0, 0, 0))
            screen.blit(fact_text, (20, fact_y))
            
            # Create buy button for each fact
            buy_button = pygame.Rect(700, fact_y, 60, 30)
            pygame.draw.rect(screen, (0, 128, 0), buy_button)
            buy_text = font.render("Buy", True, (255, 255, 255))
            screen.blit(buy_text, (buy_button.x + 10, buy_button.y + 5))
            
            fact_buttons.append((buy_button, item))  # Store button and item info
            fact_y += 50

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button, item in fact_buttons:
                    if button.collidepoint(event.pos):
                        # Check if player has enough currency
                        if currency >= item["cost"]:
                            currency -= item["cost"]
                            purchased_facts.append(item["fact"])
                            print(f"Purchased: {item['fact']}")  # Debugging message for purchased fact
                        else:
                            print("Not enough currency to buy this fact!")  # Debugging message

        # Display purchased facts
        purchased_text_y = fact_y + 50
        purchased_title = font.render("Purchased Facts", True, (0, 0, 128))
        screen.blit(purchased_title, (10, purchased_text_y))
        purchased_text_y += 40
        for fact in purchased_facts:
            purchased_fact_text = font.render(fact, True, (0, 0, 0))
            screen.blit(purchased_fact_text, (20, purchased_text_y))
            purchased_text_y += 30

        pygame.display.flip()

    return currency  # Return updated currency after purchases
