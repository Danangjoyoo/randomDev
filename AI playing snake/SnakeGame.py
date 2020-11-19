import pygame as pg
import random
import numpy as np

def cvt(num):
    return num*20
def reCvt(num):
    return int(num/20)

class snake():
    matrix = []
    for i in range(25):
        matrix.append(i)

    def __init__(self):
        self.x, self.y = self.randomnum(), self.randomnum()
        self.posi = [[cvt(self.x), cvt(self.y)]]
        self.length, self.lock = 1, 0
        self.eat = False
        self.dead = False
        self.head = random.choice([1,2,3,4])
        self.t = 0
        self.directionLock()
        self.inner_block, self.outer_block = None, None
        print(self.head, self.lock)

    def randomnum(self):
        return random.choice(snake.matrix)

    def body(self, xy, head=None):
        titik = xy[0]
        titik2 = xy[1]
        if head:
            self.outer_block = pg.draw.rect(win, (100,100,250), (titik, titik2, 20, 20))
            self.inner_block = pg.draw.rect(win, (40, 20, 10), (titik + 2, titik2 + 2, 16, 16))
        else:
            self.outer_block = pg.draw.rect(win,(100,100,250), (titik, titik2, 20, 20))
            self.inner_block = pg.draw.rect(win,(40,200,100), (titik+2, titik2+2, 16, 16))

    def draw(self):
        self.body_pos = []
        self.head_pos = []
        if not self.dead:
            if not self.eat:
                if ular.posi[0][0]+10 == kue.pos[-1][0] and ular.posi[0][1]+10 == kue.pos[-1][1]:
                    self.eat = True
                    kue.eaten = True
            else:
                self.length += 1
                self.eat = False

            for i in enumerate(self.posi):
                if i[0]+1 <= self.length:
                    if i[0] == 0:
                        self.body(i[1], head=True)
                        self.head_pos = self.outer_block
                    else:
                        self.body(i[1])
                        self.body_pos.append(self.outer_block)
                else:
                    self.posi.pop(i[0])

            for i in self.body_pos:
                if self.head_pos.colliderect(i):
                    self.dead = True

        else:
            self.over()

    def over(self): #game over function
        global gameover
        pic = pg.image.load('gameover.png')
        win.blit(pic, (0,0))
        global eps; eps += 1
        length_bank.append(self.length)
        gameover = True

    def directionLock(self):
        if self.head == 1:
            self.lock = 2
        elif self.head == 2:
            self.lock = 1
        elif self.head == 3:
            self.lock = 4
        elif self.head == 4:
            self.lock = 3

    def setHead(self, direction):
        lastHead = self.head
        self.head = direction
        if self.head != self.lock:
            self.head = direction
        else:
            self.head = lastHead

    def autorun(self):
        self.t += 1
        #print(f'SNAKE T: {self.t}')
        self.directionLock()
        if self.t == 5:
            if self.head == 1 and self.lock != 1: #kanan
                self.x += 1
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            elif self.head == 2 and self.lock != 2: #kiri
                self.x -= 1
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            elif self.head == 3 and self.lock != 3: #atas
                self.y -= 1
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            elif self.head == 4 and self.lock != 4: #bawah
                self.y += 1
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            self.borderingReact(False)
        elif self.t > 5:
            self.t = 0
        self.draw()

    def borderingReact(self, passThrough=True):
        if passThrough:
            if cvt(self.y) > 500:
                self.y = 0
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            elif cvt(self.y) < 0:
                self.y = 480 / 20
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))

            if cvt(self.x) > 500:
                self.x = 0
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
            elif cvt(self.x) < 0:
                self.x = 480 / 20
                self.posi.insert(0, (cvt(self.x) - 10, cvt(self.y) - 10))
        else:
            if cvt(self.x) < 20 or cvt(self.x) > 480 or cvt(self.y) < 20 or cvt(self.y) > 480:
                self.dead = True

