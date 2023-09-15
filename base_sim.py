
import numpy as np
import pygame, sys, random
from pygame.locals import *
pygame.init()

# Screen Setup
BACKGROUND = '#C4A484'
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

# Tweak
tweak_delay = 2
tweak_turning = .3

# Sim Setup
ants_grid_x_y = 16
anthill = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]
pheromone_grid = np.zeros(WINDOW_WIDTH, WINDOW_HEIGHT)
 
 
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
    pheromone_grid[self.x, self.y] += 2
    self.x += directions[self.velocity][0]
    self.y += directions[self.velocity][1]
    self.x = self.x%WINDOW_WIDTH
    self.y = self.y%WINDOW_HEIGHT

  def explore(self):
    self.velocity = round(self.velocity + np.random.normal(scale = tweak_turning))%8
    self.move()

  def phero_check(self):
    for direction in directions:
      check_x = self.x + direction[0]
      check_y = self.y + direction[1]

  def draw(self):
    pygame.draw.rect(WINDOW, 'red',pygame.Rect(self.x, self.y, 5, 5))


ants = []

def first_spawn():
  for _ in range(20):
    ants.append(Ant())


def update() :
  for ant in ants:
    ant.explore()
    ant.draw()
  for space in pheromone_grid:
    space -= 1

last_time = 0

def time_step(delay) :
  if pygame.time.get_ticks() > (last_time + delay):
    last_time = pygame.time.get_ticks()
    update()


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
