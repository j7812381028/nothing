import pygame, random, sys
from pygame.locals import *

width=1366
height=768

BLACK=(0,0,0)
WHITE=(255,255,255)
MIXER=(234,78,34)

fps=60

treemaxsize=100
treeminsize=10
coinmaxsize=30
coinminsize=30
treespeed=5
treespawnrate=18
playerspeed=5
coinspawnrate=100

def terminate():
    pygame.quit()
    sys.exit()
def detectkeypress():
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            if event.type==KEYDOWN:    
                if event.key==K_ESCAPE:
                    terminate()
                return
def hitler(playerrect,trees):
    for t in trees:
        if playerrect.colliderect(t['rect']):
            return True
        return False

def eat(playerrect,foods):
    for f in foods:
        if playerrect.colliderect(f['rect']):
            foods.remove(f)
            return True
        return False


def drawtext(text,font,surface,x,y):
    textobj=font.render(text,1,BLACK)
    textrect=textobj.get_rect()
    textrect.topleft=(x,y)
    surface.blit(textobj,textrect)
    

pygame.init()
mainClock=pygame.time.Clock()
windowsurface=pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption('skitree')
pygame.mouse.set_visible(False)


font=pygame.font.SysFont(None,48)


gameoversound=pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
pickupsound=pygame.mixer.Sound('pickup.wav')


playerimage=pygame.image.load('MARIO2.png')
playerrect=playerimage.get_rect()
treeimage=pygame.image.load('Mushroom2.png')
foodimage=pygame.image.load('coin.png')
windowsurface.fill(WHITE)


drawtext('skitree',font,windowsurface,width/3,height/3)
drawtext('press any key to start',font,windowsurface,width/3,height/3+50)

pygame.display.update()
detectkeypress()


topscore=0
while True:
    trees=[]
    foods=[]
    score=0
    playerrect.topleft=(width/2,height-50)
    moveleft=moveright=moveup=movedown=False
    treecounter=0
    foodcounter=0
    print(123)
    pygame.mixer.music.play(-1,0.0)
    while True:
        score+=1
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                    if event.key==K_LEFT or event.key==K_a:
                        moveright=False
                        moveleft=True
                    if event.key==K_RIGHT or event.key==K_d:
                        moveleft=False
                        moveright=True
                    if event.key==K_UP or event.key==K_w:
                        movedown=False
                        moveup=True
                    if event.key==K_DOWN or event.key==K_s:
                        movedown=True
                        moveup=False
            if event.type==KEYUP:
                if event.key==K_LEFT or event.key==K_a:
                    moveleft=False
                if event.key==K_RIGHT or event.key==K_d:
                    moveright=False
                if event.key==K_UP or event.key==K_w:
                    moveup=False
                if event.key==K_DOWN or event.key==K_s:
                    movedown=False
                if event.key==K_ESCAPE:
                    terminate()
                if event.key==K_p:
                    fps=99999999999
                if event.key==K_g:
                    fps=60




        treecounter+=1
        if treecounter>=treespawnrate:
            treecounter=0
            treesize=random.randint(treeminsize,treemaxsize)
            newtree={'rect':pygame.Rect(random.randint(0,width-treesize),0-treesize,treesize,treesize),
                     'speed':treespeed,
                     'surface':pygame.transform.scale(treeimage,(treesize,treesize))}
            trees.append(newtree)
            
        for t in trees:
            t['rect'].move_ip(0, t['speed'])


        for t in trees[:]:
            if t['rect'].top>height:
                trees.remove(t)



        foodcounter+=1
        if foodcounter>=coinspawnrate:
            foodcounter=0
            foodsize=random.randint(coinminsize,coinmaxsize)
            newfood={'rect':pygame.Rect(random.randint(0,width-foodsize),0-foodsize,foodsize,foodsize),
                     'speed':treespeed,
                     'surface':pygame.transform.scale(foodimage,(foodsize,foodsize))}
            foods.append(newfood)
            
        for f in foods:
            f['rect'].move_ip(0, f['speed'])


        for f in foods[:]:
            if f['rect'].top>height:
                foods.remove(f)

        
        if movedown and playerrect.bottom<height:
            playerrect.top += playerspeed
        if moveup and playerrect.top>0:
            playerrect.top -= playerspeed
        if moveleft and playerrect.left>0:
            playerrect.left -= playerspeed
        if moveright and playerrect.right<width:
            playerrect.left += playerspeed


        windowsurface.fill(WHITE)

        drawtext('Score:%s'%score,font,windowsurface,10,0)
        drawtext('TopScore:%s'%topscore,font,windowsurface,10,40)


        windowsurface.blit(playerimage,playerrect)


        for t in trees:
            windowsurface.blit(t['surface'],t['rect'])
        for f in foods:
            windowsurface.blit(f['surface'],f['rect'])
            
        if eat(playerrect,foods):
            score+=250
            pickupsound.play()
            fps+=2

        
        if hitler(playerrect,trees):
            fps=60
            if score > topscore:
                topscore=score
            break
            
        pygame.display.update()
        mainClock.tick(fps)

    pygame.mixer.music.stop()
    gameoversound.play()
    drawtext('GAMEOVER!',font,windowsurface,width/3,height/3)
    drawtext('press any key to start',font,windowsurface,width/3,height/3+50)
    pygame.display.update()
    detectkeypress()


    


    

