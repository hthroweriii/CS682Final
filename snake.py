import pygame, random, sys, re
from datetime import datetime
from pygame.locals import *


class SnakeFrame:

	def __init__(self, XS, YS, APOS, DIR):
		self.xs = list(XS)
		self.ys = list(YS)
		self.applepos = list(APOS)
		self.sLength = len(XS)
		self.dirs = DIR
	def __str__(self):
		return str(self.xs) + " " + str(self.ys) + " " + str(self.applepos) + " " + str(self.sLength) + " " + str(self.dirs)

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
		return True
	else:
		return False

def die(screen, score):
	#Declare Variables
	f=pygame.font.SysFont('Arial', 30)
	t=f.render('Your score was: '+str(score), True, (0, 0, 0))
	date = datetime.now()

	#Die Sequence
	screen.blit(t, (10, 270))
	pygame.display.update()
	pygame.time.wait(2000)

	#write data to file
	if humanTrain:
		out = open(date.__str__()[:19] + "(" + str(startSquares) + " - " + str(score + 5) + ")" , 'w')
		for x in range(0 , lastValidFrame + 1):
			out.write(frameData[x].__str__() + "\n")
		out.close()

	sys.exit(0)

def wait():
	while True:
		if pygame.event.peek(KEYUP):
			return 

def interpretFromFile(filename):
	frames = list()
	data = open(filename, 'r')
	for line in data:
		m = re.match('(\[.+?\]) (\[.+?\]) (\[.+?\]) (.+?) (.+?)', line)
		#print m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
		xList = map(int, (m.group(1)).replace(",","").replace("[","").replace("]","").split() )
		yList = map(int, (m.group(2)).replace(",","").replace("[","").replace("]","").split() )
		apos  = map(int, (m.group(3)).replace(",","").replace("[","").replace("]","").split() )
		direction = int(m.group(5)) 
		frames.append(SnakeFrame(xList, yList, apos, direction))
	data.close()
	return frames

#Config
humanTrain = True #Pause between Frames and Output all Frames?
trainPause = True
startSquares = 5 #Starting Snake Length
loadData = False
dataSrc = "2015-11-27 14:11:08(5 - 13)"


#Training Setup
if loadData:
	loadedData = interpretFromFile(dataSrc)
frameData = list()
lastValidFrame = 0
totalFrames = 0
startSquaresX = [290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310,\
330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350,\
370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390,\
410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430]
startSquaresY = [290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290]



#General Game Setup
if startSquares > 104:
	startSquares = 104
if loadData:
	#Load Previous Play
	xs = loadedData[-1].xs
	ys = loadedData[-1].ys
	dirs = loadedData[-1].dirs
	score = loadedData[-1].sLength - 5
	applepos = loadedData[-1].applepos
	startSquares = loadedData[-1].sLength
else:
	#Standard Game Start
	xs = list(startSquaresX[0:startSquares])
	ys = list(startSquaresY[0:startSquares])
	dirs = 0 
	score = 0
	applepos = (random.randint(0, 590), random.randint(0, 590))
initScore = score
pygame.init()
s=pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')
appleimage = pygame.Surface((10, 10))
appleimage.fill((0, 255, 0))
img = pygame.Surface((20, 20))
img.fill((255, 0, 0))
f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

while True:
	if humanTrain and trainPause:
		wait()
	events = pygame.event.get()
	for e in events:
		if e.type == QUIT:
			sys.exit(0)
		#Controls
		elif e.type == KEYDOWN:
			if e.key == K_UP and dirs != 0:dirs = 2
			elif e.key == K_DOWN and dirs != 2:dirs = 0
			elif e.key == K_LEFT and dirs != 1:dirs = 3
			elif e.key == K_RIGHT and dirs != 3:dirs = 1
			elif e.key == K_SPACE: 
				trainPause = not trainPause
	i = len(xs)-1
	while i >= 2:
		if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
			die(s, score)
		i-= 1
	#Apple Collisoin
	if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
		score+=1
		xs.append(700)
		ys.append(700)
		applepos=(random.randint(0,590),random.randint(0,590))
		lastValidFrame = totalFrames
	#Walls
	if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580: 
		die(s, score)
	i = len(xs)-1
	while i >= 1:
		xs[i] = xs[i-1]
		ys[i] = ys[i-1]
		i -= 1
	if dirs==0:ys[0] += 20
	elif dirs==1:xs[0] += 20
	elif dirs==2:ys[0] -= 20
	elif dirs==3:xs[0] -= 20	
	s.fill((255, 255, 255))	
	for i in range(0, len(xs)):
		s.blit(img, (xs[i], ys[i]))
	s.blit(appleimage, applepos)
	t=f.render(str(score), True, (0, 0, 0))
	s.blit(t, (10, 10))
	pygame.display.update()
	frameData.append(SnakeFrame(xs,ys, applepos, dirs))
	totalFrames += 1



