import os
import pygame
import sys
from pygame.compat import geterror

if not pygame.font:
    print >> sys.stderr, 'Warning, fonts disabled'
if not pygame.mixer:
    print >> sys.stderr, 'Warning, sound disabled'

main_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(main_dir, 'data')

# dicts of assets
images = {}
sounds = {}
anims = {}

#functions to create our resources
def _image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print >> sys.stderr, 'Cannot load image:', fullname
        sys.exit(geterror())
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def load_image(name, colorkey=None):
    '''Loads an image named `name' and with colorkey `colorkey' from a file.'''
    img = _image(name, colorkey)
    images[name] = img
    return img

def get_image(name, colorkey=None):
    '''Returns an image surface for an image asset named `name' .

    If `name' has been previously loaded, then it returns that instance (`colorkey' param is ignored).
    Otherwise, it calls load_image(name, colorkey).'''
    if name in images:
        return images[name]
    return load_image(name, colorkey)

def _anim(name, num, colorkey=None):
    if not isinstance(num, int) or num < 1:
        raise Exception('invalid num: %s' % num)
    surf = _image(name, colorkey)
    frames = []
    width = (surf.get_width() - num + 1) / num
    height = surf.get_height()
    for i in xrange(num):
        frames.append(surf.subsurface(((width+1) * i, 0, width, height)))
    return frames

def load_anim(name, num, colorkey=None):
    '''Loads an animation named `name' with `num' frames and with colorkey `c' from a file.

    The animation is supposed to be in a spritesheet that has num sprites horizontally, separated by 1px columns.
    Use spritesheet.py to generate such sheets.'''
    anim = _anim(name, num, colorkey)
    anims[name] = anim
    return anim

def get_anim(name, num=0, colorkey=None):
    '''Returns an animation (surface list) for image asset named `name' .

    If `name' has been previously loaded, then it returns that instance (`num' and `colorkey' params are ignored).
    Otherwise, it calls load_anim(name, num, colorkey).'''
    if name in anims:
        return anims[name]
    if num < 1:
        raise Exception('Invalid num: %d!' % num)
    return load_anim(name, num, colorkey)


def _sound(name):
    class NoneSound(object):
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        return pygame.mixer.Sound(fullname)
    except pygame.error:
        print >> sys.stderr, 'Cannot load sound: %s' % fullname
        sys.exit(geterror())

def load_sound(name):
    '''Loads a sound from a file.

    If Pygame's mixer isn't available, returns a null sound.'''
    sound = _sound(name)
    sounds[name] = sound
    return sound

def get_sound(name):
    '''Returns a sound asset named `name'.

    If `name' has been previously loaded, then it returns that instance.
    Otherwise, it calls load_sound(name).'''
    if name in sounds:
        return sounds[name]
    return load_sound(name)


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.p = [100, 100]

    def set_image(self, name):
        self.anim = None
        self.image = get_image(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def set_anim(self, name, frametime=1, num=0, colorkey=0):
        '''Use an animation (see get_anim) as the sprite.

        Gets an animation named `anim' (num and colorkey used if it's not already loaded).
        Changes to the next frame every `frametime' milliseconds.'''
        self.anim = get_anim(name, num, colorkey)
        self.anim_counter = 0.0
        self.anim_frame = 0
        self.image = self.anim[0]
        self.rect = self.anim[0].get_rect()
        self.rect.topleft = [0, 0]
        self.frame_time = frametime

    def update(self, dt):
        self.rect[0] = self.p[0] - (self.rect[2]/2)
        self.rect[1] = self.p[1] - (self.rect[3]/2)
        if self.anim:
            self.anim_counter += dt
            if self.anim_counter > self.frame_time:
                self.anim_counter = 0.0
                self.anim_frame += 1
                #print self.anim_frame
                if self.anim_frame > len(self.anim)-1:
                    self.anim_frame = 0
                self.image = self.anim[self.anim_frame]


    def draw(self, target, dt):
        self.update(dt)
        g = pygame.sprite.RenderPlain(self)
        g.draw(target)
        g.empty()