class food():
    matrix = []
    for i in range(20):
        matrix.append(i+2)

    def __init__(self):
        self.x, self.y = cvt(self.randomnum()),cvt(self.randomnum())
        self.pos = [[self.x, self.y]]
        self.eaten = False

    def randomnum(self):
        return random.choice(food.matrix)

    def spawn(self):
        map = remap()
        freespace = []
        if self.eaten:
            self.pos.clear()
            #self.x, self.y = cvt(self.randomnum()), cvt(self.randomnum())
            for i in enumerate(map):
                for ii in enumerate(i[1]):
                    if ii[1] == 0:
                        freespace.append((ii[0], i[0]))
            randomSel = random.choice(freespace)
            self.x, self.y = cvt(randomSel[0]), cvt(randomSel[1])
            self.pos.append((self.x, self.y))
            self.eaten = False
        else:
            self.draw()

    def draw(self):
        pg.draw.circle(win,(255,30,30),(self.x,self.y),(5))

def drawWindow():
    win.fill((0, 0, 0))
    ular.autorun()
    if not ular.dead:
        kue.spawn()
    eps_text = pg.font.SysFont('comicsans', 30).render('Episode : ', 1, (255, 255, 255))
    eps_count = pg.font.SysFont('comicsans', 30).render(str(eps), 1, (255, 255, 255))
    win.blit(eps_text, (10, 10))
    win.blit(eps_count, (130, 10))
    length_text = pg.font.SysFont('comicsans', 30).render('Snake Length : ', 1, (255, 255, 255))
    length_count = pg.font.SysFont('comicsans', 30).render(str(ular.length), 1, (255, 255, 255))
    win.blit(length_text, (180, 10))
    win.blit(length_count, (340, 10))
    try:
        pass
        #pg.draw.line(win, (25, 250, 50), (ular.head_pos[0]+10, ular.head_pos[1]+10), (kue.pos[0][0], kue.pos[0][1]), 1)
    except:
        pass
    pg.display.update()

def remap():
    map = []
    for i in range(26):
        map.append([])
        for ii in range(26):
            if i == 0 or i == 25:
                map[i].append(1)
            elif ii == 0 or ii == 25:
                map[i].append(1)
            else:
                map[i].append(0)
    for i in ular.body_pos:
        x,y = reCvt(i[0]+10), reCvt(i[1]+10)
        map[y][x] = 1

    x, y = reCvt(ular.head_pos[0]+10), reCvt(ular.head_pos[1]+10)
    map[y][x] = 2

    x, y = reCvt(kue.pos[0][0]+10), reCvt(kue.pos[0][1]+10)
    map[y][x] = 3
    return map

def checkSurrounding(map, x ,y, centerVal):
    x , y = reCvt(x+10), reCvt(y+10)
    surMap = []
    for i in range(3): #define row
        surMap.append([])
        for ii in range(3): #define column
            pos = map[y-1+i][x-1+ii]
            if not pos == map[y][x]:
                surMap[i].append(pos) #surrounding value
            else:
                surMap[i].append(centerVal) #center value
    """for i in surMap:
        print(i)
    print('===')"""
    return surMap

def calculateDist(pos1, pos2):
    dist = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    return dist

def localCor2globalCor(referencedPos, localMap):
    globalCor = []
    hx, hy = referencedPos[0], referencedPos[1]
    globalCor.append([localMap[1][2], (0 + hy, 1 + hx)])  # kanan
    globalCor.append([localMap[1][0], (0 + hy, -1 + hx)])  # kiri
    globalCor.append([localMap[0][1], (-1 + hy, 0 + hx)])  # atas
    globalCor.append([localMap[2][1], (1 + hy, hx)])  # bawah
    return globalCor

