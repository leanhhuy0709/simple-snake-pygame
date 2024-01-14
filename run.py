"""
Snake Eater
Made with PyGame
"""

import pygame
import sys
import time
import random
from image import Image
from constant import Snake
import math

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 40

# Window size
frame_size_x = 720
frame_size_y = 480
cell_size = 20

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(
        f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [300, 60]
snake_body = [[300, 60]]

food_pos = [random.randrange(1, (frame_size_x//cell_size))
            * cell_size, random.randrange(1, (frame_size_y//cell_size)) * cell_size]
food_spawn = True


direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 40)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (70, 30)
    else:
        score_rect.midtop = (frame_size_x//2, 50)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


def autoSnake():
    choices = []
    x = food_pos[0] - snake_body[0][0]
    y = food_pos[1] - snake_body[0][1]

    if x > 0:
        choices.append('RIGHT')
    elif x < 0:
        choices.append('LEFT')
    if y > 0:
        choices.append('DOWN')
    elif y < 0:
        choices.append('UP')

    if direction == 'UP' and 'DOWN' in choices:
        choices.remove('DOWN')
    elif direction == 'DOWN' and 'UP' in choices:
        choices.remove('UP')
    elif direction == 'LEFT' and 'RIGHT' in choices:
        choices.remove('RIGHT')
    elif direction == 'RIGHT' and 'LEFT' in choices:
        choices.remove('LEFT')

    # Safe choice
    if snake_pos[0] - cell_size < 0 or [snake_pos[0] - cell_size, snake_pos[1]] in snake_body:
        if 'LEFT' in choices:
            choices.remove('LEFT')
    if snake_pos[0] + cell_size > frame_size_x or [snake_pos[0] + cell_size, snake_pos[1]] in snake_body:
        if 'RIGHT' in choices:
            choices.remove('RIGHT')
    if snake_pos[1] - cell_size < 0 or [snake_pos[0], snake_pos[1] - cell_size] in snake_body:
        if 'UP' in choices:
            choices.remove('UP')
    if snake_pos[1] + cell_size > frame_size_y or [snake_pos[0], snake_pos[1] + cell_size] in snake_body:
        if 'DOWN' in choices:
            choices.remove('DOWN')

    if len(choices) == 0:
        choices = ['RIGHT', 'LEFT', 'UP', 'DOWN']

        if direction == 'UP' and 'DOWN' in choices:
            choices.remove('DOWN')
        elif direction == 'DOWN' and 'UP' in choices:
            choices.remove('UP')
        elif direction == 'LEFT' and 'RIGHT' in choices:
            choices.remove('RIGHT')
        elif direction == 'RIGHT' and 'LEFT' in choices:
            choices.remove('LEFT')

        # Safe choice
        if snake_pos[0] - cell_size < 0 or [snake_pos[0] - cell_size, snake_pos[1]] in snake_body:
            if 'LEFT' in choices:
                choices.remove('LEFT')
        if snake_pos[0] + cell_size > frame_size_x or [snake_pos[0] + cell_size, snake_pos[1]] in snake_body:
            if 'RIGHT' in choices:
                choices.remove('RIGHT')
        if snake_pos[1] - cell_size < 0 or [snake_pos[0], snake_pos[1] - cell_size] in snake_body:
            if 'UP' in choices:
                choices.remove('UP')
        if snake_pos[1] + cell_size > frame_size_y or [snake_pos[0], snake_pos[1] + cell_size] in snake_body:
            if 'DOWN' in choices:
                choices.remove('DOWN')

        if len(choices) == 0:
            # Lose!!!
            choices = ['RIGHT', 'LEFT', 'UP', 'DOWN']

    return choices[random.randint(0, len(choices) - 1)]


def drawSnakeBody():
    for i in range(len(snake_body)):
        pos = snake_body[i]
        # Snake body
        if i == 0:
            image = Image.getImage(Snake.HEAD_DOWN)
            angle = 0
            if direction == 'UP':
                angle = 180
            elif direction == 'LEFT':
                angle = 270
            elif direction == 'RIGHT':
                angle = 90

            image = pygame.transform.rotate(image, angle)
        elif i == len(snake_body) - 1:
            image = Image.getImage(Snake.TAIL_DOWN)
            oldPos = snake_body[i - 1]

            if oldPos[0] == pos[0]:
                if oldPos[1] < pos[1]:
                    image = Image.getImage(Snake.TAIL_DOWN)
                else:
                    image = Image.getImage(Snake.TAIL_UP)
            else:
                if oldPos[0] < pos[0]:
                    image = Image.getImage(Snake.TAIL_RIGHT)
                else:
                    image = Image.getImage(Snake.TAIL_LEFT)
        else:
            oldPos = snake_body[i - 1]
            nextPos = snake_body[i + 1]

            if oldPos[0] == pos[0] and pos[0] == nextPos[0]:
                image = Image.getImage(Snake.BODY_VERTICAL)
            elif oldPos[1] == pos[1] and pos[1] == nextPos[1]:
                image = Image.getImage(Snake.BODY_VERTICAL)
                image = pygame.transform.rotate(image, 90)
            elif oldPos[0] < pos[0] and pos[1] < nextPos[1] or nextPos[0] < pos[0] and pos[1] < oldPos[1]:
                image = Image.getImage(Snake.BODY_BOTTOM_LEFT)
            elif oldPos[0] < pos[0] and pos[1] > nextPos[1] or nextPos[0] < pos[0] and pos[1] > oldPos[1]:
                image = Image.getImage(Snake.BODY_BOTTOM_LEFT)
                image = pygame.transform.rotate(image, 270)
            elif oldPos[1] < pos[1] and pos[0] < nextPos[0] or nextPos[1] < pos[1] and pos[0] < oldPos[0]:
                image = Image.getImage(Snake.BODY_BOTTOM_LEFT)
                image = pygame.transform.rotate(image, 180)
            elif oldPos[1] > pos[1] and pos[0] < nextPos[0] or nextPos[1] > pos[1] and pos[0] < oldPos[0]:
                image = Image.getImage(Snake.BODY_BOTTOM_LEFT)
                image = pygame.transform.rotate(image, 90)
            else:
                image = Image.getImage(Snake.BODY_VERTICAL)
        game_window.blit(image, (pos[0], pos[1]))


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    change_to = autoSnake()

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= cell_size
    if direction == 'DOWN':
        snake_pos[1] += cell_size
    if direction == 'LEFT':
        snake_pos[0] -= cell_size
    if direction == 'RIGHT':
        snake_pos[0] += cell_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(
            1, (frame_size_x//cell_size)) * cell_size, random.randrange(1, (frame_size_y//cell_size)) * cell_size]
    food_spawn = True

    # GFX
    # game_window.fill(black)
    background = Image.getImage('./assets/background.png')
    game_window.blit(background, (0, 0))

    show_score(1, black, 'consolas', 25)

    drawSnakeBody()

    # Snake food
    # pygame.draw.rect(game_window, red, pygame.Rect(
    #     food_pos[0], food_pos[1], cell_size, cell_size))

    image = Image.getImage('./assets/apple.png')
    game_window.blit(image, (food_pos[0], food_pos[1]))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
