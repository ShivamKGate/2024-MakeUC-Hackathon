# screens/game_screen.py
import pygame
import random
import time
pygame.mixer.init()

# Load the MP3 file
pickup_file = "./assets/sounds/retro-coin-4-236671.mp3"  # Use forward slashes or a raw string for the path
pickup_sound = pygame.mixer.Sound(pickup_file) 
end_file = "./assets/sounds/level-win-6416.mp3"
end_sound = pygame.mixer.Sound(end_file)

def game_screen(screen, font, player_image, middle_trash_image, trash_image, screen_width, screen_height):
    # Load assets and setup game screen
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    player_image = pygame.transform.scale(player_image, (75, 75))
    middle_trash_image = pygame.transform.scale(middle_trash_image, (120, 120))
    trash_image = pygame.transform.scale(trash_image, (30, 30))

    # Player setup
    player_rect = player_image.get_rect()
    player_rect.topleft = (100, 100)
    player_speed = 3

    # Trash setup
    INITIAL_TRASH_COUNT = 10
    TRASH_RESPAWN_THRESHOLD = INITIAL_TRASH_COUNT // 3
    TRASH_RESPAWN_AMOUNT = 5
    trash_positions = [(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)) for _ in range(INITIAL_TRASH_COUNT)]
    last_trash_collected_time = time.time()

    # Middle trash bin setup
    middle_trash_rect = middle_trash_image.get_rect(center=(screen_width // 2, screen_height // 2))

    # Timer and gameplay variables
    TIME_LIMIT = 60  # Countdown in seconds
    start_time = time.time()
    storage = 0
    storage_limit = 10
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

        # Display storage and score
        storage_text = font.render(f"Storage: {storage}/{storage_limit}", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        multiplier_text = font.render(f"Multiplier: x{multiplier}", True, (0, 0, 0))
        screen.blit(storage_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(multiplier_text, (10, 130))

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

            if player_rect.colliderect(trash_rect) and int(storage) < int(storage_limit):
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