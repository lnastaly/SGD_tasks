import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

cat2Img = pygame.image.load('cat2.png')
cat2x = 280
cat2y = 220
direction2 = 'left'

while True: # the main game loop
    DISPLAYSURF.fill(WHITE)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    if direction2 == 'right':
        cat2x += 5
        if cat2x == 280:
            direction2 = 'down'
    elif direction2 == 'down':
        cat2y += 5
        if cat2y == 220:
            direction2 = 'left'
    elif direction2 == 'left':
        cat2x -= 5
        if cat2x == 10:
            direction2 = 'up'
    elif direction2 == 'up':
        cat2y -= 5
        if cat2y == 10:
            direction2 = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))
    DISPLAYSURF.blit(cat2Img, (cat2x, cat2y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)