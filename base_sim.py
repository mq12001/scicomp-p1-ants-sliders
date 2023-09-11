
import numpy as np
import pygame, sys, random
from pygame.locals import *
pygame.init()

# Sim Setup
ants_grid = np.zeros(16, 16)
anthill = [8, 8]
 
# Game Setup
BACKGROUND = (255, 255, 255)
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ants + Anthills')
 
# The main function that controls the game
def main () :
  looping = True
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    # Processing
    # This section will be built out later
 
    # Render elements of the game
    WINDOW.fill(BACKGROUND)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
