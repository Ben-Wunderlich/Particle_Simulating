
import pygame
from time import sleep
from random import randint
import numpy as np
from math import ceil

(BLACK, WHITE) = ((0,0,0), (255,255,255))

(WIDTH, HEIGHT) = (800,510)
RADIUS = 10
THICCNESS = RADIUS

DRAG=1.05

#track each particle with a dictionary, key is position? value is vector
#data = set()
data = np.ones((WIDTH+1, HEIGHT+1, 2), dtype=int)#3rd has vector for speed of particle
occupiedSquares = set()

def GetRands():
    return (randint(0,WIDTH), randint(0,HEIGHT)), (randint(-3, 3), randint(-2, 2))

def Populate(numParticales=1):
    for _ in range(numParticales):
        nextPos, nextVelo = GetRands()
        while nextVelo[0] == 0 or nextVelo[1] == 0:
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
        newVelo = (-ceil(velo[0]/DRAG), velo[1])
        newPos = (-newPos[0], newPos[1])

    elif newPos[0] >= WIDTH:#right wall
        newVelo = (-ceil(velo[0]/DRAG), velo[1])
        newPos = (WIDTH - (2*(newPos[0]-WIDTH)), newPos[1])

    pos, velo = newPos, newVelo

    if newPos[1] < 0:#ceiling
        newVelo = (velo[0], -ceil(velo[1]/DRAG))
        newPos = (newPos[0], -newPos[1])

    elif newPos[1] >= HEIGHT:#floor
        newVelo = (velo[0], -ceil(velo[1]/DRAG))
        newPos = (newPos[0], HEIGHT - (2*(newPos[1]-HEIGHT)))

    newPos, newVelo = (int(newPos[0]), int(newPos[1])), (int(newVelo[0]), int(newVelo[1]))
    return (newPos, newVelo)

def CollisionCheck(occupied):
    #if 2 in same square they become one particle with summed components
    newOccupied = set()
    for pos in occupied:
        taken=False

        for x in range(pos[0]-RADIUS, pos[0]+RADIUS):
            for y in range(pos[1]-RADIUS, pos[1]+RADIUS):
                if (x,y)!= pos and (x,y) in occupied and not (x,y) in newOccupied:
                    newOccupied.add((x,y))
                    newOccupied.add(pos)

                    reversedPos = (-data[pos[0]][pos[1]][0]+data[x][y][0], 
                    -data[pos[0]][pos[1]][1]+data[x][y][1])

                    reversedPos = (ceil(reversedPos[0]/DRAG), ceil(reversedPos[1]/DRAG))

                    reversedXy = (data[pos[0]][pos[1]][0]-data[x][y][0], 
                    -data[pos[0]][pos[1]][1]-data[x][y][1])

                    reversedXy = (ceil(reversedXy[0]/DRAG), ceil(reversedXy[1]/DRAG))

                    data[x][y] =  reversedXy
                    data[pos[0]][pos[1]] = reversedPos
                    taken = True
        if not taken:
            newOccupied.add(pos)
    return newOccupied

#returns its velocity and position after 1 frame
def ApplyGravity(pos, velocity, acceleration=3):
    if pos[1] < HEIGHT//2:
        newVelo = (velocity[0], velocity[1]+acceleration)
    else:
        newVelo = (velocity[0], velocity[1]-acceleration)
    return newVelo

Populate(12)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
speed=0.025

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speed/=1.1
    elif keys[pygame.K_DOWN]:
        speed*=1.1

    Wipe(screen)
    nextFrame = set()
    for pos in occupiedSquares:
        newVelo = ApplyGravity(pos, data[pos[0]][pos[1]], -5)
        newPos, newVelo = BounceCheck(pos, newVelo)

        nextFrame.add(newPos)
        data[newPos[0]][newPos[1]] = newVelo
        pygame.draw.circle(screen, (255-newPos[1]//2, newPos[1]//2, 255), newPos, RADIUS, THICCNESS)
        
    occupiedSquares = nextFrame

    occupiedSquares = CollisionCheck(occupiedSquares)

    pygame.display.update()
    sleep(speed)
