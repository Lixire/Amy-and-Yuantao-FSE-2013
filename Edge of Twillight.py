###Import Modules
from pygame import *
from glob import *
from random import *
screen = display.set_mode((1100,700))

"---------------------------------------------------------"
###Menu Screens
loading = image.load("screens/loading.png")
#Loading screen first because you need it at the start when its loading
def loadingscreen():
    screen.blit(loading,(0,0))
    display.flip()
loadingscreen()
page = "menu"
titlescreen = image.load("screens/title.png")
playhighlight = image.load("screens/play.png")
instructhighlight = image.load("screens/instructions.png")
credithighlight = image.load("screens/credits.png")
creditscreen = image.load("screens/creditscreen.png")
instructionsscreen = image.load("screens/instructionsscreen.png")
playbox = Rect(493,350,118,28)
instructbox = Rect(380,401,335,25)
creditbox = Rect(450,455,197,25)
"---------------------------------------------------------"
#Graphics
###In Game graphics
enemyPics=[]
for i in range(10):
    enemyPic=[]
    for j in range(13):
        enemyPic.append(image.load("pictures/characters/meanerpants/enemy"+str(i)+"/enemy"+str(i)+str(j)+".png"))
    enemyPics.append(enemyPic)
bossPics=[]
for i in range(25):
    bossPics.append(image.load("pictures/characters/meanerpants/boss/porter"+str(i)+".png"))
powerupPic=[0]*7
for i in range(7):
    powerupPic[i]=image.load("pictures/entities/powerup"+str(i)+".png")
bombPic=[0]*22
for i in range(22):
    bombPic[i]=image.load("pictures/entities/bomb"+str(i)+".png")
bulletPic=[0]*2
for i in range(2):
    bulletPic[i]=image.load("pictures/entities/bullet-"+str(i)+".png")
doorPics=[]
for i in range(4):
    doorPics.append([])
    for j in range(4):
        doorPics[i].append(image.load("pictures/terrain/doors/door"+str(i)+str(j)+".png"))
        
"---------------------------------------------------------"
#screen
levelpanel=[]
for i in range(6):
    levelpanel.append(image.load("screens/level"+str(i)+".png"))
dead = image.load("screens/gameover.png")
notdead = image.load("screens/victory.png")
#character gui
healthgui = image.load("pictures/charactergui/healthgui.png")
bombgui = image.load("pictures/charactergui/bombgui.png")
attackstat = image.load("pictures/charactergui/attackstat.png")
atkspeedstat = image.load("pictures/charactergui/attackspeedstat.png")
speedstat = image.load("pictures/charactergui/speedstat.png")
font.init()
arielFont = font.SysFont("Ariel", 20)
"---------------------------------------------------------"
###Room Layouts and Spawning
#Hold possible room layouts
layouts=[[]]
#Level keeps track of the current floor graphic as well as progress
level=0
floorPic=[]
terrainPic=[]
#Bad holds all of the Enemy objects
bad = []
#Different graphics for different levels
for i in range(6):
    floorPic.append(image.load("pictures/terrain/floor"+str(i)+".png"))
    terrainPic.append([])
    #Different types of terrain
    for j in range(1,6):
        terrainPic[i].append(image.load("pictures/terrain/block"+str(i)+"-"+str(j)+".png"))
#This list holds the possible floors encountered, loaded from a txt file
floorLayouts=[]
layouts=open("txtfiles/floorLayouts.txt").read().strip().split("\n\n")
for layout in range(len(layouts)):
    floorLayouts.append(layouts[layout].split("\n"))
    #This turns the input list from a 7x13 to a 13x7
    newfloor=[[0]*7 for i in range(13)]
    for i in range(7):
        for j in range(13):
            newfloor[j][i]=int(floorLayouts[layout][i][j])
    floorLayouts[layout]=newfloor
#Gets coordanates from file for where enemies will spawn
spawnpoints=open("txtfiles/spawnpoints.txt").read().strip().split("\n")
for  i in range(len(spawnpoints)):
    spawnpoints[i]=spawnpoints[i].split(" ")
    if len(spawnpoints[i][-1])==1:
        spawnpoints[i][-1]=[int(spawnpoints[i][-1])]*(len(spawnpoints[i])-1)
    else:
        spawnpoints[i][-1]=spawnpoints[i][-1].split(",")
    for j in range(len(spawnpoints[i])-1):
        tx,ty=spawnpoints[i][j].split(",")
        spawnpoints[i][j]=(int(tx),int(ty),int(spawnpoints[i][-1][j]))
    del spawnpoints[i][-1]

"---------------------------------------------------------"
#####Functions and Classes
###Path Finding
#Uses math to find distance
def mathdistance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

#Heuristic score for a*
def hscore(point,target):
    return abs(point[0]-target[0])+abs(point[1]-target[1])

#Part of a*
#Uses parent dictionary to find next step
def goback(start,target,current,parent):
    while current!=start:
        temp=current
        current=parent[current]
    #If current = start to begin with then it will simply return target
    try:
        return temp
    except:
        return target
    
