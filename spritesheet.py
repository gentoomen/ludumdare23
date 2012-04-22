#!/usr/bin/python

import getopt
import os
import pygame
import sys

num = None
width = None
height = None
filename = None

try:
    usage = 'Usage: %s -w SPRITE_WIDTH -h SPRITE_HEIGHT -n NUMBER_OF_FRAMES FILE_NAME' % os.path.basename(sys.argv[0])
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'w:h:n:', ['width=', 'height=', 'num='])
    for o, a in opts:
        if o in ('-w', '--width'):
            width = int(a)
        elif o in ('-h', '--height'):
            height = int(a)
        elif o in ('-n', '--num'):
            num = int(a)
    if not width or not num or not height:
        raise Exception('missing parameters')
    if len(args) != 1:
        raise Exception('missing filename')
    filename = args[0]
except Exception as e:
    print >> sys.stderr, '%s:' % os.path.basename(sys.argv[0]), e
    print >> sys.stderr, usage
    sys.exit(2)

pygame.init()
surf = pygame.Surface(((num*(width+1)), height))
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
surf.fill(white)
for i in xrange(num-1):
    pygame.draw.line(surf, black, ((width)*(i+1) + i, 0), ((width)*(i+1) + i, height))
pygame.image.save(surf, filename)
