
import numpy as np
import pygame, sys, random
from pygame.locals import *
pygame.init()

# Tweak
tweak_delay = 2
tweak_turning = 1

# Sim Setup
ants_grid_x_y = 16
anthill = [8, 8]
 
# Screen Setup
BACKGROUND = 'gray'
FPS = 60
clock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ants + Anthills')

direction = {
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
    self.x += direction[self.velocity][0]
    self.y += direction[self.velocity][1]
    self.velocity = round(self.velocity + np.random.normal(scale = tweak_turning))%8

  def draw(self):
    pygame.draw.rect(WINDOW, 'red',pygame.Rect(self.x + 50,self.y + 50, 5, 5))


ants = []

def first_spawn():
  for _ in range(20):
    ants.append(Ant())


def update() :
  for ant in ants:
    ant.move()
    ant.draw()

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
