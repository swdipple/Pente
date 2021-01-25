import pygame as pg
import numpy as np
pg.init()

ss=500
num_squares=10
gridsize=int(ss/num_squares)
xsize=ss
ysize=ss
cross=np.array([[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]])
check=np.array([[-1,-1],[-1,-1]])



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

def removal_check(move,board,isred):
    '''
    Looks to see if move would result in the removal of two peices
    If a removal would happen, the two peices that are removed are returned
    else an array of -1 is returned
    '''

    i=0
    out=np.zeros((2,2),dtype=int)-1

    
    while(i<len(cross[:,0])):
        if(move[0]+3*cross[i,0]>=0 and move[0]+3*cross[i,0]<len(board[0,:]) and move[1]+3*cross[i,1]>=0 and move[1]+3*cross[i,1]<len(board[:,0])):
            if(board[move[0]+3*cross[i,0],move[1]+3*cross[i,1]]==int(isred)+1):
                if(board[move[0]+2*cross[i,0],move[1]+2*cross[i,1]]==2-int(isred) and board[move[0]+cross[i,0],move[1]+cross[i,1]]==2-int(isred)):
                    out[0,0]=move[0]+2*cross[i,0]
                    out[0,1]=move[1]+2*cross[i,1]
                    out[1,0]=move[0]+cross[i,0]
                    out[1,1]=move[1]+cross[i,1]
                    return out
        i+=1
    return out


def check_seq(board,move,isred,length):
    
    '''
    returns 0,-1 if no sequence of designated length was found, returns color,direction if a sequence is found
    '''
    
    i=0
    while(i<len(cross[:,0])):
        j=1
        while(True):
            if(move[0]+j*cross[i,0]<0 or move[0]+j*cross[i,0]>=len(board[0,:]) or move[1]+j*cross[i,1]<0 or move[1]+j*cross[i,1]>=len(board[:,0])):
                break
            else:
                if(board[move[0]+j*cross[i,0],move[1]+j*cross[i,1]]!=int(isred)+1):
                    break
                elif(j==length-1):
                    return int(isred)+1,i
                else:
                    j+=1
        k=-1
        while(True):
            if(move[0]+k*cross[i,0]<0 or move[0]+k*cross[i,0]>=len(board[0,:]) or move[1]+k*cross[i,1]<0 or move[1]+k*cross[i,1]>=len(board[:,0])):
                break
            else:
                if(board[move[0]+k*cross[i,0],move[1]+k*cross[i,1]]!=int(isred)+1):
                    break
                elif(j-k==length):
                    return int(isred)+1,i
                else:
                    k-=1
        i+=1
    return 0,-1

def register_move(move,board,taken,isred,over):
    
    test=True
    if(move[0]<gridsize/2 or move[0]>xsize-gridsize/2 or move[1]<gridsize/2 or move[1]>ysize-gridsize/2):
        return isred,over,False
    remainder=move[0]%gridsize
    if(remainder<gridsize/2):
        move[0]-=remainder
    else:
        move[0]+=gridsize-remainder
    move[0]/=gridsize
    move[0]-=1
    remainder=move[1]%gridsize
    if(remainder<gridsize/2):
        move[1]-=remainder
    else:
        move[1]+=gridsize-remainder
    move[1]/=gridsize
    move[1]-=1
    print(move)
    if(board[move[0],move[1]]==0):
        out=removal_check(move,board,isred)
        while((out!=check).all()):
            board[out[0,0],out[0,1]]=0
            board[out[1,0],out[1,1]]=0
            taken[int(isred)]+=1
            out=removal_check(move,board,isred)
        board[move[0],move[1]]=int(isred)+1
        if(taken[int(isred)]>=5):
            over+=int(isred) +1
        else:
            t1,t2=check_seq(board,move,isred,5)
            over+=t1
        isred=not isred
        return isred,over,True
    else:
        return isred,over,False

