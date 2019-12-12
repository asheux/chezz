"""
Disclaimer: This code really needs refactoring
            and it's incomplete; TIME 
"""
import pygame
import sys
import random

width = 800
height = 600

# I need the directions to compute the next vector as the bot move
# or human as we named them
directions = {'N': (0, 3), 'S': (0, -3), 'E': (10, 0), 'W': (-10, 0)}

# initialize an empty array pretty huge, im sure there is a better way
WORLD = [None] * (height * width)


def transform_img(image, coords):
    """
    Most of the images are large, had trouble finding tiny pics
    apparently pygame can compress them for me, awesome
    Parameters
    ----------
    image, coords; pygame.Surface, tuple
        image is the image to compress as you may have guessed
        coords is the coordinates or rather the size you want
        to compress your image in
    """
    return pygame.transform.scale(image, coords)


def walls(d, matrix):
    """
    Inserts the required bricks to create the walls
    Parameters
    ----------
    d, matrix; pygame.Display, a two-dimentionals array
        d is the display surface for pygame
        matrix is the two-d array containing the bricks
    """
    for x in range(len(matrix)):
        row = matrix[x]
        i = x + 1
        x = round(width * (0.1 * i), 1)
        for y in range(len(row)):
            img = row[y]
            j = y + 3.6
            y = round(height * (0.12 * j), 1)
            if img:
                set_position((int(x), int(y)), img)


def create_walls(world, display):
    """
    This create the walls you see when you first log into the game
    Parameters
    ----------
    world, display; list, pygame.Display
        world is an array
        display is the pygame surface
    """
    for i, item in enumerate(world):
        if item:
            c = i // height, i % height
            display.blit(item, c)


def set_position(coords, value):
    """
    Sets anew object on the surface
    Parameters
    ----------
    coords, value; tuple, pygame.Surface
        coords is the coordinate of the place you want to place the object
        value is the object itself
    """
    x, y = coords
    WORLD[x + (height * y)] = value


def get_position(coords, world):
    """
    Gets position of an object on the surface
    Parameters
    ----------
    coords, world; tuple, list
        coords is the coordinate of the object you want pull
        world in the surface array

    Returns
    -------
        out: the value based on the position privided
    """
    x, y = coords
    x, y = int(x), int(y)

    return world[x + (height * y)]


def shooter(coords, d, img):
    """
    defines a shooter
    Parameters
    ----------
    coords, d, img; tuple, pygame.Display, pygame.Surface
        coords is the coordinates for the specific image
        img is the image to display
        d is the display instance
    """
    d.blit(img, coords)


def main():
    """
    main function
    """
    pygame.init()

    display = pygame.display.set_mode((width + 30, height + 50))
    pygame.display.set_caption('Shoot to kill')

    black = (0, 0, 0)
    blue = (0, 0, 128)
    green = (0, 255, 112)

    clock = pygame.time.Clock()
    crashed = False

    human = pygame.image.load('human.png')
    human = transform_img(human, (50, 50))

    wall_img = pygame.image.load('wall.jpg')
    wall_img = transform_img(wall_img, (50, 50))

    bot = pygame.image.load('bot.png')
    bot = transform_img(bot, (50, 50))

    bulletpicture = pygame.image.load('bullet.jpeg')
    bulletpicture = transform_img(bulletpicture, (10, 10))

    matrix = [[wall_img, wall_img, wall_img, wall_img],
              [wall_img, None, wall_img, wall_img],
              [wall_img, None, wall_img, wall_img],
              [wall_img, wall_img, None, wall_img],
              [wall_img, wall_img, None, wall_img],
              [wall_img, wall_img, wall_img, wall_img]]

    x = int(round((width * 0.1), 1))
    y = int(round((height * random.random()), 1))
    x2 = int(round((width * 0.8), 1))
    y2 = int(round((height * random.random()), 1))

    bx_change = 0
    x_change = 0
    y_change = 0
    y2_change = 0

    bullets = []
    bot_bullets = []
    humanisshooting = False
    bot_shooting = False

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = ""
    t = font.render(text, True, green, blue)
    textRect = t.get_rect()
    textRect.center = (width // 2, height // 2)

    human_score = 0
    bot_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    x_change, y_change = directions['S']
                elif event.key == pygame.K_DOWN:
                    x_change, y_change = directions['N']
                elif event.key == pygame.K_SPACE:
                    bot_shooting = False
                    bullets[:] = []
                    humanisshooting = True
                    # This bot generates rondom coordinates based on the
                    # opponen's key strokes, it's hard to beat such a strategy
                    # although it's a vague one
                    y2_change = random.randint(-4, 4)
                    bx_change, _ = directions['E']
                    bullets.append([x, y])
                elif event.key == pygame.K_LEFT:
                    humanisshooting = False
                    bullets[:] = []
                    bot_shooting = True
                    bullets.append([x2, y2])

        display.fill(green)
        walls(display, matrix)
        create_walls(WORLD, display)
        y2 += y2_change

        # Crap; Needs refactor

        if y2 >= height - 8 and y2 <= height + 8:
            if y2_change < 0:
                y2 += y2_change
            else:
                y2_change *= -1
        if y2 >= -5 and y2 <= 5:
            y2_change = 4

        x += x_change
        y += y_change
        if y >= height - 5 and y <= height + 5:
            x_change, y_change = directions['S']
            x += x_change
            y += y_change
        if y >= -5 and y <= 5:
            x_change, y_change = directions["N"]
            y += y_change

        for b in range(len(bullets)):
            if bot_shooting:
                bullets[b][0] -= 10
            elif humanisshooting:
                bullets[b][0] += 10

        for bullet in bullets[:]:
            if (bullet[0] >= width - 5
                    and bullet[0] <= width + 5) or (bullet[0] >= -5
                                                    and bullet[0] <= 5):
                bullets.remove(bullet)

        for bullet in bullets:
            display.blit(bulletpicture, (bullet[0], bullet[1]))
            if y == bullet[1]:
                human_score += 1
            if y2 == bullet[1]:
                bot_score += 1

        # TODO will complete if it ever crosses my mind again
        if human_score > 1 and human_score == bot_score:
            text = "IT'S A TIE"
        elif human_score > 1 and human_score > bot_score:
            text = "YOU WON!!"
        elif human_score > 1 and human_score < bot_score:
            text = "YOU LOST!!"

        display.blit(t, textRect)

        shooter((x, y), display, human)
        shooter((x2, y2), display, bot)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
