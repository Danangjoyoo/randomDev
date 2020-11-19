import pygame as pg
import random as rd

class char():
	def __init__(self,x,y,pic):
		self.x = x
		self.y = y
		self.pic = pic
		self.dead = False
		self.box = None
		self.q_step = []
		self.reward = 0
		self.bonus = 0
		self.step_table = []
		self.s, self.t1, self.t2 = 0, 0, 0
		self.idx = 0
		self.depreciated = False

	def move(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			self.y -= 1
		if keys[pg.K_s]:
			self.y += 1
		if keys[pg.K_a]:
			self.x -= 1
		if keys[pg.K_d]:
			self.x += 1

	def autorun(self):
		global q_table, r_table, eps
		self.t1 += 1
		list_idx_max = []
		list_max = []
		len_list_max =[]
		if self.t1 == 2:
			if eps == 0:
				future_val = rd.choice([1,2,3,4])
			else:
				try:
					max_val = max(q_table[0])
					for i in enumerate(q_table[0]):
						if i[1] == max_val:
							list_idx_max.append(i[0])
							len_list_max.append(len(q_table[1][i[0]]))
					idx_max = len_list_max.index(max(len_list_max))
					self.idx = list_idx_max[idx_max]
					q = q_table[1][self.idx]
					if self.s < len(q) and not self.depreciated:
						future_val = q[self.s]
					else:
						future_val = rd.choice([1,2,3,4])	
					print(future_val, ' | ', self.idx, ' | ',r_table[self.idx] , ' | ', q, ' | ', self.q_step, ' | ', self.s )
				except:
					future_val = rd.choice([1,2,3,4])

			self.s += 1
			if future_val == 1: #atas
				self.y -= 1
			elif future_val == 2: #bawah
				self.y += 1
			elif future_val == 3: #kiri
				self.x -= 1
			elif future_val == 4: #kanan
				self.x += 1
			self.q_step.append(future_val)
			try:
				pass
				#print(self.s, self.t2, future_val, self.q_step[-2])
			except:
				pass
			try:
				if self.q_step[-2] != future_val:
					if self.q_step[-2] + 1 == future_val or self.q_step[-2] - 1 == future_val: 
						#self.bonus -= 1
						print(self.q_step[-2], future_val)
						self.q_step.pop(-1)
						self.q_step.append(self.q_step[-2])
						print("WRONG DIRECTION")
			except:
				pass
			self.t2 += 1
		elif self.t1 > 2:
			self.t1 = 0

	def getReward(self):
		global r_table, q_table
		score = 0
		score += r_table[-1]*0.1
		try:
			#pass
			#self.q_step.pop(-1)
			if len(q_table[1][self.idx]) > 2: 
				q_table[1][self.idx].pop(-1)
				q_table[0][self.idx] -= 1
				self.depreciated = False
			else:
				self.depreciated = True
		except:
			pass
		score += len(self.q_step)
		#score += self.bonus*self.t2
		r_table.append(score)
		return score

	def over(self):
		global eps, gameover, q_table
		try:
			self.q_step.pop(-1)
			self.q_step.append(rd.choice([1,2,3,4]))
		except:
			pass
		self.reward = self.getReward()
		q_table[0].append(self.reward)
		q_table[1].append(self.q_step)
		eps += 1
		gameover = True

	def draw(self):
		if not self.dead:
			scale_x, scale_y = self.x*10, self.y*10
			self.box = win.blit(self.pic,(scale_x, scale_y))
		else:
			self.over()

def draw_wall(pic,x,y):
	a = win.blit(pic, (x*10, y*10))
	return a

def drawWindow():
	global map1, win, w, h, main_w, main_h, boundaries, eps
	pg.draw.rect(win, (100,100,180), (0, 0, w, h))
	boundaries = []
	for i in enumerate(map1):
		for ii in enumerate(i[1]):
			if ii[1] == 1:
				boundaries.append(draw_wall(wall_pic, ii[0], i[0]))
	man.draw()
	for i in boundaries:
		if i.colliderect(man.box):
			man.dead = True

	main.blit(	pg.transform.scale(win, (main_w, main_h)), (0,0))
	pg.draw.rect(main, (0,0,0), (7,3,165,30))
	eps_text1 = pg.font.SysFont('comicsans', 39).render('Episode : ', 5, (255, 255,255))
	eps_count1 = pg.font.SysFont('comicsans', 39).render(str(eps), 5, (255,255,255))
	main.blit(eps_text1, (10, 5))
	main.blit(eps_count1, (140, 5))
	pg.display.update()

def AI():
	global q_table
	learning_rate = 0.1
	discount_factor = 0.95

def getReward():
	return reward

q_table = [[],[]]
r_table = [0]
pg.init()
w = 160
h = 120
main_w = w*4
main_h = h*4
main = pg.display.set_mode((main_w, main_h))
win = pg.Surface((w,h))
clock = pg.time.Clock()

wall_pic = pg.image.load('wall.png')
char_pic = pg.image.load('head.png')

man = char(1,10,char_pic)

map1 =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
       [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
       [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
       [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

run = True
gameover = False
t = 0
eps = 1
boundaries = []

while run:
	t += 1
	if not gameover:
		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
		if t == 2:
			#man.move()
			man.autorun()
		elif t > 2:
			t = 0
		drawWindow()
	else:
		t = 0
		man = 0
		man = char(1, 10, char_pic)
		gameover = False

	if pg.key.get_pressed()[pg.K_ESCAPE]:
		run = False

	#for i in q_table:
		#print(i)

file = open('qTab.txt', 'w')
for i in q_table:
	file.write(str(i))
file.close()
pg.quit()