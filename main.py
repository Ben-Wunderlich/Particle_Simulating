
import pygame
from time import sleep
from random import randint
import numpy as np

(BLACK, WHITE) = ((0,0,0), (255,255,255))

(WIDTH, HEIGHT) = (400,400)
RADIUS = 2
THICCNESS = RADIUS
HALF_RADIUS = RADIUS//2

#track each particle with a dictionary, key is position? value is vector
data = set()
data2 = np.ones((WIDTH, HEIGHT, 2))#3rd has vector for speed of particle
occupiedSquares = set()

def Populate(numParticales=1):
    for _ in range(numParticales):
        nextParticle = ((randint(0,WIDTH), randint(0,HEIGHT)), (randint(-3, 3), randint(-2, 2)))
        if nextParticle[1][0] == 0 or nextParticle[1][1] == 0:
            continue 
        data.add(nextParticle)

def Wipe(screen):
    pygame.Surface.fill(screen, BLACK)

#returns newPos, newvelo
def BounceCheck(pos, velo):
    newPos = (pos[0]+velo[0], pos[1]+velo[1])
    newVelo = velo

    if pos[0] < 0:#left wall
        newVelo = (-velo[0], velo[1])
        newPos = (-newPos[0], newPos[1])
    elif pos[0] > WIDTH:#right wall
        newVelo = (-velo[0], velo[1])
        newPos = (WIDTH - (2*(newPos[0]-WIDTH)), newPos[1])
    pos, velo = newPos, newVelo

    if pos[1] < 0:#ceiling
        newVelo = (velo[0], -velo[1])
        newPos = (newPos[0], -newPos[1])
    elif pos[1] > HEIGHT:#floor
        newVelo = (velo[0], -velo[1])
        newPos = (newPos[0], HEIGHT - (2*(newPos[1]-HEIGHT)))

    return (newPos, newVelo)

def CollisionCheck(particleData):
    pass
    #if 2 in same square they become one particle with summed components
    newData = set()
    duplicates = set()
    for pos, velo in particleData:
        for x in range(pos[0]-HALF_RADIUS, pos[0]+HALF_RADIUS):
            for y in range(pos[1]-HALF_RADIUS, pos[1]+HALF_RADIUS):
                pass


Populate(5)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pass

    Wipe(screen)
    nextFrame = set()
    for pos, velo in data:        
        newPos, newVelo = BounceCheck(pos, velo)

        nextFrame.add((newPos, newVelo))
        pygame.draw.circle(screen, WHITE, newPos, RADIUS, THICCNESS)
        
    data = nextFrame
    pygame.display.update()
    sleep(0.01)
