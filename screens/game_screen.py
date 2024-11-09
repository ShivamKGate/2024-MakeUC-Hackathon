import pygame
import random
import time
pygame.mixer.init()

# Load sounds
pickup_file = "./assets/sounds/retro-coin-4-236671.mp3"
pickup_sound = pygame.mixer.Sound(pickup_file)
end_file = "./assets/sounds/level-win-6416.mp3"
end_sound = pygame.mixer.Sound(end_file)

# Define level configurations
level_configs = {
    1: {"background": "assets/images/background/city_view.png", "player_speed": 3, "initial_trash": 10, "respawn_threshold": 3, "respawn_amount": 5, "time_limit": 60, "storage_limit": 10},
    2: {"background": "assets/images/background/dark_forest.png", "player_speed": 3.2, "initial_trash": 15, "respawn_threshold": 5, "respawn_amount": 6, "time_limit": 55, "storage_limit": 12},
    3: {"background": "assets/images/background/day_rooftop (2).png", "player_speed": 3.3, "initial_trash": 20, "respawn_threshold": 7, "respawn_amount": 7, "time_limit": 50, "storage_limit": 15},
    4: {"background": "assets/images/background/hospital.png", "player_speed": 3.4, "initial_trash": 25, "respawn_threshold": 9, "respawn_amount": 8, "time_limit": 45, "storage_limit": 18},
    5: {"background": "assets/images/background/market_place (2).png", "player_speed": 3.5, "initial_trash": 30, "respawn_threshold": 11, "respawn_amount": 9, "time_limit": 40, "storage_limit": 20},
    6: {"background": "assets/images/background/school.png", "player_speed": 3.6, "initial_trash": 35, "respawn_threshold": 13, "respawn_amount": 10, "time_limit": 35, "storage_limit": 22},
    7: {"background": "assets/images/background/night_view.png", "player_speed": 3.7, "initial_trash": 40, "respawn_threshold": 15, "respawn_amount": 11, "time_limit": 30, "storage_limit": 25},
    8: {"background": "assets/images/background/living_room.png", "player_speed": 3.8, "initial_trash": 45, "respawn_threshold": 17, "respawn_amount": 12, "time_limit": 25, "storage_limit": 28},
    9: {"background": "assets/images/background/snow.png", "player_speed": 3.9, "initial_trash": 50, "respawn_threshold": 19, "respawn_amount": 13, "time_limit": 20, "storage_limit": 30},
    10: {"background": "assets/images/background/dayforest.png", "player_speed": 4, "initial_trash": 55, "respawn_threshold": 21, "respawn_amount": 14, "time_limit": 15, "storage_limit": 32}
}

# Game screen function for each level
def game_screen(screen, font, player_image, middle_trash_image, trash_image, screen_width, screen_height, level_data, level):
    # Load background and scale images according to level data
    background = pygame.image.load(level_data["background"])
    background = pygame.transform.scale(background, (screen_width, screen_height))
    player_image = pygame.transform.scale(player_image, (75, 75))
    middle_trash_image = pygame.transform.scale(middle_trash_image, (120, 120))
    trash_image = pygame.transform.scale(trash_image, (30, 30))

    # Player setup
    player_rect = player_image.get_rect()
    player_rect.topleft = (100, 100)
    player_speed = level_data["player_speed"]

    # Trash setup based on level data
    INITIAL_TRASH_COUNT = level_data["initial_trash"]
    TRASH_RESPAWN_THRESHOLD = level_data["respawn_threshold"]
    TRASH_RESPAWN_AMOUNT = level_data["respawn_amount"]
    trash_positions = [(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)) for _ in range(INITIAL_TRASH_COUNT)]
    last_trash_collected_time = time.time()

    # Middle trash bin setup
    middle_trash_rect = middle_trash_image.get_rect(center=(screen_width // 2, screen_height // 2))

    # Timer and gameplay variables
    TIME_LIMIT = level_data["time_limit"]
    start_time = time.time()
    storage = 0
    storage_limit = level_data["storage_limit"]
    score = 0
    streak = 0
    multiplier = 1
    game_over = False

    # Game loop
    while not game_over:
        # Display background and player
        screen.blit(background, (0, 0))
        screen.blit(middle_trash_image, middle_trash_rect)
        screen.blit(player_image, player_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += player_speed

        # Display timer
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(TIME_LIMIT - elapsed_time, 0)
        timer_text = font.render(f"Time Left: {remaining_time}s", True, (0, 0, 0))
        screen.blit(timer_text, (10, 10))
        if remaining_time == 0:
            game_over = True

        # Display storage, score, multiplier, and level
        storage_text = font.render(f"Storage: {storage}/{storage_limit}", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        multiplier_text = font.render(f"Multiplier: x{multiplier}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))  # Display current level
        screen.blit(storage_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(multiplier_text, (10, 130))
        screen.blit(level_text, (10, 170))  # Position of the level display

        # Trash respawn logic
        if len(trash_positions) < TRASH_RESPAWN_THRESHOLD:
            for _ in range(TRASH_RESPAWN_AMOUNT):
                new_trash_x = random.randint(50, screen_width - 50)
                new_trash_y = random.randint(50, screen_height - 50)
                trash_positions.append((new_trash_x, new_trash_y))
            last_trash_collected_time = time.time()

        # Draw and collect trash items
        for pos in trash_positions[:]:
            trash_rect = pygame.Rect(pos[0], pos[1], 30, 30)
            screen.blit(trash_image, pos)

            if player_rect.colliderect(trash_rect) and storage < storage_limit:
                pickup_sound.play()
                trash_positions.remove(pos)
                storage += 1
                score += 1 * multiplier
                streak += 1

                if storage >= storage_limit:
                    storage = storage_limit

                # Update multiplier based on streak timing
                if time.time() - last_trash_collected_time <= 5:
                    multiplier = streak
                else:
                    streak = 0
                    multiplier = 1
                last_trash_collected_time = time.time()

        # Deposit trash if player reaches the middle bin
        if player_rect.colliderect(middle_trash_rect) and storage > 0:
            storage = 0
            streak = 0
            multiplier = 1

        pygame.display.flip()

# Function for level selection
def level_selection(screen, font):
    screen.fill((255, 255, 255))
    title_text = font.render("Select Level", True, (0, 0, 0))
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

    level_buttons = []
    for i in range(1, 11):
        level_text = font.render(f"Level {i}", True, (0, 0, 0))
        button_rect = pygame.Rect(100, 100 + i * 50, level_text.get_width() + 20, level_text.get_height() + 10)
        level_buttons.append((button_rect, i))
        screen.blit(level_text, (button_rect.x + 10, button_rect.y + 5))

    pygame.display.flip()

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button, level in level_buttons:
                    if button.collidepoint(event.pos):
                        selecting = False
                        return level

# Example usage
# level = level_selection(screen, font)
# game_screen(screen, font, player_image, middle_trash_image, trash_image, screen_width, screen_height, level_configs[level])
