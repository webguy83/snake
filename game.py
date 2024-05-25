import pygame
import random
from config import win, WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, YELLOW, PINK
from utils import display_score, game_over_message

def spawn_food(snake_list, snake_block):
    while True:
        foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
        if [foodx, foody] not in snake_list:
            return foodx, foody

def spawn_power_up(snake_list, snake_block):
    while True:
        power_up_x = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
        power_up_y = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
        if [power_up_x, power_up_y] not in snake_list:
            return power_up_x, power_up_y

def game():
    running = True
    game_over = False

    # Snake properties
    snake_block = 20
    snake_speed = 15
    default_snake_speed = 15
    snake_list = []
    length_of_snake = 1

    # Power-up properties
    power_up_duration = 5000  # Power-up effect duration in milliseconds
    power_up_last_time = 0  # Timestamp of last power-up effect
    power_up_type = None  # Current active power-up type
    power_up_spawned = False
    power_up_x, power_up_y = 0, 0

    # Initial snake position
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0

    # Initial food position
    foodx, foody = spawn_food(snake_list, snake_block)

    clock = pygame.time.Clock()

    # Add the initial position to the snake list
    snake_list.append([x1, y1])

    while running:
        while game_over:
            win.fill(BLACK)
            game_over_message()
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change = 0
                    y1_change = snake_block

        # Calculate new head position
        new_x1 = x1 + x1_change
        new_y1 = y1 + y1_change

        # Check for collision with boundaries
        if new_x1 >= WIDTH or new_x1 < 0 or new_y1 >= HEIGHT or new_y1 < 0:
            game_over = True

        # Check for collision with itself
        if [new_x1, new_y1] in snake_list[:-1]:
            game_over = True

        if not game_over:
            # Update position
            x1 = new_x1
            y1 = new_y1

            snake_list.append([x1, y1])
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            win.fill(BLACK)
            pygame.draw.rect(win, GREEN, [foodx, foody, snake_block, snake_block])

            # Check if power-up is collected
            if power_up_spawned and x1 == power_up_x and y1 == power_up_y:
                power_up_last_time = pygame.time.get_ticks()
                power_up_spawned = False
                print(f"Power-up collected: {power_up_type}")
                if power_up_type == "speed":
                    snake_speed = default_snake_speed + 5
                elif power_up_type == "slow":
                    snake_speed = max(5, default_snake_speed - 5)
                elif power_up_type == "very_fast":
                    snake_speed = default_snake_speed + 10

            # Reset power-up effects after duration
            if power_up_last_time and pygame.time.get_ticks() - power_up_last_time > power_up_duration:
                print(f"Power-up effect ended: {power_up_type}")
                snake_speed = default_snake_speed
                power_up_last_time = 0
                power_up_type = None

            # Draw power-up
            if power_up_spawned:
                if power_up_type == "slow":
                    pygame.draw.rect(win, RED, [power_up_x, power_up_y, snake_block, snake_block])
                elif power_up_type == "speed":
                    pygame.draw.rect(win, YELLOW, [power_up_x, power_up_y, snake_block, snake_block])
                elif power_up_type == "very_fast":
                    pygame.draw.rect(win, PINK, [power_up_x, power_up_y, snake_block, snake_block])

            for segment in snake_list:
                pygame.draw.rect(win, WHITE, [segment[0], segment[1], snake_block, snake_block])

            # Draw snake head with a smiley face
            pygame.draw.rect(win, WHITE, [x1, y1, snake_block, snake_block])
            pygame.draw.circle(win, BLACK, (x1 + 5, y1 + 5), 2)
            pygame.draw.circle(win, BLACK, (x1 + 15, y1 + 5), 2)
            pygame.draw.arc(win, BLACK, (x1 + 4, y1 + 4, 12, 12), 3.14, 0, 1)

            display_score(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx, foody = spawn_food(snake_list, snake_block)
                length_of_snake += 1

                # Remove any uncollected power-up before spawning a new one
                power_up_spawned = False
                power_up_last_time = 0

                # Spawn power-up randomly when food is eaten
                if random.randint(1, 2) == 1:  # 50% chance to spawn a power-up
                    power_up_type = random.choice(["slow", "speed", "very_fast"])
                    power_up_x, power_up_y = spawn_power_up(snake_list, snake_block)
                    power_up_spawned = True
                    print(f"Power-up spawned: {power_up_type} at ({power_up_x}, {power_up_y})")

        clock.tick(snake_speed)

    pygame.quit()
