import os
import pygame
import sys
from pygame.locals import *
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
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_image(id, c=None):
    '''Loads an image named `id' and with colorkey `c' from a file.'''
    img, imgrec = _image(id, c)
    images[id] = (img, imgrec)
    return img, imgrec

def get_image(id, colorkey=None):
    '''Returns a tuple (image, rect) for an image asset named `id' .

    If `id' has been previously loaded, then it returns that instance (`colorkey' param is ignored).
    Otherwise, it calls load_image(id, colorkey).'''
    if id in images:
        return images[id]
    return load_image(id, colorkey)


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

def load_sound(id):
    '''Loads a sound from a file.

    If Pygame's mixer isn't available, returns a null sound.'''
    sound = _sound(id)
    sounds[id] = sound
    return sound

def get_sound(id):
    '''Returns a sound asset named `id'.

    If `id' has been previously loaded, then it returns that instance.
    Otherwise, it calls load_sound(id).'''
    if id in sounds:
        return sounds[id]
    return load_sound(id)


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.p = [100, 100]

    def set_image(self, id):
        self.image = get_image(id)[0]
        self.rect = get_image(id)[1]
        self.rect.topleft = [0, 0]

    def update(self):
        self.rect[0] = self.p[0]
        self.rect[1] = self.p[1]

    def draw(self, target):
        self.update()
        g = pygame.sprite.RenderPlain(self)
        g.draw(target)
        g.empty()
