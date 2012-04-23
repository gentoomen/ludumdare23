#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""



#Import Modules
import math
import asset
import os
import pygame
from pygame.locals import *
from pygame.compat import geterror
import random
#if not pygame.font: print ('Warning, fonts disabled')
#if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

FPS = 60

#import objects
#from objects import *


#classes for our game objects
#these two can be removed later, just using them to have some interactivity while testing assets
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = asset.get_image('fist.bmp', -1)
        self.rect = self.image.get_rect()
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image = asset.get_image('coolface.png', -1)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        #else:
            #self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 1)
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 5
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
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
        ax+= vel
    else:
        ax-= vel
    if random.randrange(0, 100) > random_bias:
        ay+= vel
    else:
        ay-= vel
    return [ax, ay]


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('LD23 a tiny world')
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(1, 10)
#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("press space to shuffle food", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(asset.get_image('f4.png', 0), (0,0))
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
#Prepare Game Objects
    clock = pygame.time.Clock()

    chimp = Chimp()
    fist = Fist()

    allsprites = pygame.sprite.RenderPlain((fist, chimp))
    
    ants = []
    for i in xrange(30):
        ants.append(asset.Entity())
        ants[i].set_anim('ant.png', num=3, frametime=100.0, colorkey=pygame.Color(255, 255, 255))
        ants[i].p = [320,240]
        ants[i].home = 0
        ants[i].target = [-1,-1]
        ants[i].life = 200

	asset.get_image('apple.png', -1)
    food = []
    for i in xrange(10):
        food.append(asset.Entity())
        food[i].set_image('apple.png')
        food[i].p = random.randrange(640), random.randrange(480)
        food[i].life = random.randrange(15)

    asset.get_image('ant_hill.png', -1)
    home = asset.Entity()
    home.set_image('ant_hill.png')
    home.p = 320,240
    home.target = [-1,-1]
		
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
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    if event.key == K_LEFT:
                        chimp.rect[0] -= 0.1 * dt
                    if event.key == K_RIGHT:
                        chimp.rect[0] += 0.1 * dt
                    if event.key == K_UP:
                        chimp.rect[1] -= 0.1 * dt
                    if event.key == K_DOWN:
                        chimp.rect[1] += 0.1 * dt
                    if event.key == K_SPACE:
                        for i in xrange(10):
                            food[i].p = random.randrange(640), random.randrange(480)


                elif event.type == MOUSEBUTTONDOWN:
                    if fist.punch(chimp):
                        asset.get_sound('punch.wav').play() #punch
                        chimp.punched()
                    else:
                        asset.get_sound('whiff.wav').play() #miss
                elif event.type == MOUSEBUTTONUP:
                    fist.unpunch()

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        #uncommenting these two lines will let you move an infinite foodsource around and control the ants
        #food[0].p = pygame.mouse.get_pos()
        #food[0].life = 1000
        home.draw(screen,dtTime)
        for i in xrange(10):
            food[i].draw(screen,dtTime)
        #swarm test 
        for i in xrange(30):
            if ants[i].home == 0:
                for j in xrange(10):
                    if getDistance(ants[i].p, food[j].p) < 130 and ants[i].target[0] == -1:
                        ants[i].p = moveToTarget(ants[i].p, food[j].p, 0.01 * dtTime)
                    if getDistance(ants[i].p, food[j].p) < 20:
                        if food[j].life < 0:
                            food[j].p = random.randrange(640), random.randrange(480)
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
                    distx = random.randrange(10,320)
                    disty = random.randrange(10,240)
                    ants[i].target = ants[i].p[0] + random.randrange(-distx,distx), ants[i].p[1] + random.randrange(-disty,disty)

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
                ants[i].draw(screen,dtTime)
			
        pygame.display.flip()

    pygame.quit()
#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
