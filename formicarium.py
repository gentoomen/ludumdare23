import pygame
import random

DIRT = pygame.Color(150, 50, 0) # dirt color
AIR = pygame.Color(250, 150, 100) # tunnel color
SIZE = 8 # tunnel size
TUNNELS = 10 # increase for more tunnels
DISTANCE = 128 # increase for longer tunnels, 0 to disable
MOVE = 8 # how much tunnel to generate at once in one direction

class Formicarium(object):
    def __init__(self, surf):
        self.surf = surf
        self.dim = surf.get_size()
        self.dirt = None
        self.tunnels = None
        self.reset()
        self.generate()

    def reset(self):
        self.dirt = []
        self.tunnels = []
        for i in xrange(self.dim[0]/SIZE):
            self.dirt.append([])
            for j in xrange(self.dim[1]/SIZE):
                self.dirt[-1].append(False)

    def generate(self, pos=None, direct=None, distance=0):
        if not pos:
            num = 1
            while random.randrange(num) < TUNNELS:
                num += 1
                if not random.randrange(2) and self.tunnels and any(self.tunnels):
                    pos = None
                    while not pos:
                        pos = self.tunnels[random.randrange(len(self.tunnels))]
                        distance = random.randrange(DISTANCE)
                else:
                    pos = random.randrange(0, self.dim[0]/SIZE), 0 #random.randrange(0, self.dim[1]/SIZE)
                d = random.randrange(6)
                self.generate(pos, d, distance)
        else:
            distance += 1
            if self.tunnels and self.tunnels[-1] == None:
                self.tunnels.append(pos)
            oldpos = pos
            pos = self.topos(pos, direct)
            if pos[0] >= 0 and pos[0] < self.dim[0]/SIZE and pos[1] >= 0 and pos[1] < self.dim[1]/SIZE and not self.dirt[pos[0]][pos[1]] and (random.randrange(distance) < DISTANCE or not DISTANCE):
                self.tunnels.append(pos)
                directs = set()
                direct = self.new_direct(direct)
                directs.add(direct)
                self.generate(pos, direct, distance+1)
                if not random.randrange(16):
                    direct = (direct + 3) % 6
                    self.generate(pos, direct, distance)
            else:
                self.tunnels.append(None)
        last = None
        for t in self.tunnels:
            if last and t:
                self.line(last, t)
            last = t

    def line(self, p1, p2):
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
        #if direct in (1, 4):
        #    direct += random.choice((-1, 0, 0, 0, 1))
        if not random.randrange(8):
            direct = (direct + 3) % 6
        return direct

    def topos(self, pos, direct):
        l = [
            (1, -1),
            (1, 1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (-1, 1),
        ]
        return pos[0] + l[direct][0]*random.randrange(1, MOVE), pos[1] + l[direct][1]*random.randrange(1, MOVE)

    def draw(self):
        self.surf.fill(DIRT)
        for i in xrange(self.dim[0]/SIZE):
            for j in xrange(self.dim[1]/SIZE):
                if self.dirt[i][j]:
                    rect = i*SIZE - SIZE/4, j*SIZE - SIZE/4, SIZE + SIZE/2, SIZE + SIZE/2
                    #self.surf.fill(AIR, rect)
                    pygame.draw.circle(self.surf, AIR, (rect[0]+SIZE/2, rect[1]+SIZE/2), SIZE/2 + SIZE/4)
                    pygame.draw.circle(self.surf, AIR, (rect[0]+SIZE/2, rect[1]+SIZE/2+SIZE/4), SIZE/2 + SIZE/4)
                    pygame.draw.circle(self.surf, AIR, (rect[0]+SIZE/2+SIZE/4, rect[1]+SIZE/2), SIZE/2 + SIZE/4)
                    pygame.draw.circle(self.surf, AIR, (rect[0]+SIZE/2+SIZE/4, rect[1]+SIZE/2+SIZE/4), SIZE/2 + SIZE/4)

    def draw_lines(self, width=SIZE*2):
        self.surf.fill(DIRT)
        lines = []
        for t in self.tunnels:
            if t:
                lines.append((t[0] * SIZE, t[1] * SIZE))
            else:
                if len(lines) > 1:
                    pygame.draw.lines(self.surf, AIR, False, lines, width)
                lines = []

if __name__ == '__main__': #test
    def main():
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