#A* algorithm
##The A* pathfinding works by adding and ranking nearby tiles. It then
##takes the best ranked tile (based on movement cost and distance frrom target)
##and adds it to a closed list. Once it has found the target, it will
##trace it back to the starting location using the parent dictionary
##and finding the place you have to start to step onto that square.
##It then returns the next step that must be taken.
x8=[0,1,0,-1,1,-1,1,-1]        #8 directions you can go
y8=[1,0,-1,0,1,1,-1,-1]
movecost=[10]*4+[14]*4
valid=set([(x,y) for x in range(13) for y in range(7)])
def astar(start,target):
    x=x8
    y=y8
    openset=set([start])
    closedset=set([])
    fscore={}
    gscore={}
    parent={}
    gscore[start]=0
    fscore[start]=gscore[start]+hscore(start,target)
    #Main A* Loop
    #EDIT: Ignore all of this stuff below because it DOES NOTHING,
    #I have torn out hairs on this and I still cannot find the source
    #of the crash as it is completely random and I have gone through
    #several games without experiencing it once before it comes back
    #several times. The only lead I have is that it occurs not only in
    #the A* but in the enemy movement, but since A* is the longest portion
    #it ends up breaking here. I am really lost on how this issue even occurs.
    #Putting in flags and such are pointless when I have no idea when the
    #crash will occurs and when it does, it stops just as randomly as it came.
    #It's like trying to find the needle in the haysack, you get poked but
    #you see no needle. I know it's not an issue with no finding the player
    #because I've been able to get the A* to reach accordingly as well as
    #having checked the map the crash occurs on, but all the local variables
    #are lost. :( :( :( :( ;_;
    while len(openset)>0:       #If there are no more open tiles to add or check, then the target cannot be reached
        #if len(openset)>70:     #Prevents a crash where the program is stuck in the a* loop
        #    break               #Also it makes it so that enemies won't chase you that far
        low=9999999999          #Very high number to start
        for coor in openset:    #Finds lowest number
            if fscore[coor]<low and coor not in closedset:
                current=coor
                low=fscore[coor]
        openset.remove(current);
        closedset.add(current)
        if current == target:
            return goback(start,target,current,parent)
        for i in range(8):
            if (current[0]+x[i],current[1]+y[i]) in valid:
                temp=(current[0]+x[i],current[1]+y[i])
                if floor[temp[0]][temp[1]]<3:
                    good = True
                    if i>3:
                        if (temp[0],temp[1]-y[i]) in valid:
                            if floor[temp[0]][temp[1]-y[i]]>2:
                                good = False
                        if (temp[0]-x[i],temp[1]) in valid:
                            if floor[temp[0]-x[i]][temp[1]]>2:
                                good = False
                    if temp in closedset:
                        good = False
                    if temp not in gscore and good:
                        gscore[temp]=gscore[current]+movecost[i]
                    if (temp not in openset or gscore[current]+movecost[i]<gscore[temp]) and good:
                        gscore[temp]=gscore[current]+movecost[i]
                        fscore[temp]=gscore[temp]+hscore(temp,target)
                        parent[temp]=current
                        if temp == target:
                            return goback(start,target,temp,parent)
                        openset.add(temp)
    return start