def check_autowin(board,taken,isred):

    '''
    Checks if there is any move the inputed color can take that will result in a win
    Returns position of that move is one exists, -1,-1 else
    '''
    alt=np.zeros((0,2),dtype=int)
    i=0
    while(i<len(board[:,0])):
        j=0
        while(j<len(board[0,:])):
            if(board[i,j]==0):

                if(taken[int(isred)]==4):
                    out=removal_check(np.array([i,j]),board,isred)
                    if((out!=check).all()):
                        return i,j

                t1,t2=check_seq(board,np.array([i,j]),isred,5)
                if(t1>0):
                    return i,j
                t1,t2=check_seq(board,np.array([i,j]),isred,4)
                if(t1>0):
                    k=1
                    forward=True
                    while(True):
                        if not (i+k*cross[t2,0]>=0 and 
                           i+k*cross[t2,0]<len(board[:,0]) and 
                           j+k*cross[t2,1]>=0 and 
                           j+k*cross[t2,1]<len(board[0,:])):
                            forward=False
                            break
                        if(board[i+k*cross[t2,0],j+k*cross[t2,1]]==int(not isred)+1):
                            forward=False
                            break
                        elif(board[i+k*cross[t2,0],j+k*cross[t2,1]]==0):
                            break
                        k+=1
                    k=1
                    while(True):
                        if not (i-k*cross[t2,0]>=0 and 
                           i-k*cross[t2,0]<len(board[:,0]) and 
                           j-k*cross[t2,1]>=0 and 
                           j-k*cross[t2,1]<len(board[0,:])):
                            forward=False
                            break
                        if(board[i-k*cross[t2,0],j-k*cross[t2,1]]==int(not isred)+1):
                            forward=False
                            break
                        elif(board[i-k*cross[t2,0],j-k*cross[t2,1]]==0):
                            break
                        k+=1
                    if(forward):
                        alt=np.append(alt,np.array([[i,j]]),axis=0)
            j+=1
        i+=1
    if(len(alt[:,0])>0):
        return alt[0,:]
    return -1,-1
    


