#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""



#Import Modules
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
        text = font.render("SURE IS ANTS IN HERE!", 1, (10, 10, 10))
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
    for i in xrange(100):
        ants.append(asset.Entity())
        ants[i].set_anim('ant.png', num=3, frametime=100.0, colorkey=pygame.Color(255, 255, 255))
        ants[i].p = random.randrange(640), random.randrange(480)
		
        asset.get_image('apple.png', -1)
        food = asset.Entity()
        food.set_image('apple.png')
        food.p = 320, 240

		
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
        #allsprites.draw(screen)
        food.p = pygame.mouse.get_pos()
        food.draw(screen,dtTime)
		#swarm test
        for i in xrange(100):
            ax = ants[i].p[0]
            ay = ants[i].p[1]
            if random.randrange(0,100) > 50:
                ax+= 0.1 * dtTime
            if random.randrange(0,100) > 50:
                ax-= 0.1 * dtTime
            if random.randrange(0,100) > 50:
                ay+= 0.1 * dtTime
            if random.randrange(0,100) > 50:
                ay-= 0.1 * dtTime
            if ax < food.p[0] and random.randrange(0,100) > 80:
                ax += 0.1 * dtTime
            if ax > food.p[0] and random.randrange(0,100) > 80:
                ax -= 0.1 * dtTime
            if ay < food.p[1] and random.randrange(0,100) > 80:
                ay += 0.1 * dtTime
            if ay > food.p[1] and random.randrange(0,100) > 80:
                ay -= 0.1 * dtTime
            
            ants[i].p = [ax, ay]
            ants[i].draw(screen,dtTime)
			
        pygame.display.flip()

    pygame.quit()
#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
