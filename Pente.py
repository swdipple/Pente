import pygame as pg
import numpy as np
pg.init()

xsize=500
ysize=500
gridsize=50

win=pg.display.set_mode((xsize,ysize))
pg.display.set_caption("Pente: by Stephen")

def background(win):
    i=gridsize
    while(i<xsize):
        pg.draw.line(win,(0,0,0), (i,0),(i,ysize))
        i+=gridsize
    i=gridsize
    while(i<ysize):
        pg.draw.line(win,(0,0,0), (0,i),(xsize,i))
        i+=gridsize

circ_loc=np.zeros((0,2))
x=50
y=50
width=40
height=60
vel=5

run=True
while run:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        elif event.type==pg.MOUSEBUTTONUP:
            pos=np.array(pg.mouse.get_pos())
            test=True
            if(pos[0]<gridsize/2 or pos[0]>xsize-gridsize/2 or pos[1]<gridsize/2 or pos[1]>ysize-gridsize/2):
                test=False
            remainder=pos[0]%gridsize
            if(remainder<gridsize/2):
                pos[0]-=remainder
            else:
                pos[0]+=gridsize-remainder
            remainder=pos[1]%gridsize
            if(remainder<gridsize/2):
                pos[1]-=remainder
            else:
                pos[1]+=gridsize-remainder
            i=0
            while(i<len(circ_loc[:,0]) and test):
                if(circ_loc[i,0]==pos[0] and circ_loc[i,1]==pos[1]):
                    test=False
                i+=1
            if(test):
                circ_loc=np.append(circ_loc,np.array([pos]),axis=0)

    keys=pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        x-=vel
    if keys[pg.K_RIGHT]:
        x+=vel
    if keys[pg.K_UP]:
        y-=vel
    if keys[pg.K_DOWN]:
        y+=vel

    win.fill((255,255,255))
    background(win)

    i=0
    while(i<len(circ_loc[:,0])):
        pg.draw.circle(win,(0,0,255),circ_loc[i,:],gridsize/3)
        i+=1
    pg.display.update()
pg.quit()