#Uses similar triangles to find a path
#If no path can be found then it uses a* instead. If a path is found,
#it uses similar triangles to move towards the target
def regularpath(speed,start,target,size):
    screenbox=Rect(0,0,1037-62,605-90)
    startx,starty = start
    temx,temy=start
    tarx,tary = target
    distance = mathdistance(startx,starty,tarx,tary)
    #If the target is within running distance, the mob reaches its target
    if speed>distance:
        return (tarx+62,tary+90)
    blocked = False
    while speed<distance:
        #collision check
        if screenbox.colliderect(Rect(temx-size//2,temy,size,size)):
            for w in walls:
                if Rect(temx+62-size//2,temy+90,size,size).colliderect(w):
                    blocked = True
                    break
        else:
            return (startx+62,starty+90)
        #Progression
        distance = mathdistance(temx,temy,tarx,tary)
        ratio=6/max(distance,10**(-100))
        temx = (tarx-temx)*ratio+temx
        temy = (tary-temy)*ratio+temy
        temx=int(temx)
        temy=int(temy)
    #If blocked, A* choses the new target square
    if blocked:
        start=(start[0]//75,start[1]//75)
        target=(target[0]//75,target[1]//75)
        tarx,tary=astar(start,target)
        tarx=tarx*75+37
        tary=tary*75+37
    distance = mathdistance(startx,starty,tarx,tary)
    if distance<speed:
        return (tarx+62,tary+90)
    ratio=speed/max(distance,10**(-100))
    startx = int((tarx-startx)*ratio+startx)
    starty = int((tary-starty)*ratio+starty)
    if screenbox.collidepoint((startx,starty)):
        return (startx+62,starty+90)
    return (start[0]+62,start[1]+90)

#This path returns a boolean statement.
#If it checks if the enemy can reach the player by similar triangles.
#The boolean is based on it they can reach the player and tells the
#class if it can shoot or not. An issue with this is that the ratio
#to get to the player is always changing and as some angles are unobtainable
#this allows thhe program to curve around corners. As I cannot make the bullets
#home in the the player, this causes ranged enemiesto get trapped on corners.
#Which because I found the melee enemies to be really boring, that means all
#enemies.
def shootcheck(speed,start,target,size):
    screenbox=Rect(0,0,1037-62,605-90)
    startx,starty = start
    temx,temy=start
    tarx,tary = target
    distance = mathdistance(startx,starty,tarx,tary)
    #Explained in regular path
    if speed>distance:
        return True
    while speed<distance:
        if screenbox.colliderect(Rect(temx,temy,size,size)):
            for w in walls:
                if Rect(temx+62,temy+90,size,size).colliderect(w):
                    return False
        else:
            return False
        distance = mathdistance(temx,temy,tarx,tary)
        ratio=speed/max(distance,10**(-100))
        temx = (tarx-temx)*ratio+temx
        temy = (tary-temy)*ratio+temy
        temx=int(temx)
        temy=int(temy)
    return True
"---------------------------------------------------------"
###Floor Drawing
#Floor holds all the ground values
#0-Nothing 1-Spikes 2-Broken crate bottem Below 3 is Walkable 3-Broken Crate 4-Crate 5-Wall
floor=[[0]*7 for i in range(13)]
def drawfloor(level):
    screen.blit(floorPic[level],(62,100))
    for i in range(13):
        for j in range(7):
            if floor[i][j]!=0:
                n=floor[i][j]-1
                screen.blit(terrainPic[level][n],(i*75+62,j*75+100))
                
#This function returns a list holding the positions of all terrains of a certian
#type. In this case the walls and the spikes
def collidebox(floor,n=2,greater=True):
    nowalk= []
    for i in range(len(floor)):
        for j in range(len(floor[i])):
            if greater:
                if floor[i][j] >n:
                    nowalk.append(Rect(i*75+61,j*75+100,75,75))
            else:
                if floor[i][j] ==n:
                    nowalk.append(Rect(i*75+61,j*75+100,75,75))
    #Zihao did this, I have nothing to do with this please forgive me I'm sorry, he said it would work (he thinks anyways)
    return set(list(map(tuple,nowalk)))

"---------------------------------------------------------"
###Classes and Class Interaction
#This class is the enemies that will be fought during the game
#It takes in a x position, a y position, and a breed type.
#health     :Hits taken before death
#damage     :Damage done
#cooldown   :Delay between attacks, melee enemies have no delay, but use the player is granted invulnerability after taking damage
#range      :Distance the enemy will shoot, bullet goes just a little further, if range is 0, the nemy is melee
#hitbox size:Size of the Enemy, making this too big will cause it to get stuck on walls
#speed      :Movement speed of the enemy
#shots      :How many bullets per shot
#burst      :How many times a shots will be fired in succession, includ
#shot deviation     :How inaccurate the shot will be
breedstat=[
    [3,1,0,0,40,5,0,0,0],             #0.Basic Thug, runs at you
    [2,1,30,250,40,3,1,0,5],        #1.Basic Thug with basic gun
    [5,1,20,450,50,0,1,3,1],        #2.Turret, really tough but can't move
    [4,1,40,200,40,3,3,0,15],       #3.Tougher thug with shotgun
    [3,2,50,600,40,3,1,0,0],        #4.Rifle Soldier
    [4,3,30,300,40,3,4,0,1],        #5.Blaster Soldier
    [7,2,90,600,90,0,20,0,15],      #6.Cannon Soldier, lots of shots and tough, but long cooldown and low range with no movement
    [5,2,80,150,60,3,3,25,25],      #7.Flamethrower, high burst, short cooldown and range
    [4,1,30,150,40,4,4,2,20],       #8.Shogun Trooper, fast short ranged frighter
    [3,2,20,100,30,5,6,3,15]       #9.Blizt Trooper, faster, smaller, but with shorter range and health
    ]
class Enemy:
    def __init__(self, x, y, breed=0):
        self.x = x
        self.y = y
        self.velocity = [0]*4
        self.breed=breed
        self.health = breedstat[breed][0]
        self.damage = breedstat[breed][1]
        self.cooldown = 0
        self.cooldownmax = breedstat[breed][2]
        self.distance = breedstat[breed][3]
        self.hitbox = breedstat[breed][4]
        self.speed=breedstat[breed][5]
        self.shots=breedstat[breed][6]
        self.burst=breedstat[breed][7]
        self.bursts=self.burst
        self.deviation=breedstat[breed][8]
        self.canshoot=False
        self.cooldown=0

        self.pics=[0]*13
        for i in range(13):
            self.pics[i]=enemyPics[breed][i]
        self.frame = 0
        self.frameDelay = 3
        self.frameCount = 0
    #Uses regular movement and A*, check above
    #Ranged enemies check if they can shoot, if not
    #they try to move into position
    def move(self):
        if self.distance==0:
            if not Rect(guy.x-guy.hitbox//2,guy.y,guy.hitbox,guy.hitbox).colliderect(Rect(self.x-self.hitbox//2,self.y,self.hitbox,self.hitbox)):
                oldx=self.x
                oldy=self.y
                self.x,self.y=regularpath(self.speed,(self.x-62,self.y-90),(guy.x-62,guy.y-90),self.hitbox)
                oldx=self.x-oldx
                oldy=self.y-oldy
                if oldx==0 and oldy==0:
                    self.frame=0
                else:
                    if oldx>oldy:
                        if oldx>0:
                            self.frame=7
                        else:
                            self.frame=4
                    else:
                        if oldy>0:
                            self.frame=1
                        else:
                            self.frame=10
        else:
            if mathdistance(guy.x-7,guy.y+self.hitbox//2-7,self.x,self.y)<=self.distance:
                self.canshoot=shootcheck(12,(self.x-62-7,self.y-90+self.hitbox//2-7),(guy.x-62,guy.y-90),15)
            else:
                self.canshoot=False
            if not self.canshoot and self.speed>0:
                oldx=self.x
                oldy=self.y
                self.x,self.y=regularpath(self.speed,(self.x-62,self.y-90),(guy.x-62,guy.y-90),self.hitbox)
                oldx=self.x-oldx
                oldy=self.y-oldy
                if oldx>oldy:
                    if oldx>0:
                        self.frame=7
                    else:
                        self.frame=4
                else:
                    if oldy>0:
                        self.frame=1
                    else:
                        self.frame=10
            elif not self.canshoot:
                self.frame=0
    #Makes bullets or punches         
    def attack(self):
        if self.distance==0:
            if Rect(guy.x-guy.hitbox//2,guy.y,guy.hitbox,guy.hitbox).colliderect(Rect(self.x-self.hitbox//2,self.y,self.hitbox,self.hitbox)):
                if guy.health>0 and guy.immunity==0:
                        guy.health-=self.damage
                        guy.immunity=40
        else:
            if self.canshoot and self.cooldown==self.cooldownmax:
                ratio=randint(7,8)/max(mathdistance(guy.x-7,guy.y+self.hitbox//2-7,self.x,self.y),10**(-100))
                dx=(guy.x-self.x)*ratio
                dy=(guy.y-self.y)*ratio
                if dx>dy:
                    if dx>0:
                        self.frame=7
                    else:
                        self.frame=4
                else:
                    if dy>0:
                        self.frame=2
                    else:
                        self.frame=11
                        
                for i in range(self.shots):
                    badbullets.append([self.x-7,self.y+self.hitbox//2-7,int(dx+randint(-self.deviation,self.deviation)/10),int(dy+randint(-self.deviation,self.deviation)/10),15,(self.x-7,self.y+self.hitbox//2-7),self.distance,self.damage])
                if self.bursts==0:
                    self.cooldown=0
                    self.bursts=self.burst
                else:
                    self.bursts-=1
                    
            if self.cooldown!=self.cooldownmax:
                self.cooldown +=1
    #Draws the enemy
    def draw(self):
        self.frameDelay-=1
        if self.canshoot:
            self.frameDelay=3
            self.frameCount=1
        if self.frameDelay==0:
            self.frameDelay=3
            self.frameCount+=1
        if self.frame==0 or self.canshoot:
            screen.blit(self.pics[self.frame],(self.x-self.hitbox//2,self.y))
        else:
            screen.blit(self.pics[self.frame+self.frameCount%3],(self.x-self.hitbox//2,self.y))

#This function moves all the enemy bullets and checks if:
#1. They hit anything and deals damage
#2. They go outside of their range
#enemy bullets are kept globally so that killing an enemy
#doesn't delete their shots
def movebadbullet(bulletFrame):
    global badbullets
    newbullets = []
    for bull in badbullets:
        x= bull[0]
        y = bull[1]
        col = False
        if 46<x<(1050) and 100<y<625:
            hitbox = Rect(x,y,bull[4],bull[4])
            if hitbox.colliderect(Rect(guy.x-guy.hitbox//2,guy.y,guy.hitbox,guy.hitbox)) and guy.immunity==0 and guy.health>0:
                guy.health-=bull[7]
                col = True
                guy.immunity=40
                
            for w in walls:
                if hitbox.colliderect(w):
                    col = True
                    break
            if col == False and mathdistance(x,y,bull[5][0],bull[5][1])<=bull[6]*1.5:
                newbullets.append([bull[0]+bull[2],bull[1]+bull[3],bull[2],bull[3],bull[4],bull[5],bull[6],bull[7]])
    badbullets = newbullets[:]
    for bull in badbullets:
        screen.blit(bulletPic[bulletFrame],(bull[0],bull[1]))

#The goal of each level is to find the boss room where the teleporter is located.
#There, you fight a tough teleporter that spawns guards to protect itself. When
#you have defeated the teleporter you can jump in to progress or continue to
#fight through.
class Boss:
    def __init__(self):
        self.cooldown=0
        self.health=20
        self.hitbox=Rect(6*75+45+7,3*75+50,100,100)
        self.pics=[]
        #This is the spawning chances for different levels
        self.spawn=[[1,1,3],[4],[3,4,5,5],[4,4,4,5,5,5,7,7],[5,5,7,8],[8,8,8,9],[9]]
        for b in bossPics:
            self.pics.append(b)
    #Changes the cooldown. Limits total enemies to 6 to prevent lag
    def cooldownset(self,level):
        if len(bad)<6:
            self.cooldown+=1
        else:
            self.cooldown=0
        if self.cooldown==200 and self.health>0:
            self.cooldown=0
            makeEnemyOne(6,3,choice(self.spawn[level]))
    #If the teleporter is beaten, you use it to progress to the next level
    #(using something you just broke makes no sense but we're not getting marked on that sort of logic right?)
    def endlevel(self):
        global level,guy,room,floor,badbullets,bad,powerups,bulletframe,teleporter
        if self.health<1:
            if Rect(guy.x-guy.hitbox//2,guy.y,guy.hitbox,guy.hitbox).colliderect(Rect(6*75+80+7,3*75+85,30,30)):
                #Advances level, resets everything
                level+=1
                if level==6:
                    return True
                room=(0,0)
                genmap()
                guy.x,guy.y=(6*75+37+70,3*75+37+91)
                guy.immunity=40
                floor=list(floormap[room])
                drawfloor(0)
                badbullets=[]
                guy.bullets=[]
                bad=[]
                powerups=[]
                guy.bombs=[]
                bulletFrame=0
                #The teleporter grwos stronger with every level
                teleporter=Boss()
                teleporter.health+=level*5
        return False
            
    def draw(self):
        if self.health>0:
            if self.cooldown<100:
                screen.blit(self.pics[0],(self.hitbox[0],self.hitbox[1]))
            elif self.cooldown<150:
                screen.blit(self.pics[1+self.cooldown%7],(self.hitbox[0],self.hitbox[1]))
            elif self.cooldown<156:
                screen.blit(self.pics[8+self.cooldown%6],(self.hitbox[0],self.hitbox[1]))
            elif self.cooldown<162:
                screen.blit(self.pics[14+self.cooldown%3],(self.hitbox[0],self.hitbox[1]))
            elif self.cooldown<=200:
                screen.blit(self.pics[17+self.cooldown%7],(self.hitbox[0],self.hitbox[1]))
        else:
            screen.blit(self.pics[24],(self.hitbox[0],self.hitbox[1]))

            
#Current movement velocity for the character
vx = 0
vy = 0
#Character class
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bulletv=[0]*4
        self.hitbox = 30
        self.velocity= [0]*4
        self.health = 6
        self.damage = 1 #
        self.movev = 6 #
        self.bullets = []
        self.cooldown = 15
        self.cooldownmax=15
        self.immunity=0
        self.distance=600 #
        #bombs
        self.bombcount=3
        self.bombs=[]
        #graphics
        self.pics={}
        for i in range(13):
            self.pics[i]=image.load("pictures/characters/character/character"+str(i)+".png")
        self.frame = 0
        self.frameDelay = 3
        self.frameCount = 0
        self.shooting=False
        #Movement
        self.velocity[2]=[ord("d"),self.movev,0]
        self.velocity[0]=[ord("s"),0,self.movev]
        self.velocity[3]=[ord("w"),0,-self.movev]
        self.velocity[1]=[ord("a"),-self.movev,0]
        #Shooting
        self.bulletv=[0]*4
        self.bulletv[2]=[K_RIGHT,14,0]
        self.bulletv[0]=[K_DOWN,0,14]
        self.bulletv[3]=[K_UP,0,-14]
        self.bulletv[1]=[K_LEFT,-14,0]
    #Displays health, bombs and other stats
    def chargui(self,level,levelpanel):
        screen.blit(healthgui,(620,32))
        screen.blit(bombgui,(620,54))
        screen.blit(attackstat,(245,10))
        screen.blit(speedstat,(245,50))
        screen.blit(atkspeedstat,(375,50))
        atkstxt = arielFont.render("Atk speed: "+str(16-self.cooldownmax), True, (200,100,100))
        speedtxt = arielFont.render("Speed: "+str(self.movev), True, (200,100,100))
        attacktxt =arielFont.render("Attack: "+str(self.damage), True, (200,100,100))
        rangetxt = arielFont.render("Range "+str(self.distance)+" px", True, (200,100,100))
        screen.blit(atkstxt,(410,62))
        screen.blit(speedtxt,(280,62))
        screen.blit(attacktxt,(280,20))
        screen.blit(rangetxt,(410,20))
        for i in range(self.health):
            draw.rect(screen,(0,255,0),(650+i*50,30,45,20))
        for i in range(self.bombcount):
            draw.rect(screen,(255,0,0),(650+i*50,55,45,20))
            screen.blit(levelpanel[level],(0,660))
    #Moves character, goes through list to check for movement
    def move(self):
        global vx,vy, walls
        keys=key.get_pressed()
        flag = False #to prevent multiple direction shots
        for v in self.velocity:
            if keys[v[0]]:
                flag = True
                if not self.shooting:
                    self.frame=self.velocity.index(v)*3+1
                
                if 62< self.x+v[1]<1037 and 90<self.y+v[2]<595: #to prevent character from going off the screen
                    hitbox = Rect(self.x+v[1]-self.hitbox//2,self.y+v[2],self.hitbox, self.hitbox) #to check collide with walls
                    col = False
                    for w in walls:
                        if hitbox.colliderect(w):
                            col = True
                    
                    if col == False: #if you don't hit a wall
                        self.x += v[1]
                        self.y += v[2]
                        
                vx=[v[1] if v[1]!=0 else 0][0] #your velocity
                vy=[v[2] if v[2]!=0 else 0][0]
        if flag == False: #if you're not walking
            if not self.shooting:
                self.frame=0
            vx = 0
            vy = 0        
        for s in spikes:
            if Rect(self.x+v[1]-self.hitbox//2,self.y+v[2],self.hitbox, self.hitbox).colliderect(s):
                if self.health>0 and self.immunity==0:
                    self.health-=1
                    self.immunity=40
        if self.immunity>0:
            self.immunity-=1
    #Same as movement, but for attacking. Adds bullets to a list
    def shoot(self,vx,vy):
        keys=key.get_pressed()
        if self.cooldown== self.cooldownmax:
            self.shooting = False
            for bv in self.bulletv:
                if keys[bv[0]]:
                    self.cooldown = 0
                    self.frame=self.bulletv.index(bv)*3+1
                    self.shooting = True
                    
                    if vx!= 0 or vy!=0:
                        self.bullets.append([self.x-7,self.y+self.hitbox//2,bv[1]+vx//2,bv[2]+vy//2,(self.x-7,self.y+self.hitbox//2)])
                    else:
                        self.bullets.append([self.x-7,self.y+self.hitbox//2,bv[1],bv[2],(self.x-7,self.y+self.hitbox//2)])
                    break
        else:
            self.cooldown +=1
    #Moves bullets
    def movebullet(self):
        newbullets = []
        for bull in self.bullets:
            newbullets.append([bull[0]+bull[2],bull[1]+bull[3],bull[2],bull[3],bull[4]])
        self.bullets = newbullets
    #Checks bullets for collisions and stuff
    def checkbullet(self):
        global floor, room, bossroom, teleporter
        newbullets = []
        for bull in self.bullets:
            x= bull[0]
            y = bull[1]
            col = False
            if 46<x<(1050) and 100<y<625:
                hitbox = Rect(x,y,15,15)
                if room == bossroom:
                    if hitbox.colliderect(teleporter.hitbox) and teleporter.health>0:
                        teleporter.health-=self.damage
                        col=True
                if not col:
                    for b in bad:
                        if hitbox.colliderect(Rect(b.x-b.hitbox//2,b.y,b.hitbox,b.hitbox)):
                            b.health-=self.damage
                            col = True
                            break
                if not col:
                    for w in walls:
                        if hitbox.colliderect(w):
                            wallx,wally,temp1,temp2=w
                            if 2<floor[wallx//75][wally//75-1]<5:
                                floor[wallx//75][wally//75-1]-=1
                            col = True
                            break
                if mathdistance(bull[4][0],bull[4][1],bull[0],bull[1])>self.distance:
                    col=True
                if not col:
                    newbullets.append(bull)
        self.bullets = newbullets[:]
        
    def draw(self,bulletFrame):
        self.frameDelay-=1
        if self.shooting:
            self.frameDelay=3
            self.frameCount=1
        if self.frameDelay==0:
            self.frameDelay=3
            self.frameCount+=1
            
        if self.immunity%4==0:
            if self.health>0:
                if self.frame==0:
                    screen.blit(self.pics[self.frame],(self.x-self.hitbox//2,self.y))
                else:
                    screen.blit(self.pics[self.frame+self.frameCount%3],(self.x-self.hitbox//2,self.y))
        for bull in self.bullets:
            screen.blit(bulletPic[bulletFrame],(bull[0],bull[1]))

    def checkleave(self):
        global room, floor, level, bad, powerups
        x=[0,-1,1,0]
        y=[1,0,0,-1]
        picfixx=[-10,-10,0,-10]
        picfixy=[5,-10,-10,-10]
        doors=[Rect(6*75+62+10,7*75+95,55,10),Rect(52,3*75+110,12,55),Rect(13*75+62,3*75+110,12,55),Rect(6*75+72,90,55,10)]
        newloc=[(6*75+72+37,105),(13*75+62-37,3*75+110),(52+100,3*75+110),(6*75+62+10+37,7*75+60)]
        for i in range(4):
            if (room[0]+x[i],room[1]+y[i]) in floormap:
                if bossroom==(room[0]+x[i],room[1]+y[i]):
                    doortype=2
                else:
                    doortype=0
                d=doors[i]
                if room in beaten:
                    screen.blit(doorPics[doortype+1][i],(doors[i][0]+picfixx[i],doors[i][1]+picfixy[i]))
                    if Rect(self.x-self.hitbox//2,self.y,self.hitbox,self.hitbox).colliderect(d) and i==(self.frame-1)//3:
                        guy.x,guy.y=newloc[i]
                        floormap[room]=list(floor[:])
                        room=(room[0]+x[i],room[1]+y[i])
                        floor=list(floormap[room][:])
                        self.bullets=[]
                        self.bombs=[]
                        powerups=[]
                        badbullets=[]
                        bad=[]
                        if room not in beaten:
                            if room == bossroom:
                                teleporter=Boss()
                            breakcount=0
                            while len(bad)==0:
                                if bad!=[]:
                                    break
                                makeEnemyMass(choice(spawnpoints[level*4:(level+1)*4]))
                else:
                    screen.blit(doorPics[doortype][i],(doors[i][0]+picfixx[i],doors[i][1]+picfixy[i]))
    #Drops a bomb and advances bombs, does a lot of damage to
    #both self and nearby enemies
    def checkbomb(self,spacepress):
        global room, bossroom, teleporter
        if self.bombcount>0 and spacepress:
            self.bombcount-=1
            self.bombs.append([self.x-7,self.y+self.hitbox//2,100])
        for b in self.bombs:
            b[2]-=1
            if b[2]==14:
                for baddie in bad:
                    if mathdistance(b[0],b[1],baddie.x,baddie.y)<100:
                        baddie.health-=4
                if room == bossroom:
                    if mathdistance(b[0],b[1],teleporter.hitbox[0]+50,teleporter.hitbox[1]+50)<150:
                        teleporter.health-=4
                    
                if mathdistance(b[0],b[1],self.x,self.y)<100:
                    if self.health>0 and self.immunity==0:
                        self.health-=4
                        self.immunity=40
                x=x8+[0]
                y=y8+[0]
                bx=(b[0]-62)//75
                by=(b[1]-100)//75
                for i in range(9):
                    if (bx+x[i],by+y[i]) in valid:
                        if 2<floor[bx+x[i]][by+y[i]]<=5:
                            floor[bx+x[i]][by+y[i]]=2
            if b[2]<13:
                screen.blit(bombPic[b[2]],(b[0]-50,b[1]-50))
            elif b[2]<20:
                screen.blit(bombPic[b[2]],(b[0]-15,b[1]-15))
            else:
                screen.blit(bombPic[20+b[2]%2],(b[0]-15,b[1]-15))
            if b[2]==0:
                self.bombs.remove(b)
"---------------------------------------------------------"
###Power ups
#Picking up a powerup change your characters stats.
#This holds the names for all the powerups and is
#organized in the same order as the pictures for indexing.
#The drop list is for chance instead
poweruplist=["health++","bomb","bombx3","health","damage boost","fire rate boost","speed boost"]
powerupdroplist=["health","bomb","health","bomb","bombx3","health++","damage boost","fire rate boost","speed boost"]
powerups=[]
def powerupdrop(x,y,chance):
    if floor[(x-62)//75][(y-90)//75]==0 and randint(0,chance)==0:
        powerups.append([x,y,choice(powerupdroplist)])

def powerupcheck():
    global guy
    for p in powerups:
        screen.blit(powerupPic[poweruplist.index(p[2])],(p[0],p[1]))
        if Rect(guy.x-guy.hitbox//2,guy.y,guy.hitbox,guy.hitbox).colliderect(p[0],p[1],30,30):
            if p[2]=="health":
                if guy.health<6:
                    guy.health+=1
            elif p[2]=="health++":
                guy.health=6
            elif p[2]=="bomb":
                guy.bombcount+=1
            elif p[2]=="bombx3":
                guy.bombcount+=3
            elif p[2]=="damage boost":
                guy.damage+=1
            elif p[2]=="fire rate boost":
                if guy.cooldownmax>0:
                    guy.cooldownmax-=3
                    guy.cooldown=guy.cooldownmax
            elif p[2]=="speed boost":
                guy.movev+=1
            powerups.remove(p)
"---------------------------------------------------------"
####Game Map
#The map in the game is a dictionary full of points held in a set
#floormap is the dictionary of layouts. As the player
#progresses through each room, it will generate a new
#layout and store it in the map. The set is used to
#prevent two rooms spawning in the same place.
floormap={}
floormap[(0,0)]=[[0]*7 for i in range(13)]
mapset=set([(0,0)])
beaten=set([(0,0)])
seen=set([(0,0)])
bossroom=(0,0)
#genmap  recursively creates a map where the size is dependent on the
#currently level It uses a set to hold used room locations(filled or otherwise)
#and a dictionary to hold all of the rooms. The first room is always empty.
def genmap(current=(0,0),counter=0):
    global floormap,mapset,floorLayouts,bossroom,beaten,seen
    x=[1,-1,0,0]
    y=[0,0,1,-1]
    if counter==0:
        floormap={}
        floormap[(0,0)]=[[0]*7 for i in range(13)]
        mapset=set([(0,0)])
        beaten=set([(0,0)])
        seen=set([(0,0)])
    for i in range(4):
        new=(current[0]+x[i],current[1]+y[i])
        if new not in mapset and len(mapset)<(level+1)*6+1:
            chance=randint(0,counter+1)
            if counter<3 and mathdistance(0,0,new[0],new[1])<3:
                if chance==0 or len(mapset)<(level+1)*3:
                    floormap[new]=[]
                    temp=choice(floorLayouts)
                    for t in temp:
                        floormap[new].append(t[:])
                    genmap(new,counter+1)
                    mapset.add(new)
                    if mathdistance(0,0,new[0],new[1])>2:
                        bossroom=new[:]
    floormap[bossroom]=[]
    temp=floorLayouts[0]
    for t in temp:
        floormap[bossroom].append(t[:])
    floormap[(0,0)]=[[0]*7 for i in range(13)]
def minimap(mapset,room):
    for m in mapset:
        if mathdistance(room[0],room[1],m[0],m[1])==1 and m not in seen:
            seen.add(m)
        if m == room:
            draw.rect(screen,(255,255,255),(m[0]*21+60+1,m[1]*14+35+1,19,13))
        elif m in beaten:
            draw.rect(screen,(155,155,155),(m[0]*21+60+1,m[1]*14+35+1,18,12))
        elif m in seen:
            draw.rect(screen,(255,255,255),(m[0]*21+60+1,m[1]*14+35+1,18,12),2)
        if m == bossroom and (m in seen or m in beaten):
            draw.rect(screen,(255,0,0),(m[0]*21+60+1,m[1]*14+35+1,18,12),2)

"---------------------------------------------------------"            
###Enemy creation functions
#Makes enemies based on list
def makeEnemyMass(points):
    global bad
    for x,y,z in points:
        if floor[x][y]<2:
            bad.append(Enemy(x*75+37+62,y*75+100,z))
#Individual spawning
def makeEnemyOne(x,y,z):
    global bad
    if floor[x][y]<2:
        bad.append(Enemy(x*75+37+58,y*75+100,z))

"---------------------------------------------------------"
###Menu Functions
#Menu screen, this allows the user to press buttons and
#access different parts of the menu. Pressing play will
#break out of the menu loop and go into the game loop.
def menu():
    running = True
    hover = "none"
    click = False
    screen.blit(titlescreen,(0,0))
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEBUTTONDOWN:
                click = True
            else:
                click = False
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        if playbox.collidepoint(mpos):
            if hover != "play":
                hover = "play"
                screen.blit(playhighlight,(0,0))
            if click:
                return "play"
        elif instructbox.collidepoint(mpos):
            if hover!= "instruct":
                hover = "instruct"
                screen.blit(instructhighlight,(0,0))
            if click:
                return "instruct"
        elif creditbox.collidepoint(mpos):
            if hover!="credit":
                hover = "credit"
                screen.blit(credithighlight,(0,0))
            if click:
                return "credit"
        elif hover != "none":
            hover = "none"
            screen.blit(titlescreen,(0,0))
        display.flip()
    return "exit"
#Instructions
def instructions():
    running = True
    screen.blit(instructionsscreen,(0,0))
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
        #blits screen image
        #if quit returns to menu
        display.flip()
    return "menu"
#Credits
def credit():
    running = True
    screen.blit(creditscreen,(0,0))
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
        display.flip()
    return "menu"
#Game over screen, pretty self explanatory
def gameover():
    global page, dead
    screen.blit(dead,(0,0))
    display.flip()
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
    page="menu"
#Victory Screen
def victory():
    global page, notdead
    screen.blit(notdead,(0,0))
    display.flip()
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
    page="menu"

#Main Loop
running = True
while page!="exit":
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
                page="exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        while page != "exit":
            if page == "menu":
                page = menu()
            if page == "instruct":
                page = instructions()
            if page == "play":
                break
            if page == "credit":
                page = credit()
        break
    if page=="play":
        #Sets all variables
        level=0
        genmap()
        guy=Character(6*75+37+70,3*75+37+91)
        room=(0,0)
        floor=list(floormap[room])
        drawfloor(level)
        badbullets=[]
        bulletFrame=0
        teleporter=Boss()
        running = True
        myClock = time.Clock()
        win=False
        while running:
            spacepress=False
            for evnt in event.get():
                if evnt.type == QUIT or guy.health<1:
                    running = False
                if evnt.type == KEYDOWN:
                    if key.get_pressed()[K_SPACE]:
                        spacepress=True
            
            #Walls holds all positions that are not walkable
            walls = collidebox(floor)
            #Spikes holds all positions that are painful to walk on
            spikes = collidebox(floor,1,False)
            
            mb = mouse.get_pressed()
            mx,my = mouse.get_pos()
            guy.move()
            guy.shoot(vx,vy)
            guy.checkbullet()
            guy.movebullet()
            
            screen.fill((0,0,0))
            drawfloor(level)
            powerupcheck()
            guy.checkbomb(spacepress)
            minimap(mapset,room)
            if room==bossroom:
                teleporter.cooldownset(level)
                teleporter.draw()
            if room not in beaten:
                for baddie in bad:
                    if baddie.health<1:
                        powerupdrop(baddie.x,baddie.y,10)
                        bad.remove(baddie)
                    if room not in beaten:
                        baddie.move()
                        baddie.attack()
                        baddie.draw()
            movebadbullet(bulletFrame)
            bulletFrame=1-bulletFrame
            guy.draw(bulletFrame)
            if len(bad)==0 and (teleporter.health<1 or room!=bossroom):
                if room not in beaten:
                    beaten.add(room)
                    powerupdrop(6*75+62,3*75+90,1)
            if teleporter.health<1 and room==bossroom:
                if teleporter.endlevel():
                    win=True
                    break
            guy.checkleave()
            guy.chargui(level,levelpanel)
            display.flip()
            myClock.tick(50)
        if win:
            victory()
        else:
            gameover()
        running=True
    else:
        break
quit()