def ai1_move(board,taken,isred):

    #auto win moves
    i,j=check_autowin(board,taken,isred)
    if(i!=-1):
        return np.array([i,j])

    #prevent auto lose moves
    autolose=np.zeros((0,2),dtype=int)
    allowed=np.zeros((0,2),dtype=int)
    i=0
    while(i<len(board[:,0])):
        j=0
        while(j<len(board[0,:])):
            if(board[i,j]==0):
                tboard=np.copy(board)
                tboard[i,j]=int(isred)+1
                k,l=check_autowin(tboard,taken,not isred)
                if(k!=-1):
                    autolose=np.append(autolose,np.array([[i,j]]),axis=0)
                else:
                    allowed=np.append(allowed,np.array([[i,j]]),axis=0)
            j+=1
        i+=1
    if(len(allowed[:,0])==1):
        return allowed[0,:]

    

    i=0
    while(i<len(allowed[:,0])):
        #print(allowed[i,:])
        t1,t2=check_seq(board,allowed[i,:],isred,4)
        if(t1!=0):
            forward=0
            j=1
            #print(allowed[i,0]+j*cross[t2,0],allowed[i,1]+j*cross[t2,1],'j')
            
            while(allowed[i,0]+j*cross[t2,0]>=0 and 
                  allowed[i,0]+j*cross[t2,0]<len(board[:,0]) and 
                  allowed[i,1]+j*cross[t2,1]>=0 and 
                  allowed[i,1]+j*cross[t2,1]<len(board[0,:])):
                if((board[allowed[i,0]+j*cross[t2,0],allowed[i,1]+j*cross[t2,1]]==0 and j==1) or
                   (board[allowed[i,0]+j*cross[t2,0],allowed[i,1]+j*cross[t2,1]]==0 and board[allowed[i,0]+(j-1)*cross[t2,0],allowed[i,1]+(j-1)*cross[t2,1]]==int(isred)+1)):
                    forward+=1
                    break
                elif(board[allowed[i,0]+j*cross[t2,0],allowed[i,1]+j*cross[t2,1]]!=int(isred)+1):
                    break
                    
                j+=1
                #print(allowed[i,0]+j*cross[t2,0],allowed[i,1]+j*cross[t2,1],'j')
            j-=1

            k=1
            #print(allowed[i,0]-k*cross[t2,0],allowed[i,1]-k*cross[t2,1],'k')
            while(allowed[i,0]-k*cross[t2,0]>=0 and 
                  allowed[i,0]-k*cross[t2,0]<len(board[:,0]) and 
                  allowed[i,1]-k*cross[t2,1]>=0 and 
                  allowed[i,1]-k*cross[t2,1]<len(board[0,:]) and 
                  forward):
                if((board[allowed[i,0]-k*cross[t2,0],allowed[i,1]-k*cross[t2,1]]==0 and k==1) or
                   (board[allowed[i,0]-k*cross[t2,0],allowed[i,1]-k*cross[t2,1]]==0 and board[allowed[i,0]-(k-1)*cross[t2,0],allowed[i,1]-(k-1)*cross[t2,1]]==int(isred)+1)):
                    forward+=1
                    break
                elif (board[allowed[i,0]-k*cross[t2,0],allowed[i,1]-k*cross[t2,1]]!=int(isred)+1):
                    break
                k+=1
                #print(allowed[i,0]-k*cross[t2,0],allowed[i,1]-k*cross[t2,1],'k')
            k-=1
                
            #print(forward,j,k)
            if(forward==2):
                return allowed[i,:]
        i+=1
    removal_moves=np.zeros((0,2),dtype=int)
    i=0
    while(i<len(allowed[:,0])):
        out=removal_check(allowed[i,:],board,isred)
        if(out[0,0]!=-1):
            removal_moves=np.append(removal_moves,np.reshape(allowed[i,:],(-1,2)),axis=0)
        i+=1
    if(len(removal_moves[:,0])>0):
        return removal_moves[np.random.randint(0,len(removal_moves[:,0])),:]
    
    if(len(allowed[:,0])==0):
        i=0
        while(i<len(board[:,0])):
            j=0
            while(j<len(board[0,:])):
                if(board[i,j]==0):
                    return np.array([i,j])
                j+=1
            i+=1

    i=len(allowed[:,0])-1
    while(i>=0):
        tboard=np.copy(board)
        tboard[allowed[i,0],allowed[i,1]]=int(isred)+1
        j=0
        while(j<len(cross[:,0])):
            if(allowed[i,0]+cross[j,0]>=0 and 
               allowed[i,0]+cross[j,0]<len(board[:,0]) and 
               allowed[i,1]+cross[j,1]>=0 and 
               allowed[i,1]+cross[j,1]<len(board[0,:])):
                out=removal_check([allowed[i,0]+cross[j,0],allowed[i,1]+cross[j,1]],tboard,not isred)
                if(out[0,0]!=-1):
                    allowed=np.delete(allowed,i,0)
                    break
            j+=1
        i-=1
    good_moves=np.zeros((0,2),dtype=int)
    i=0
    while(i<len(allowed[:,0])):
        j=0
        while(j<len(cross[:,0])):
            if(allowed[i,0]+cross[j,0]>=0 and 
               allowed[i,0]+cross[j,0]<len(board[:,0]) and 
               allowed[i,1]+cross[j,1]>=0 and 
               allowed[i,1]+cross[j,1]<len(board[0,:])):
                if(board[allowed[i,0]+cross[j,0],allowed[i,1]+cross[j,1]]==int(isred)+1):
                    good_moves=np.append(good_moves,np.reshape(allowed[i,:],(-1,2)),axis=0)
                elif(allowed[i,0]+2*cross[j,0]>=0 and 
                     allowed[i,0]+2*cross[j,0]<len(board[:,0]) and 
                     allowed[i,1]+2*cross[j,1]>=0 and 
                     allowed[i,1]+2*cross[j,1]<len(board[0,:])):
                    if(board[allowed[i,0]+cross[j,0],allowed[i,1]+cross[j,1]]==int(not isred)+1 and
                     board[allowed[i,0]+2*cross[j,0],allowed[i,1]+2*cross[j,1]]==int(not isred)+1):
                        good_moves=np.append(good_moves,np.reshape(allowed[i,:],(-1,2)),axis=0)
            j+=1
        i+=1
    if(len(good_moves)>0):
        return good_moves[np.random.randint(0,len(good_moves[:,0])),:]

    i=0
    while(i<len(allowed[:,0])):
        j=0
        while(j<len(cross[:,0])):
            if(allowed[i,0]+cross[j,0]>=0 and 
               allowed[i,0]+cross[j,0]<len(board[:,0]) and 
               allowed[i,1]+cross[j,1]>=0 and 
               allowed[i,1]+cross[j,1]<len(board[0,:])):
                if(board[allowed[i,0]+cross[j,0],allowed[i,1]+cross[j,1]]!=0):
                    good_moves=np.append(good_moves,np.reshape(allowed[i,:],(-1,2)),axis=0)
            j+=1
        i+=1
    if(len(good_moves)>0):
        return good_moves[np.random.randint(0,len(good_moves[:,0])),:]

    if(board[int(len(board[:,0])/2),int(len(board[0,:])/2)]==0):
        return np.array([int(len(board[:,0])/2),int(len(board[0,:])/2)])

    i=0
    while(i<len(board[:,0])):
        j=0
        while(j<len(board[0,:])):
            if(board[i,j]==0):
                return np.array([i,j])
            j+=1
        i+=1


    

        












