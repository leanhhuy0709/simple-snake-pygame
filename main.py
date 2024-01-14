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
import asyncio

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120


class Static:
    difficulty = 10

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
game_window = pygame.display.set_mode(
    (Static.frame_size_x, Static.frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
Static.snake_pos = [300, 60]
Static.snake_body = [[300, 60]]

Static.food_pos = [random.randrange(1, (Static.frame_size_x//Static.cell_size))
                   * Static.cell_size, random.randrange(1, (Static.frame_size_y//Static.cell_size)) * Static.cell_size]
Static.food_spawn = True


Static.direction = 'RIGHT'
Static.change_to = Static.direction

Static.score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (Static.frame_size_x/2, Static.frame_size_y/4)
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
    score_surface = score_font.render(str(Static.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (70, 30)
    else:
        score_rect.midtop = (Static.frame_size_x//2, 50)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


def autoSnake():
    choices = []
    x = Static.food_pos[0] - Static.snake_body[0][0]
    y = Static.food_pos[1] - Static.snake_body[0][1]

    if x > 0:
        choices.append('RIGHT')
    elif x < 0:
        choices.append('LEFT')
    if y > 0:
        choices.append('DOWN')
    elif y < 0:
        choices.append('UP')

    if Static.direction == 'UP' and 'DOWN' in choices:
        choices.remove('DOWN')
    elif Static.direction == 'DOWN' and 'UP' in choices:
        choices.remove('UP')
    elif Static.direction == 'LEFT' and 'RIGHT' in choices:
        choices.remove('RIGHT')
    elif Static.direction == 'RIGHT' and 'LEFT' in choices:
        choices.remove('LEFT')

    # Safe choice
    if Static.snake_pos[0] - Static.cell_size < 0 or [Static.snake_pos[0] - Static.cell_size, Static.snake_pos[1]] in Static.snake_body:
        if 'LEFT' in choices:
            choices.remove('LEFT')
    if Static.snake_pos[0] + Static.cell_size > Static.frame_size_x or [Static.snake_pos[0] + Static.cell_size, Static.snake_pos[1]] in Static.snake_body:
        if 'RIGHT' in choices:
            choices.remove('RIGHT')
    if Static.snake_pos[1] - Static.cell_size < 0 or [Static.snake_pos[0], Static.snake_pos[1] - Static.cell_size] in Static.snake_body:
        if 'UP' in choices:
            choices.remove('UP')
    if Static.snake_pos[1] + Static.cell_size > Static.frame_size_y or [Static.snake_pos[0], Static.snake_pos[1] + Static.cell_size] in Static.snake_body:
        if 'DOWN' in choices:
            choices.remove('DOWN')

    if len(choices) == 0:
        choices = ['RIGHT', 'LEFT', 'UP', 'DOWN']

        if Static.direction == 'UP' and 'DOWN' in choices:
            choices.remove('DOWN')
        elif Static.direction == 'DOWN' and 'UP' in choices:
            choices.remove('UP')
        elif Static.direction == 'LEFT' and 'RIGHT' in choices:
            choices.remove('RIGHT')
        elif Static.direction == 'RIGHT' and 'LEFT' in choices:
            choices.remove('LEFT')

        # Safe choice
        if Static.snake_pos[0] - Static.cell_size < 0 or [Static.snake_pos[0] - Static.cell_size, Static.snake_pos[1]] in Static.snake_body:
            if 'LEFT' in choices:
                choices.remove('LEFT')
        if Static.snake_pos[0] + Static.cell_size > Static.frame_size_x or [Static.snake_pos[0] + Static.cell_size, Static.snake_pos[1]] in Static.snake_body:
            if 'RIGHT' in choices:
                choices.remove('RIGHT')
        if Static.snake_pos[1] - Static.cell_size < 0 or [Static.snake_pos[0], Static.snake_pos[1] - Static.cell_size] in Static.snake_body:
            if 'UP' in choices:
                choices.remove('UP')
        if Static.snake_pos[1] + Static.cell_size > Static.frame_size_y or [Static.snake_pos[0], Static.snake_pos[1] + Static.cell_size] in Static.snake_body:
            if 'DOWN' in choices:
                choices.remove('DOWN')

        if len(choices) == 0:
            # Lose!!!
            choices = ['RIGHT', 'LEFT', 'UP', 'DOWN']

    return choices[random.randint(0, len(choices) - 1)]


def drawSnakeBody():
    for i in range(len(Static.snake_body)):
        pos = Static.snake_body[i]
        # Snake body
        if i == 0:
            image = Image.getImage(Snake.HEAD_DOWN)
            angle = 0
            if Static.direction == 'UP':
                angle = 180
            elif Static.direction == 'LEFT':
                angle = 270
            elif Static.direction == 'RIGHT':
                angle = 90

            image = pygame.transform.rotate(image, angle)
        elif i == len(Static.snake_body) - 1:
            image = Image.getImage(Snake.TAIL_DOWN)
            oldPos = Static.snake_body[i - 1]

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
            oldPos = Static.snake_body[i - 1]
            nextPos = Static.snake_body[i + 1]

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


Static.isAuto = False


async def main():
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
                    Static.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    Static.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    Static.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    Static.change_to = 'RIGHT'
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    Static.isAuto = not Static.isAuto
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if Static.isAuto:
            Static.change_to = autoSnake()

        # Making sure the snake cannot move in the opposite direction instantaneously
        if Static.change_to == 'UP' and Static.direction != 'DOWN':
            Static.direction = 'UP'
        if Static.change_to == 'DOWN' and Static.direction != 'UP':
            Static.direction = 'DOWN'
        if Static.change_to == 'LEFT' and Static.direction != 'RIGHT':
            Static.direction = 'LEFT'
        if Static.change_to == 'RIGHT' and Static.direction != 'LEFT':
            Static.direction = 'RIGHT'

        # Moving the snake
        if Static.direction == 'UP':
            Static.snake_pos[1] -= Static.cell_size
        if Static.direction == 'DOWN':
            Static.snake_pos[1] += Static.cell_size
        if Static.direction == 'LEFT':
            Static.snake_pos[0] -= Static.cell_size
        if Static.direction == 'RIGHT':
            Static.snake_pos[0] += Static.cell_size

        # Snake body growing mechanism
        Static.snake_body.insert(0, list(Static.snake_pos))
        if Static.snake_pos[0] == Static.food_pos[0] and Static.snake_pos[1] == Static.food_pos[1]:
            Static.score += 1
            Static.food_spawn = False
        else:
            Static.snake_body.pop()

        # Spawning food on the screen
        if not Static.food_spawn:
            Static.food_pos = [random.randrange(
                1, (Static.frame_size_x//Static.cell_size)) * Static.cell_size, random.randrange(1, (Static.frame_size_y//Static.cell_size)) * Static.cell_size]
        Static.food_spawn = True

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
        game_window.blit(image, (Static.food_pos[0], Static.food_pos[1]))

        # Game Over conditions
        # Getting out of bounds
        if Static.snake_pos[0] < 0 or Static.snake_pos[0] > Static.frame_size_x-10:
            game_over()
        if Static.snake_pos[1] < 0 or Static.snake_pos[1] > Static.frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in Static.snake_body[1:]:
            if Static.snake_pos[0] == block[0] and Static.snake_pos[1] == block[1]:
                game_over()

        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(Static.difficulty)
        await asyncio.sleep(0)

asyncio.run(main())
