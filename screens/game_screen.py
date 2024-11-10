import pygame
import random
import time
pygame.mixer.init()

# Load sounds
pickup_file = "./assets/sounds/retro-coin-4-236671.mp3"
pickup_sound = pygame.mixer.Sound(pickup_file)
end_file = "./assets/sounds/level-win-6416.mp3"
end_sound = pygame.mixer.Sound(end_file)

# Define level configurations without player_speed
level_configs = {
    1: {"background": "assets/images/background/city_view.png", "initial_trash": 10, "respawn_threshold": 3, "respawn_amount": 5, "time_limit": 60, "storage_limit": 10},
    2: {"background": "assets/images/background/dark_forest.png", "initial_trash": 15, "respawn_threshold": 5, "respawn_amount": 6, "time_limit": 55, "storage_limit": 12},
    3: {"background": "assets/images/background/day_rooftop (2).png", "initial_trash": 20, "respawn_threshold": 7, "respawn_amount": 7, "time_limit": 50, "storage_limit": 15},
    4: {"background": "assets/images/background/hospital.png", "initial_trash": 25, "respawn_threshold": 9, "respawn_amount": 8, "time_limit": 45, "storage_limit": 18},
    5: {"background": "assets/images/background/market_place (2).png", "initial_trash": 30, "respawn_threshold": 11, "respawn_amount": 9, "time_limit": 40, "storage_limit": 20},
    6: {"background": "assets/images/background/school.png", "initial_trash": 35, "respawn_threshold": 13, "respawn_amount": 10, "time_limit": 35, "storage_limit": 22},
    7: {"background": "assets/images/background/night_view.png", "initial_trash": 40, "respawn_threshold": 15, "respawn_amount": 11, "time_limit": 30, "storage_limit": 25},
    8: {"background": "assets/images/background/living_room.png", "initial_trash": 45, "respawn_threshold": 17, "respawn_amount": 12, "time_limit": 25, "storage_limit": 28},
    9: {"background": "assets/images/background/snow.png", "initial_trash": 50, "respawn_threshold": 19, "respawn_amount": 13, "time_limit": 20, "storage_limit": 30},
    10: {"background": "assets/images/background/dayforest.png", "initial_trash": 55, "respawn_threshold": 21, "respawn_amount": 14, "time_limit": 3, "storage_limit": 32}
}

# Draw the pause button in the top right corner
def draw_pause_button(screen):
    pause_button_rect = pygame.Rect(screen.get_width() - 50, 10, 30, 30)
    pygame.draw.rect(screen, (200, 0, 0), pause_button_rect)  # Red color for pause button
    pause_text = pygame.font.Font(None, 36).render("||", True, (255, 255, 255))  # Pause symbol
    screen.blit(pause_text, (screen.get_width() - 45, 12))
    return pause_button_rect

# Function to display the pause menu with options
def pause_menu(screen, font):
    screen.fill((0, 0, 0, 150))  # Semi-transparent black overlay
    menu_options = ["Resume", "Restart", "Home", "Quit"]
    button_rects = []

    for i, option in enumerate(menu_options):
        button_rect = pygame.Rect(screen.get_width() // 2 - 60, 150 + i * 70, 120, 50)
        pygame.draw.rect(screen, (0, 200, 0), button_rect)  # Green buttons
        text_surf = font.render(option, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=button_rect.center))
        button_rects.append((button_rect, option))

    pygame.display.flip()
    return button_rects

# Game screen function with pause functionality
def game_screen(screen, font, player_image, middle_trash_image, trash_image, screen_width, screen_height, level_data, level):
    # Load background and scale images
    background = pygame.image.load(level_data["background"])
    background = pygame.transform.scale(background, (screen_width, screen_height))
    player_image = pygame.transform.scale(player_image, (75, 75))
    middle_trash_image = pygame.transform.scale(middle_trash_image, (120, 120))
    trash_image = pygame.transform.scale(trash_image, (30, 30))

    # Player and gameplay setup
    player_rect = player_image.get_rect()
    player_rect.topleft = (100, 100)
    middle_trash_rect = middle_trash_image.get_rect(center=(screen_width // 2, screen_height // 2))
    trash_positions = [(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)) for _ in range(level_data["initial_trash"])]
    last_trash_collected_time = time.time()

    TIME_LIMIT = level_data["time_limit"]
    start_time = time.time()
    storage, score, streak, multiplier = 0, 0, 0, 1
    game_over = False
    paused = False

    while not game_over:
        screen.blit(background, (0, 0))
        screen.blit(middle_trash_image, middle_trash_rect)
        screen.blit(player_image, player_rect)
        pause_button_rect = draw_pause_button(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = True

        # Pause menu interaction
        if paused:
            button_rects = pause_menu(screen, font)
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button_rect, option in button_rects:
                            if button_rect.collidepoint(event.pos):
                                if option == "Resume":
                                    paused = False
                                elif option == "Restart":
                                    return "restart"
                                elif option == "Home":
                                    return "home"
                                elif option == "Quit":
                                    pygame.quit()
                                    exit()
                pygame.display.flip()

        # Game logic if not paused
        if not paused:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= 1
            if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
                player_rect.x += 1
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.y -= 1
            if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
                player_rect.y += 1

            # Display timer
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(TIME_LIMIT - elapsed_time, 0)
            timer_text = font.render(f"Time Left: {remaining_time}s", True, (0, 0, 0))
            screen.blit(timer_text, (10, 10))
            if remaining_time == 0:
                game_over = True

            # Display storage, score, multiplier, and level
            storage_text = font.render(f"Storage: {storage}/{level_data['storage_limit']}", True, (0, 0, 0))
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            multiplier_text = font.render(f"Multiplier: x{multiplier}", True, (0, 0, 0))
            level_text = font.render(f"Level: {level}", True, (0, 0, 0))
            screen.blit(storage_text, (10, 50))
            screen.blit(score_text, (10, 90))
            screen.blit(multiplier_text, (10, 130))
            screen.blit(level_text, (10, 170))

            # Trash respawn logic
            if len(trash_positions) < level_data["respawn_threshold"]:
                for _ in range(level_data["respawn_amount"]):
                    new_trash_x = random.randint(50, screen_width - 50)
                    new_trash_y = random.randint(50, screen_height - 50)
                    trash_positions.append((new_trash_x, new_trash_y))
                last_trash_collected_time = time.time()

            # Draw and collect trash items
            for pos in trash_positions[:]:
                trash_rect = pygame.Rect(pos[0], pos[1], 30, 30)
                screen.blit(trash_image, pos)

                if player_rect.colliderect(trash_rect) and storage < level_data["storage_limit"]:
                    pickup_sound.play()
                    trash_positions.remove(pos)
                    storage += 1
                    score += 1 * multiplier
                    streak += 1
                    if time.time() - last_trash_collected_time <= 5:
                        multiplier = streak
                    else:
                        streak, multiplier = 0, 1
                    last_trash_collected_time = time.time()

            # Deposit trash if player reaches the middle bin
            if player_rect.colliderect(middle_trash_rect) and storage > 0:
                storage, streak, multiplier = 0, 0, 1

        pygame.display.flip()

    return "end_game"  # Default return when the game ends
