
import numpy as np
import pygame
import sys
import random
from pygame.locals import *
pygame.init()

# Screen Setup
BACKGROUND = '#C4A484'
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Tweak
tweak_delay = 2
tweak_turning = .3
carrying_capacity = 100

# Sim Setup
num_squares_side = 170
square_size = 3
anthill = [num_squares_side/2, num_squares_side/2]
pheromone_grid = np.zeros((num_squares_side, num_squares_side))


WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ants + Anthills')

directions = {
    0: [0, 1],
    1: [1, 1],
    2: [1, 0],
    3: [1, -1],
    4: [0, -1],
    5: [-1, -1],
    6: [-1, 0],
    7: [-1, 1]
}


class Ant:
    def __init__(self) -> None:
        self.x = anthill[0]
        self.y = anthill[1]
        self.velocity = np.random.randint(7)
        self.detected = {}

    def move(self):
        pheromone_grid[int(self.y)][int(self.x)] = min(
            carrying_capacity, pheromone_grid[int(self.y)][int(self.x)] + 10)
        self.x += directions[self.velocity][0]
        self.y += directions[self.velocity][1]
        self.x = self.x % num_squares_side
        self.y = self.y % num_squares_side

    def explore(self):
        self.phero_check()
        self.turn()
        self.move()

    def turn(self):
        max_direction = None
        max = 0
        for angle in [0, 1, 7, 6, 2]:
            direction = (self.velocity + angle) % 8
            if self.detected[direction] > max:
                max_direction = direction
                max = self.detected[direction]

        get_confused = np.random.rand()  # *(max/carrying_capacity)
        if get_confused < .4:
            max_direction = None

        if max_direction == None:
            self.velocity = round(
                self.velocity + np.random.normal(scale=tweak_turning)) % 8
        else:
            self.velocity = max_direction

    def phero_check(self):
        for direction in directions:
            check_x = int(self.x) + (directions[direction][0])
            check_y = int(self.y) + (directions[direction][1])
            self.detected[direction] = pheromone_grid[check_y %
                                                      num_squares_side][check_x % num_squares_side]

    def draw(self):
        pygame.draw.rect(WINDOW, 'red', pygame.Rect(
            c_projection(self.x), c_projection(self.y), square_size, square_size))


ants = []


def first_spawn():
    for _ in range(200):
        ants.append(Ant())


def c_projection(coordinate):
    margin = WINDOW_HEIGHT - num_squares_side*square_size
    return (margin/2) + coordinate*square_size


def draw_grid():
    y = 0  # we start at the top of the screen
    for row in pheromone_grid:
        x = 0  # for every row we start at the left of the screen again
        for pheromone in row:
            f = max(0, pheromone / carrying_capacity)  # 135 116 72 -> 97 65 15
            color = (135 - 38*f, 116 - 51*f, 72 - 57*f)

            pygame.draw.rect(WINDOW, color, [c_projection(
                x), c_projection(y), square_size, square_size])
            x += 1  # for ever item/number in that row we move one "step" to the right
        y += 1   # for every new row we move one "step" downwards


def update():
    for y in range(num_squares_side):
        for x in range(num_squares_side):
            pheromone_grid[y][x] = max(0, pheromone_grid[y][x] - 1)

    draw_grid()

    for ant in ants:
        ant.explore()
        ant.draw()

    pygame.display.update()


def main():

    looping = True

    img = pygame.image.load("img/grass.png").convert()
    imageWidth, imageHeight = img.get_size()
    tilesX = int(np.ceil(WINDOW_WIDTH / imageWidth))
    tilesY = int(np.ceil(WINDOW_HEIGHT / imageHeight))

    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            WINDOW.blit(img, (.8*x * imageWidth, .8*y * imageHeight))

    pygame.draw.rect(WINDOW, (97, 65, 15), [c_projection(
        -3), c_projection(-3), square_size*(num_squares_side+6), square_size*(num_squares_side+6)])

    first_spawn()
    # The main  loop
    while looping:
        clock.tick(FPS)
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Processing
        update()

        # Render

        pygame.display.flip()


main()
