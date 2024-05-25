import pygame
import random
from config import win, WIDTH, HEIGHT, WHITE, BLACK, GREEN
from utils import display_score, game_over_message

def game():
    running = True
    game_over = False

    # Snake properties
    snake_block = 20
    snake_speed = 15
    snake_list = []
    length_of_snake = 1

    # Initial snake position
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0

    # Initial food position
    foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

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

        # Debugging information
        print(f"New head position: ({new_x1}, {new_y1})")
        print(f"Snake list: {snake_list}")

        # Check for collision with boundaries
        if new_x1 >= WIDTH or new_x1 < 0 or new_y1 >= HEIGHT or new_y1 < 0:
            print("Collision with boundary detected")
            game_over = True

        # Check for collision with itself
        if [new_x1, new_y1] in snake_list[:-1]:
            print("Collision with self detected")
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
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
