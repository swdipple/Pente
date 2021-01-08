import pygame as pg
import numpy as np
pg.init()

xsize=500
ysize=500
gridsize=50

win=pg.display.set_mode((xsize,ysize+gridsize))
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
    pg.draw.line(win,(0,0,0), (0,ysize),(xsize,ysize))

def removal_check(move,p1,p2):
    i=0
    out=0
    cross=np.array([[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]])
    cross*=gridsize
    while(i<len(p1[:,0])):
        k=0
        while(k<len(cross[:,0])):
            if(p1[i,0]+3*cross[k,0]==move[0] and p1[i,1]+3*cross[k,1]==move[1]):
                j=0
                test=0
                loc=np.zeros(2,dtype=int)
                while(j<len(p2[:,0]) and test!=2):
                    if(p2[j,0]+2*cross[k,0]==move[0] and p2[j,1]+2*cross[k,1]==move[1]) or (p2[j,0]+cross[k,0]==move[0] and p2[j,1]+cross[k,1]==move[1]):
                        loc[test]=j
                        test+=1
                    j+=1
                if(test==2):
                    p2=np.delete(p2,loc[1],axis=0)
                    p2=np.delete(p2,loc[0],axis=0)
                    out+=1
            k+=1
        i+=1
    return p2,out

def register_move(move,red,blue,taken,isred,over):
    
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
    while(i<len(red[:,0]) and test):
        if(red[i,0]==pos[0] and red[i,1]==pos[1]):
            test=False
            break
        i+=1
    i=0
    while(i<len(blue[:,0]) and test):
        if(blue[i,0]==pos[0] and blue[i,1]==pos[1]):
            test=False
            break
        i+=1
    if(test):
        if(isred):
            blue,out=removal_check(pos,red,blue)
            taken[0]+=out
            red=np.append(red,np.array([pos]),axis=0)
            isred=False
        else:
            red,out=removal_check(pos,blue,red)
            taken[1]+=out
            blue=np.append(blue,np.array([pos]),axis=0)
            isred=True
    if(taken[0]>=5):
        over+=1
    if(taken[1]>=5):
        over+=2
    return red,blue,taken,isred,over



red=np.zeros((0,2))
blue=np.zeros((0,2))
isred=True
taken=np.zeros(2,dtype=int)
over=0

run=True
while run:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        elif event.type==pg.MOUSEBUTTONUP:
            pos=np.array(pg.mouse.get_pos())
            red,blue,taken,isred,over=register_move(pos,red,blue,taken,isred,over)


    win.fill((255,255,255))
    background(win)
    font=pg.font.Font('freesansbold.ttf',32)
    text=font.render(str(taken[1]),True,(255,0,0),(255,255,255))
    textRect=text.get_rect()
    textRect.center=(3*xsize/4,ysize+gridsize/2)
    win.blit(text,textRect)
    font=pg.font.Font('freesansbold.ttf',32)
    text=font.render(str(taken[0]),True,(0,0,255),(255,255,255))
    textRect=text.get_rect()
    textRect.center=(xsize/4,ysize+gridsize/2)
    win.blit(text,textRect)


    i=0
    while(i<len(red[:,0])):
        pg.draw.circle(win,(0,0,255),red[i,:],gridsize/3)
        i+=1
    i=0
    while(i<len(blue[:,0])):
        pg.draw.circle(win,(255,0,0),blue[i,:],gridsize/3)
        i+=1
    if(over==2):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Red Wins',True,(0,0,255),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        run=False
    elif(over==1):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Blue Wins',True,(255,0,0),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        run=False
    elif(over>2):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Tie',True,(0,0,0),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        run=False
    pg.display.update()
pg.time.delay(5000)
pg.quit()