def AI():
    dist_list = []
    allMove = []
    availableMove = []
    map = remap()
    surMap = checkSurrounding(map, ular.head_pos[0], ular.head_pos[1],2) #untuk surrounding kepala ular
    tx, ty = reCvt(kue.pos[0][0]+10), reCvt(kue.pos[0][1]+10)
    hx, hy = reCvt(ular.head_pos[0] + 10), reCvt(ular.head_pos[1] + 10)

    # global coordinate
    allMove = localCor2globalCor((hx, hy), surMap) #all coverage movement, both allowed or not

    for i in allMove:
        if i[0] == 0 or i[0] == 3:
            availableMove.append(i) #only allowed movement, matrix
            dist = calculateDist((i[1][1],i[1][0]),(tx,ty)) #distance between allowed movement point to targeted point
            dist_list.append(dist)

    idx_distance = dist_list.index(min(dist_list)) #index value yg memiliki jarak terpendek
    selected_move = allMove.index(availableMove[idx_distance]) #index dari all covered movement, menari index matrix yang akan diambil selanjutnya dari surrounding

    #evaluate selected move
    """mini_surMap = checkSurrounding(map, cvt(future_pos[1]), cvt(future_pos[0]), 0) #untuk surrounding future head
    if (mini_surMap[0][1] == 1 and mini_surMap[2][1] == 1) or (mini_surMap[1][0] == 1 and mini_surMap[1][2] == 1):
        dist_list.pop(idx_distance)
        availableMove.pop(idx_distance)
        idx_distance = dist_list.index(min(dist_list))
        selected_move = allMove.index(availableMove[idx_distance])
    print(availableMove[idx_distance], '|', selected_move+1 )
    for i in mini_surMap:
        print(i)
    print('=====')"""
    global eps
    selected_move = verification(eps, map, allMove, availableMove, idx_distance, dist_list, selected_move)

    #print(dist_list, '|', allMove, '|', selected_move, '|', availableMove[selected_move]
    ular.head = selected_move+1

def verification(step, map, allMove, availableMove, idx_distance, dist_list, selected_move):
    future_pos = availableMove[idx_distance][1]
    for i in range(step):
        mini_surMap = checkSurrounding(map, cvt(future_pos[1]), cvt(future_pos[0]), 0)  # untuk surrounding future head
        top, bot, left, right = mini_surMap[0][1], mini_surMap[2][1], mini_surMap[1][0], mini_surMap[1][2]
        if not (left != 1 and top != 1 and right != 1) or (top != 1 and right != 1 and bot != 1) or (right != 1 and bot != 1 and left != 1) or (bot != 1 and right != 1 and top != 1):
            if (top == 1 and bot == 1) or (left == 1 and right == 1):
                dist_list.pop(idx_distance)
                availableMove.pop(idx_distance)
                idx_distance = dist_list.index(min(dist_list))
                #selected_move = allMove.index(availableMove[idx_distance])
                print(f'eleminated at step-{i}')
            else:
                for i in enumerate(availableMove):
                    if i[1] == 0:
                        idx_distance = i[0]
        future_pos = availableMove[idx_distance][1]
    selected_move = allMove.index(availableMove[idx_distance])
    #print('=============')
    return selected_move

ular = snake()
kue = food()
t = 0
pg.init()
clock = pg.time.Clock()
win = pg.display.set_mode((500, 500))
run,gameover = True, False
eps = 1
length_bank = []
while run:
    if not gameover:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        t += 1
        keys = pg.key.get_pressed()
        try:
            AI()
        except:
            pass
        if t == 3:
            if keys[pg.K_RIGHT]:
                ular.setHead(1)
            if keys[pg.K_LEFT]:
                ular.setHead(2)
            if keys[pg.K_UP]:
                ular.setHead(3)
            if keys[pg.K_DOWN]:
                ular.setHead(4)
            try:
                #pg.key.get_pressed()
                pass
            except:
                pass
        elif t > 3:
            t = 0
        if keys[pg.K_ESCAPE]:
            ular.over()
            run = False
        drawWindow()
    else:
        ular, kue, t = 0, 0, 0
        ular = snake()
        kue = food()
        gameover = False

for i in length_bank:
    print(i)
print("===============")
print(f'Maximum Length: {max(length_bank)}\nSuccessfull Percentage : {round(max(length_bank)/(23*23)*100, 2)} % at Episode {length_bank.index(max(length_bank))}')
pg.quit()