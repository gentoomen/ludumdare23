import os, pygame
from pygame.locals import *
from pygame.compat import geterror

#if not pygame.font: print ('Warning, fonts disabled')
#if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#asset stacks
images = []
sounds = []

#functions to create our resources
def _image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_image(id, c):    
    img, imgrec = _image(id, c)
    images.append((id, img, imgrec))
    return img, imgrec

def getImage(id):
    return images[id][1]

    
def _sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def load_sound(id):    
    sound = _sound(id)
    sounds.append((id, sound))
    return sound
        
def getSound(id):
    return sounds[id][1]
    

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.p = 100, 100
        
    def setImage(self, id):
        self.image = images[id][1]
        self.rect = images[id][2]
        self.rect.topleft = 0, 0
    
    def update(self):
        self.rect[0] = self.p[0]
        self.rect[1] = self.p[1]

    def draw(self, target):
		self.update()
		g = pygame.sprite.RenderPlain(self)
		g.draw(target)
		g.empty()
		