#piece position empty=0 blue=1 red=2
board=np.zeros((int(xsize/gridsize-1),int(ysize/gridsize-1)),dtype=int)
#for True red moves first
isred=True
#number of pieces taken, index 0 for blue, index 1 for red
taken=np.zeros(2,dtype=int)
over=0






#board[0,3]=1
#board[0,4]=1
#board[0,2]=1
#board[0,4]=1
#board[0,0]=1
#print(check_autowin(board,taken,False))
#print(ai1_move(board,[0,0],True))

#exit(0)

run=True
while run:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        elif event.type==pg.MOUSEBUTTONUP:
            pos=np.array(pg.mouse.get_pos())
            #print(pos)
            isred,over,move_registered=register_move(pos,board,taken,isred,over)
            new_pos=(ai1_move(board,taken,isred)+1)*gridsize
            #print(new_pos)
            if(over==0 and move_registered):
                isred,over,move_registered=register_move(new_pos,board,taken,isred,over)
            print(board)


    win.fill((255,255,255))
    background(win)
    font=pg.font.Font('freesansbold.ttf',32)
    text=font.render(str(taken[0]),True,(255,0,0),(255,255,255))
    textRect=text.get_rect()
    textRect.center=(3*xsize/4,ysize+gridsize/2)
    win.blit(text,textRect)
    font=pg.font.Font('freesansbold.ttf',32)
    text=font.render(str(taken[1]),True,(0,0,255),(255,255,255))
    textRect=text.get_rect()
    textRect.center=(xsize/4,ysize+gridsize/2)
    win.blit(text,textRect)
    if(over==0):
        if(isred):
            font=pg.font.Font('freesansbold.ttf',32)
            text=font.render('Blue Move',True,(0,0,0),(255,255,255))
            textRect=text.get_rect()
            textRect.center=(xsize/2,ysize+gridsize/2)
            win.blit(text,textRect)
        else:
            font=pg.font.Font('freesansbold.ttf',32)
            text=font.render('Red Move',True,(0,0,0),(255,255,255))
            textRect=text.get_rect()
            textRect.center=(xsize/2,ysize+gridsize/2)
            win.blit(text,textRect)

    i=0
    while(i<len(board[:,0])):
        j=0
        while(j<len(board[0,:])):
            if(board[i,j]==2):
                pg.draw.circle(win,(0,0,255),((i+1)*gridsize,(j+1)*gridsize),gridsize/3)
            elif(board[i,j]==1):
                pg.draw.circle(win,(255,0,0),((i+1)*gridsize,(j+1)*gridsize),gridsize/3)
            j+=1
        i+=1
    if(over==2):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Blue Wins',True,(0,0,255),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        pg.display.update()
        pg.time.delay(3000)
        run=False
    elif(over==1):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Red Wins',True,(255,0,0),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        pg.display.update()
        pg.time.delay(3000)
        run=False
    elif(over>2):
        font=pg.font.Font('freesansbold.ttf',32)
        text=font.render('Tie',True,(0,0,0),(255,255,255))
        textRect=text.get_rect()
        textRect.center=(xsize/2,ysize+gridsize/2)
        win.blit(text,textRect)
        pg.display.update()
        pg.time.delay(3000)
        run=False
    else:
        pg.display.update()


pg.quit()