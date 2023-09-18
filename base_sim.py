
import numpy as np
import pygame, sys, random
from pygame.locals import *
pygame.init()

# Screen Setup
BACKGROUND = '#C4A484'
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 150

# Tweak
tweak_delay = 2
tweak_turning = .3
carrying_capacity = 25

# Sim Setup
ants_grid_x_y = 16
anthill = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]
pheromone_grid = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))
 
 
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

  def move(self):
    pheromone_grid[int(self.y)][int(self.x)] = min(carrying_capacity, pheromone_grid[int(self.y)][int(self.x)] + 2)
    self.x += directions[self.velocity][0]
    self.y += directions[self.velocity][1]
    self.x = self.x%WINDOW_WIDTH
    self.y = self.y%WINDOW_HEIGHT

  def explore(self):
    self.phero_check()
    self.velocity = round(self.velocity + np.random.normal(scale = tweak_turning))%8
    self.move()

  def phero_check(self):
    detecting = {}
    for direction in directions:
      check_x = int(self.x) + directions[direction][0]
      check_y = int(self.y) + directions[direction][1]
      detecting[direction] = pheromone_grid[check_y%WINDOW_HEIGHT][check_x%WINDOW_WIDTH]
    print(detecting)

  def draw(self):
    pygame.draw.rect(WINDOW, 'red',pygame.Rect(self.x, self.y, 5, 5))


ants = []

def first_spawn():
  for _ in range(20):
    ants.append(Ant())


def draw_grid():
    y = 0  # we start at the top of the screen
    for row in pheromone_grid:
        x = 0 # for every row we start at the left of the screen again
        for item in row:
            f = max(0, item / carrying_capacity)
            color = (127 * f, 191 * f, 63 + 192 * f)

            pygame.draw.rect(WINDOW, color, [x, y, 1, 1])
            x += 1 # for ever item/number in that row we move one "step" to the right
        y += 1   # for every new row we move one "step" downwards


def update() :
  draw_grid()

  for ant in ants:
    ant.explore()
    ant.draw()

  pygame.display.update()

  for row in pheromone_grid:
    for space in row:
      space = max(0, space-1)


def main () :
  
  looping = True

  first_spawn()
  # The main  loop
  while looping :
    clock.tick(FPS)
    # Get inputs
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    # Processing
    WINDOW.fill(BACKGROUND)
    update()
 
    # Render

    pygame.display.flip()
 
main()
