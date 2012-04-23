import asset
import pygame
import random

DIRT = pygame.Color(150, 50, 0) # dirt color
AIR = pygame.Color(250, 150, 100) # tunnel color
SIZE = 16 # tunnel size
TUNNELS = 10 # increase for more tunnels
DISTANCE = 0 # increase for longer tunnels, 0 to disable
MOVE = 8 # how much tunnel to generate at once in one direction

class Formicarium(object):
    '''A randomly generated ant formicarium.'''

    def __init__(self, surf):
        '''Generate a formicarium.

        `surf' (a pygame.Surface) argument's size will be used as the formicarium's size.'''
        self.surf = surf
        self.dim = surf.get_size()
        self.dirt = None
        self.tunnels = None
        self.reset()
        self.generate()

    def reset(self):
        '''Clear all tunnels, fill everything with dirt.'''
        self.dirt = []
        self.tunnels = []
        for i in xrange(self.dim[0]/SIZE):
            self.dirt.append([])
            for j in xrange(self.dim[1]/SIZE):
                self.dirt[-1].append(False)

    def generate(self, pos=None, direct=None, distance=0):
        '''Generate tunnels.
        
        When generating a new formicarium, don't give the `pos', `direct' or `distance' arguments.
        These are used when this function recursively calls itself to generate additional tunnels.'''
        if not pos: # generating a new formicarium
            num = 1
            while random.randrange(num) < TUNNELS and num < 2*TUNNELS: # create at least TUNNELS tunnels, at most 2*TUNNELS
                num += 1
                if not random.randrange(2) and any(self.tunnels): # fork an existing tunnel
                    pos = None
                    while not pos:
                        #pos = self.tunnels[random.randrange(len(self.tunnels))]
                        pos = random.choice(self.tunnels)
                        distance = random.randrange(DISTANCE) if DISTANCE else 0 # the fork has already gone some distance
                else: # start a tunnel at the top
                    pos = random.randrange(0, self.dim[0]/SIZE), 0
                d = random.randrange(6)
                self.generate(pos, d, distance)
        else: # generating a tunnel
            distance += 1
            if self.tunnels and self.tunnels[-1] == None: # first block of a tunnel
                self.tunnels.append(pos)
            oldpos = pos
            pos = self.topos(pos, direct)
            if pos[0] >= 0 and pos[0] < self.dim[0]/SIZE and pos[1] >= 0 and pos[1] < self.dim[1]/SIZE and not self.dirt[pos[0]][pos[1]] and (not DISTANCE or (random.randrange(distance) < DISTANCE and distance < 2*DISTANCE)): # tunnel not out of screen and tunnel not too long
                self.tunnels.append(pos)
                directs = set()
                direct = self.new_direct(direct)
                directs.add(direct)
                self.generate(pos, direct, distance+1)
                if not random.randrange(16): # fork
                    direct = (direct + 3) % 6
                    self.generate(pos, direct, distance)
            else: # end of a tunnel
                self.tunnels.append(None)
        last = None
        for t in self.tunnels: # generate bool field
            if last and t:
                self.line(last, t)
            last = t

    def mask(self):
        '''Returns a Mask representing the formicarium.

        The mask is drawn by Formicarium.draw, so it has the same shape as a surface drawn by that method.
        Note: did not test'''
        surf = pygame.Surface(self.dim)
        self.draw(surf, pygame.Color(0, 0, 0, 0), pygame.Color(0, 0, 0, 255))
        return pygame.mask.from_surface(surf)

    def line(self, p1, p2):
        '''Use Bresenham line algorithm to draw a line from p1 to p2 into the bool field'''
        x0, y0 = p1
        x1, y1 = p2
        dx = abs(x1 - x0)
        dy = abs(y1 - y0) 
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if x0 < 0 or x0 >= self.dim[0]/SIZE or y0 < 0 or y0 >= self.dim[1]/SIZE:
                break
            self.dirt[x0][y0] = True
            if x0 == x1 and y0 == y1:
                break  
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy 

    def new_direct(self, direct):
        '''Switch a direction of the tunnel.
        
        At the moment, it only vertically inverts it with 1/8 chance.'''
        if not random.randrange(8):
            direct = (direct + 3) % 6
        return direct

    def topos(self, pos, direct):
        '''Return a new position based on `pos' (point) and the `direct' direction (0-5 int)'''
        l = [
            (1, -1),
            (1, 1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (-1, 1),
        ]
        return pos[0] + l[direct][0]*random.randrange(1, MOVE), pos[1] + l[direct][1]*random.randrange(1, MOVE) # moves for between 1 and MOVE in a direction based on direct

    def draw(self, surf=None, dirt=DIRT, air=AIR):
        '''Draws the formicarium on the surface using circles.
        
        If `surf' argument is given, it draws to that surface instead of `self.surf'.
        If `dirt' or `air' arguments are given, it uses these colors for dirt/air.'''
        if surf is None:
            surf = self.surf
        surf.fill(dirt)
        for i in xrange(self.dim[0]/SIZE):
            for j in xrange(self.dim[1]/SIZE):
                if self.dirt[i][j]:
                    rect = i*SIZE - SIZE/4, j*SIZE - SIZE/4, SIZE + SIZE/2, SIZE + SIZE/2
                    #surf.fill(air, rect)
                    pygame.draw.circle(surf, air, (rect[0]+SIZE/2, rect[1]+SIZE/2), SIZE/2 + SIZE/4)
                    pygame.draw.circle(surf, air, (rect[0]+SIZE/2, rect[1]+SIZE/2+SIZE/4), SIZE/2 + SIZE/4)
                    pygame.draw.circle(surf, air, (rect[0]+SIZE/2+SIZE/4, rect[1]+SIZE/2), SIZE/2 + SIZE/4)
                    pygame.draw.circle(surf, air, (rect[0]+SIZE/2+SIZE/4, rect[1]+SIZE/2+SIZE/4), SIZE/2 + SIZE/4)

    def draw_lines(self, width=SIZE*2, surf=None):
        '''Draws the formicarium on the surface using lines.

        `width' argument is the width of the lines.
        If `surf' argument is given, it draws to that surface instead of `self.surf'.'''
        if surf is None:
            surf = self.surf
        surf.fill(DIRT)
        lines = []
        for t in self.tunnels:
            if t:
                lines.append((t[0] * SIZE, t[1] * SIZE))
            else:
                if len(lines) > 1:
                    pygame.draw.lines(surf, AIR, False, lines, width)
                lines = []

if __name__ == '__main__': #test
    def main():
        '''Draw an example formicarium'''
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        f = Formicarium(screen)
        f.draw_lines(1)
        pygame.display.flip()
        ok = 0
        c = pygame.time.Clock()
        while True:
            c.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYUP:
                    if ok:
                        if ok == 2:
                            #pygame.image.save(screen, 'f4.png')
                            return
                        f.draw()
                        pygame.display.flip()
                        ok = True
                        ok += 1
                    else:
                        f.draw_lines()
                        pygame.display.flip()
                        ok += 1
    main()
