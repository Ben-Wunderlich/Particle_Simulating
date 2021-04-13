
import pygame
from time import sleep
from random import randint
import numpy as np
from math import ceil

(BLACK, WHITE) = ((0,0,0), (255,255,255))

(WIDTH, HEIGHT) = (600,600)
RADIUS = 8
THICCNESS = RADIUS

#track each particle with a dictionary, key is position? value is vector
#data = set()
data = np.ones((WIDTH+1, HEIGHT+1, 2), dtype=int)#3rd has vector for speed of particle
occupiedSquares = set()

def GetRands():
    return (randint(0,WIDTH), randint(0,HEIGHT)), (randint(-3, 3), randint(-2, 2))

def Populate(numParticales=1):
    for _ in range(numParticales):
        nextPos, nextVelo = GetRands()
        while nextVelo[0] == 0 and nextVelo[1] == 0:
            nextPos, nextVelo = GetRands() 
        #print(nextVelo)
        data[nextPos[0]][nextPos[1]] = nextVelo
        occupiedSquares.add(nextPos)

def Wipe(screen):
    pygame.Surface.fill(screen, BLACK)

#returns newPos, newvelo
def BounceCheck(pos, velo):
    newPos = (pos[0]+velo[0], pos[1]+velo[1])
    newVelo = velo

    if newPos[0] < 0:#left wall
        newVelo = (-ceil(velo[0]/1.1), velo[1])
        newPos = (-newPos[0], newPos[1])

    elif newPos[0] >= WIDTH:#right wall
        newVelo = (-ceil(velo[0]/1.1), velo[1])
        newPos = (WIDTH - (2*(newPos[0]-WIDTH)), newPos[1])

    pos, velo = newPos, newVelo

    if newPos[1] < 0:#ceiling
        newVelo = (velo[0], -ceil(velo[1]/1.1))
        newPos = (newPos[0], -newPos[1])

    elif newPos[1] >= HEIGHT:#floor
        newVelo = (velo[0], -ceil(velo[1]/1.1))
        newPos = (newPos[0], HEIGHT - (2*(newPos[1]-HEIGHT)))

    newPos, newVelo = (int(newPos[0]), int(newPos[1])), (int(newVelo[0]), int(newVelo[1]))
    return (newPos, newVelo)

def CollisionCheck(occupied):
    #if 2 in same square they become one particle with summed components
    newOccupied = set()
    rejected = set()
    for pos in occupied:
        taken=False

        for x in range(pos[0]-RADIUS, pos[0]+RADIUS):
            for y in range(pos[1]-RADIUS, pos[1]+RADIUS):
                if (x,y)!= pos and (x,y) in occupied and not (x,y) in rejected and not (x,y) in newOccupied:
                    rejected.add(pos)
                    newOccupied.add((x,y))
                    data[x][y] =  (data[pos[0]][pos[1]][0]+data[x][y][0], 
                    data[pos[0]][pos[1]][1]+data[x][y][1])
                    taken = True
        if not taken:
            newOccupied.add(pos)
    return newOccupied


Populate(1000)
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
    for pos in occupiedSquares:
        newPos, newVelo = BounceCheck(pos, data[pos[0]][pos[1]])

        nextFrame.add(newPos)
        #print(newPos[0], newPos[1])
        data[newPos[0]][newPos[1]] = newVelo
        pygame.draw.circle(screen, WHITE, newPos, RADIUS, THICCNESS)
        
    occupiedSquares = nextFrame

    occupiedSquares = CollisionCheck(occupiedSquares)

    pygame.display.update()
    sleep(0.01)
