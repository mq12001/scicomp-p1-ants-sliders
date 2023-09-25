import numpy as np
import pygame
import sys
from pygame.locals import *
pygame.init()

# Screen Setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
num_squares_side = 170
square_size = 3

# Animation Setup
FPS = 60
clock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ants + Anthills')

# Sim-Defining Variables
turning_kernel = .3
carrying_capacity = 100
fidelity = .7
deposition_rate = 10

# Setup (Empty Variables, etc)
pheromone_grid = np.zeros((num_squares_side, num_squares_side))
anthill = [num_squares_side/2, num_squares_side/2]
ants = []
num_ants = 1500

# Directions setup for mod 8
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

    def __init__(self):
        """Initialize an ant on the anthill"""
        self.x = anthill[0]
        self.y = anthill[1]
        self.velocity = np.random.randint(7)
        self.phero_max = None

    def explore(self):
        """Main body of ant movement - All ants perform three steps
        """
        self.phero_check()
        self.turn()
        self.move()

    def phero_check(self):
        """Checks all 5 blocks in front of/beside the ant and stores 
        the one with the highest pheromone concentration
        """
        self.phero_max = None
        max = 0
        for angle in [0, 1, 7, 6, 2]:  # Only checking these 5 directions
            # Check angle relative to whole grid instead of to the individual ant
            checked_angle = (self.velocity+angle) % 8
            check_x = (
                int(self.x)+directions[checked_angle][0]) % num_squares_side
            check_y = (
                int(self.y)+directions[checked_angle][1]) % num_squares_side
            if pheromone_grid[check_y][check_x] > max:
                # If it's greater than the max, it is saved as the new direction
                self.phero_max = checked_angle
                max = pheromone_grid[check_y][check_x]

    def turn(self):
        """Determines, based on pheromone values and chance, the direction
        an ant will move in next
        """

        # Ant has a small chance of getting lost, no matter what
        if np.random.rand() < (1 - fidelity):
            self.phero_max = None

        # If ant is lost, ant explores
        if self.phero_max == None:
            self.velocity = round(
                self.velocity + np.random.normal(scale=turning_kernel)) % 8
        # If ant is not lost, ant follows greatest pheromone trail
        else:
            self.velocity = self.phero_max

    def move(self):
        """Ant deposits pheromone and moves"""
        # Deposit pheromone
        pheromone_drop = pheromone_grid[int(self.y)][int(self.x)] \
            + deposition_rate
        pheromone_grid[int(self.y)][int(self.x)] = \
            min(carrying_capacity, pheromone_drop)

        # Move
        self.x = (self.x + directions[self.velocity][0]) % num_squares_side
        self.y = (self.y + directions[self.velocity][1]) % num_squares_side

    def draw(self):
        """Pygame function to draw the ant"""
        pygame.draw.rect(WINDOW, 'red', pygame.Rect(
            c_projection(self.x), c_projection(self.y), square_size, square_size))


def first_spawn():
    """Spawn in the ants"""
    for _ in range(num_ants):
        ants.append(Ant())


def c_projection(coordinate):
    """Transforms the model variables into their corresponding on-screen representation

    Args:
        coordinate (int): The index of a square in the grid that represents the model

    Returns:
        int: The coordinate that represents that grid location on screen
    """
    margin = WINDOW_HEIGHT - num_squares_side*square_size
    return (margin/2) + coordinate*square_size


def update_phero_grid():
    """Shows the pheromone concentration for every point on the grid that constitutes 
    the model
    """
    # Decreases every pheromone square on the grid
    for y in range(num_squares_side):
        for x in range(num_squares_side):
            pheromone_grid[y][x] = max(0, pheromone_grid[y][x] - 1)

    # Renders the whole pheromone grid
    y = 0
    for row in pheromone_grid:
        x = 0
        for pheromone in row:
            f = max(0, pheromone / carrying_capacity)  # Percentage convered

            # No Pheromone: 135 116 72 -> Fully Covered: 97 65 15
            color = (135 - 38*f, 116 - 51*f, 72 - 57*f)

            pygame.draw.rect(WINDOW, color, [c_projection(
                x), c_projection(y), square_size, square_size])
            x += 1
        y += 1


def update_ants():
    """Update ants!"""
    for ant in ants:
        ant.explore()
        ant.draw()


def update():
    """Updates the model every timestep"""
    update_phero_grid()
    update_ants()
    pygame.display.update()


def init_background():
    """Draws the grass in the background"""
    img = pygame.image.load("img/grass.png").convert()
    imageWidth, imageHeight = img.get_size()
    tilesX = int(np.ceil(WINDOW_WIDTH / imageWidth))
    tilesY = int(np.ceil(WINDOW_HEIGHT / imageHeight))

    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            WINDOW.blit(img, (.8*x * imageWidth, .8*y * imageHeight))


def init():
    """Initializes the background and conditions of the sim"""
    # Draw the grass
    init_background()

    # Draw the sandbox
    pygame.draw.rect(WINDOW, (97, 65, 15), [c_projection(
        -3), c_projection(-3), square_size*(num_squares_side+6), square_size*(num_squares_side+6)])

    # Spawn in all of the ants!
    first_spawn()


def main():
    """Main loop"""

    init()

    looping = True
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
