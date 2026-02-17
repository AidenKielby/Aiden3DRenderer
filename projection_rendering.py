import pygame
from pygame import *
import sys
from math import *
import numpy

focal_length = 5

#top right
z1 = -2
#top right back
z2 = -4
#bottom right
z3 = -2
#bottom right back
z4 = -4
#top left
z5 = -2
#top left back
z6 = -4
#bottom left
z7 = -2
#bottom left back
z8 = -4

zlist = [z1, z2, z3, z4, z5, z6, z7, z8]
zlistlen = len(zlist)

#top right
y1 = 2
#top right back
y2 = 2
#bottom right
y3 = -2
#bottom right back
y4 = -2
#top left
y5 = 2
#top left back
y6 = 2
#bottom left
y7 = -2
#bottom left back
y8 = -2

ylist = [y1, y2, y3, y4, y5, y6, y7, y8]
ylistlen = len(ylist)

#top right
x1 = 2
#top right back
x2 = 2
#bottom right
x3 = 2
#bottom right back
x4 = 2
#top left
x5 = -2
#top left back
x6 = -2
#bottom left
x7 = -2
#bottom left back
x8 = -2

xlist = [x1, x2, x3, x4, x5, x6, x7, x8]

angle = 0

umlist = []
zrotlist = []
yrotlist = []
finmatrix = []


    

print(finmatrix)
print(umlist)

pygame.init()
screen = pygame.display.set_mode((1300, 1300))
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    
    clock.tick(60)



    xprojected1 = (((focal_length*x1)/(focal_length+z1)) + 100)*10
    xprojected2 = (((focal_length*x2)/(focal_length+z2)) + 100)*10
    xprojected3 = (((focal_length*x3)/(focal_length+z3)) + 100)*10
    xprojected4 = (((focal_length*x4)/(focal_length+z4)) + 100)*10
    xprojected5 = (((focal_length*x5)/(focal_length+z5)) + 100)*10
    xprojected6 = (((focal_length*x6)/(focal_length+z6)) + 100)*10
    xprojected7 = (((focal_length*x7)/(focal_length+z7)) + 100)*10
    xprojected8 = (((focal_length*x8)/(focal_length+z8)) + 100)*10

    yprojected1 = (((focal_length*y1)/(focal_length+z1)) + 100)*10
    yprojected2 = (((focal_length*y2)/(focal_length+z2)) + 100)*10
    yprojected3 = (((focal_length*y3)/(focal_length+z3)) + 100)*10
    yprojected4 = (((focal_length*y4)/(focal_length+z4)) + 100)*10
    yprojected5 = (((focal_length*y5)/(focal_length+z5)) + 100)*10
    yprojected6 = (((focal_length*y6)/(focal_length+z6)) + 100)*10
    yprojected7 = (((focal_length*y7)/(focal_length+z7)) + 100)*10
    yprojected8 = (((focal_length*y8)/(focal_length+z8)) + 100)*10

    rotatin_matrix = [
        [cos(angle),sin(angle)],
        [-sin(angle),cos(angle)]
    ]

    for o in range(8):
        for zrot in range(zlistlen):
            zplace = zlist[zrot]
            yorz = len(rotatin_matrix[1])
            yrotz = rotatin_matrix[1]
            for rot in range(yorz):
                wtby = yrotz[rot]
                zmult = zplace * wtby
                zrotlist.append(zmult)

        for yrot in range(ylistlen):
            yplace = ylist[yrot]
            yory = len(rotatin_matrix[0])
            yroty = rotatin_matrix[0]
            for rot in range(yory):
                wtby = yroty[rot]
                ymult = zplace * wtby
                yrotlist.append(zmult)

    for i in range (8):
        xpro = (((focal_length*xlist[i])/(focal_length+zrotlist[i])) + 100) *10
        ypro = (((focal_length*yrotlist[i])/(focal_length+zrotlist[i])) + 100)*10
        print("xpro")
        print(xpro)
        print("ypro")
        print(ypro)
        pygame.draw.circle(screen, (0,0,0), (xpro,ypro),5)

    angle += 1
    pygame.display.update()
    #break
