#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

import asset
import formicarium
import math
import pygame
import random

FPS = 60
NUM_ANTS = 30
NUM_FOOD = 10
SCREEN_X = 1024
SCREEN_Y = 768

def getDistance(a, b):
    dist = math.hypot(a[0]-b[0], a[1]-b[1])
    if dist < 0:
        dist *= -1
    return dist

def moveToTarget(a, b, vel):
    ax = a[0]
    ay = a[1]
    if a[0] < b[0]:
        ax += vel
    if a[0] > b[0]:
        ax -= vel
    if a[1] < b[1]:
        ay += vel
    if a[1] > b[1]:
        ay -= vel
    return [ax, ay]

def moveToRandom(a, random_bias, vel):
    ax = a[0]
    ay = a[1]
    if random.randrange(0, 100) > random_bias:
        ax += vel
    else:
        ax -= vel
    if random.randrange(0, 100) > random_bias:
        ay += vel
    else:
        ay -= vel
    return [ax, ay]

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('LD23 a tiny world')
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(1, 10)
    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    formic = formicarium.Formicarium(background)

    #Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("press space to shuffle food", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        formic.draw()
        background.blit(text, textpos)

    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    #Prepare Game Objects
    clock = pygame.time.Clock()

    ants = []
    for i in xrange(NUM_ANTS):
        ants.append(asset.Entity())
        ants[i].set_anim('ant.png', num=3, frametime=100.0, colorkey=pygame.Color(255, 255, 255))
        ants[i].p = [SCREEN_X/2., SCREEN_Y/2.]
        ants[i].home = 0
        ants[i].target = [-1, -1]
        ants[i].life = 200

    asset.get_image('apple.png', -1)
    food = []
    for i in xrange(NUM_FOOD):
        food.append(asset.Entity())
        food[i].set_image('apple.png')
        food[i].p = random.randrange(SCREEN_X), random.randrange(SCREEN_Y)
        food[i].life = random.randrange(15)

    asset.get_image('ant_hill.png', -1)
    home = asset.Entity()
    home.set_image('ant_hill.png')
    home.p = SCREEN_X/2., SCREEN_Y/2.
    home.target = [-1, -1]

    #Main Loop
    currentTime = pygame.time.get_ticks()
    newTime = 0.0
    frameTime = 0.0
    accumulator = 0.0
    dt = 1000.0/60.0 #60 fps
    dtTime = 0.0 #total time for this frame, for animations

    going = True
    while going:
        #clock.tick(1.0/100.0)
        #Handle Input Events
        newTime = pygame.time.get_ticks()
        frameTime = newTime - currentTime
        currentTime = newTime
        accumulator += frameTime
        dtTime = 0.0
        #loop for smooth delta input, use dtTime for animations after the while loop
        while accumulator > dt:
            accumulator -= dt
            dtTime += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        going = False
                    elif event.key == pygame.K_SPACE:
                        for i in xrange(NUM_FOOD):
                            food[i].p = random.randrange(SCREEN_X), random.randrange(SCREEN_Y)

        #Draw Everything
        screen.blit(background, (0, 0))
        #uncommenting these two lines will let you move an infinite foodsource around and control the ants
        #food[0].p = pygame.mouse.get_pos()
        #food[0].life = 1000
        home.draw(screen, dtTime)
        for i in xrange(NUM_FOOD):
            food[i].draw(screen, dtTime)
        #swarm test
        for i in xrange(NUM_ANTS):
            if ants[i].home == 0:
                for j in xrange(NUM_FOOD):
                    if getDistance(ants[i].p, food[j].p) < 130 and ants[i].target[0] == -1:
                        ants[i].p = moveToTarget(ants[i].p, food[j].p, 0.01 * dtTime)
                    if getDistance(ants[i].p, food[j].p) < 20:
                        if food[j].life < 0:
                            food[j].p = random.randrange(SCREEN_X), random.randrange(SCREEN_Y)
                            food[j].life = random.randrange(100)
                            ants[i].target = [-1, -1]
                            ants[i].home = 1
                        else:
                            food[j].life -= 1
                            ants[i].home = 1
                            ants[i].target = food[j].p

                if ants[i].target[0] != -1:
                    ants[i].p = moveToTarget(ants[i].p, ants[i].target, 0.1 * dtTime)
                    if getDistance(ants[i].p, ants[i].target) < 10 and ants[i].home == 0:
                        #ants[i].home = 1
                        ants[i].target = [-1, -1]
                else:
                    #ants[i].p = moveToRandom(ants[i].p, 50, 0.1 * dtTime)
                    distx = random.randrange(10, SCREEN_X/2.)
                    disty = random.randrange(10, SCREEN_Y/2.)
                    ants[i].target = ants[i].p[0] + random.randrange(-distx, distx), ants[i].p[1] + random.randrange(-disty, disty)

            if ants[i].home == 1:
                ants[i].p = moveToTarget(ants[i].p, home.p, 0.1 * dtTime)
                if getDistance(ants[i].p, home.p) < 10:
                    ants[i].home = 0
                    ants[i].life = 200
                    ant_target = ants[i].target
                    if home.target[0] != -1:
                        ants[i].target = home.target
                    if ants[i].target[0] != -1:
                        home.target = ant_target
            if ants[i].home != 1:
                ants[i].life -= 1
            if ants[i].life < 0 and ants[i].target[0] == -1:
                ants[i].home = 1

            if getDistance(ants[i].p, home.p) > 25:
                ants[i].draw(screen, dtTime)

        pygame.display.flip()

    pygame.quit()
    #Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
