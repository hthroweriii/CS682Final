import pygame, random, sys, re
import os
from datetime import datetime
from pygame.locals import *
from learn_snake_classes import *
import numpy as np


class SnakeFrame:

	def __init__(self, XS, YS, APOS, DIR):
		self.xs = list(XS)
		self.ys = list(YS)
		self.applepos = list(APOS)
		self.sLength = len(XS)
		self.dirs = DIR
	def __str__(self):
		return str(self.xs) + " " + str(self.ys) + " " + str(self.applepos) + " " + str(self.sLength) + " " + str(self.dirs)

class GameData:
	def __init__(self):
		self.humanTrain = False #Pause between Frames and Output all Frames?
		self.trainPause = False
		self.startSquares = 5 #Starting Snake Length
		self.loadData = False
		self.loadedData = list()
		self.playData = False
		self.dataSrc = ""
		self.customFileName = ""
		self.trainData = []
		self.trainTargetOutput = []

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
		return True
	else:
		return False



def wait():
	while True:
		if pygame.event.peek(KEYUP):
			return 

def interpretFromFile(filename, trainData, targetOutput):
	frames = list()
	outArray = []
	data = open(filename, 'r')
	for line in data:
		m = re.match('(\[.+?\]) (\[.+?\]) (\[.+?\]) (.+?) (.+?)', line)
		#print m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
		xList = map(int, (m.group(1)).replace(",","").replace("[","").replace("]","").split() )
		yList = map(int, (m.group(2)).replace(",","").replace("[","").replace("]","").split() )
		apos  = map(int, (m.group(3)).replace(",","").replace("[","").replace("]","").split() )
		direction = int(m.group(5)) 
		frames.append(SnakeFrame(xList, yList, apos, direction))
		tempArray = []
		tempArray += apos + [direction] + xList
		for x in range(0,50-len(xList)):
			tempArray += [0]
		tempArray += xList
		for x in range(0,50-len(yList)):
			tempArray += [0]
		trainData.append(tempArray)
		targetOutput.append(direction)
	data.close()
	#for x in frames:
	#	tempArray = tempArray + [x]
	#print tempArray[0]
	return frames
#Setup command line arguments
def setupCLA( gd ):
	for x in sys.argv:
		if x.lower() == "-train":
			gd.humanTrain = True
		elif x.lower() == "-pause":
			gd.trainPause = True
		elif x.lower() == "-loaddata":
			"What data should be loaded?: "
			gd.dataSrc = raw_input("What data should be loaded?: ")
			gd.loadData = True
		elif x.lower() == "-replay":
			gd.playData = True
		elif x[0:9].lower() == "-datasrc:":
			gd.dataSrc = x[9:]
			gd.loadData = True;
		elif x[0:8].lower() == "-saveas:":
			gd.customFileName = x[8:] 
		elif x[0:9].lower() == "-squares:":
			gd.startSquares= int(x[9:])
		elif x == "snake.py":
			pass
		else:
			print x, " is not a valid config argument."
	#gd.dataSrc = "2015-11-27 13:21:29"

def enumFileName(name):
	num = 1
	print "here"
	while(fileExits(name)):
		print "file exists"
		ind = findEnumNumber(name)
		if ind == -1:
			name = name + "_1"
		else:
			num = int(name[ind+1:])
			num += 1
			name = name[0:ind] + "_" + str(num)
	return name

def findEnumNumber(name):
	for x in range(len(name) - 1, 0, -1):
		if name[x] == "_":
			return x
	return -1

def fileExits(name):
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for f in files:
		if f == name:
			return True
	return False

def replayRoutine( gd ):
	print "Replay Beginning"
	gd.loadedData = interpretFromFile(gd.dataSrc, gd.trainData, gd.trainTargetOutput)
	s=gd.screen
	appleimage = gd.appleimage
	appleimage.fill((0, 255, 0))
	img = gd.img
	img.fill((255, 0, 0))
	f = gd.font

	for l in gd.loadedData:
		s.fill((255, 255, 255))
		events = pygame.event.get()
		for i in range(0, len(l.xs)):
			s.blit(img, (l.xs[i], l.ys[i]))
		s.blit(appleimage, l.applepos)
		t = f.render(str(l.sLength - 5), True, (0, 0, 0))
		s.blit(t, (10, 10))
		pygame.display.update()
		pygame.time.wait(10)

def regularGameRoutine( gd):
	def die(screen, score):
		#Declare Variables
		f=pygame.font.SysFont('Arial', 30)
		t=f.render('Your score was: '+str(score), True, (0, 0, 0))
		date = datetime.now()

		#Die Sequence
		screen.blit(t, (10, 270))
		pygame.display.update()

		#write data to file
		if gd.humanTrain:
			if gd.customFileName == "":
				outName = date.__str__()[:19] + "(" + str(gd.startSquares) + " - " + str(score + 5) + ")"
			else:
				outName = enumFileName(gd.customFileName)
			out = open(outName, 'w')
			for x in range(0 , lastValidFrame + 1):
				out.write(frameData[x].__str__() + "\n")
			out.close()
			print "Data Saved to: " + outName
		pygame.time.wait(2000)

		sys.exit(0)
	
	#Training Setup
	if gd.loadData:
		gd.loadedData = interpretFromFile(gd.dataSrc, gd.trainData, gd.trainTargetOutput)
	frameData = list()
	lastValidFrame = 0
	totalFrames = 0
	applepos = list()
	startSquaresX = [290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310,\
	330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350,\
	370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390,\
	410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430]
	startSquaresY = [290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290]



	#General Game Setup
	if gd.startSquares > 104:
		gd.startSquares = 104
	if gd.loadData:
		#Load gd.Previous Play
		xs = gd.loadedData[-1].xs
		ys = gd.loadedData[-1].ys
		dirs = gd.loadedData[-1].dirs
		score = gd.loadedData[-1].sLength - 5
		applepos = gd.loadedData[-1].applepos
		gd.startSquares = gd.loadedData[-1].sLength

	else:
		#Standard Game Start
		xs = list(startSquaresX[0:gd.startSquares])
		ys = list(startSquaresY[0:gd.startSquares])
		dirs = 0 
		score = 0
		applepos = (random.randint(0, 590), random.randint(0, 590))

	s= gd.screen
	appleimage = gd.appleimage
	appleimage.fill((0, 255, 0))
	img = gd.img
	img.fill((255, 0, 0))
	f = gd.font
	clock = pygame.time.Clock()

	#Initial Draw
	s.fill((255, 255, 255))	
	for i in range(0, len(xs)):
		s.blit(img, (xs[i], ys[i]))
	s.blit(appleimage, applepos)
	t=f.render(str(score), True, (0, 0, 0))
	s.blit(t, (10, 10))
	pygame.display.update()

	while True:
		if gd.humanTrain and gd.trainPause:
			wait()
		events = pygame.event.get()
		frameData.append(SnakeFrame(xs,ys, applepos, dirs))
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
					gd.trainPause = not gd.trainPause
		i = len(xs)-1
		while i >= 2:
			if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
				die(s, score)
			i-= 1
		#Apple Collision
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
		totalFrames += 1


def aiGameRoutine( gd , ps):
	def die(screen, score):
		#Declare Variables
		f=pygame.font.SysFont('Arial', 30)
		t=f.render('Your score was: '+str(score), True, (0, 0, 0))
		date = datetime.now()

		#Die Sequence
		screen.blit(t, (10, 270))
		pygame.display.update()

		#write weights to file

		pygame.time.wait(2000)

		sys.exit(0)
	
	#Training Setup
	
	if gd.loadData:
		gd.loadedData = interpretFromFile(gd.dataSrc, gd.trainData, gd.trainTargetOutput)

	applepos = list()
	startSquaresX = [290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310, 310,\
	330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 330, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350,\
	370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 370, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390, 390,\
	410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 410, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430, 430]
	startSquaresY = [290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290,\
	290, 270, 250, 230, 210, 190, 170, 150, 130, 110,  90,  70,  50,  50,  70,  90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290]



	#General Game Setup
	gd.startSquares = 5
	#Standard Game Start
	xs = list(startSquaresX[0:gd.startSquares])
	ys = list(startSquaresY[0:gd.startSquares])
	dirs = 0 
	score = 0
	applepos = (random.randint(0, 590), random.randint(0, 590))

	s= gd.screen
	appleimage = gd.appleimage
	appleimage.fill((0, 255, 0))
	img = gd.img
	img.fill((255, 0, 0))
	f = gd.font
	clock = pygame.time.Clock()

	#Initial Draw
	s.fill((255, 255, 255))	
	for i in range(0, len(xs)):
		s.blit(img, (xs[i], ys[i]))
	s.blit(appleimage, applepos)
	t=f.render(str(score), True, (0, 0, 0))
	s.blit(t, (10, 10))
	pygame.display.update()

	while True:
		if gd.humanTrain and gd.trainPause:
			wait()
		events = pygame.event.get()
		state = []
		state += applepos 
		state += [dirs] 
		state +=  xs
		for x in range(0,50-len(xs)):
			state += [0]
		state += ys
		for x in range(0,50-len(ys)):
			state += [0]
			prevDirs = dirs
		dirs = ps.predict(np.asarray(state))
		if abs(dirs - prevDirs) == 2:
			dirs = prevDirs
		i = len(xs)-1
		while i >= 2:
			if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
				die(s, score)
			i-= 1
		#Apple Collision
		if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
			score+=1
			xs.append(700)
			ys.append(700)
			applepos=(random.randint(0,590),random.randint(0,590))
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





def main():
	#Config
		gameData = GameData()
		setupCLA(gameData)
		pygame.init()
		gameData.screen = pygame.display.set_mode((600, 600))
		pygame.display.set_caption('Snake')
		gameData.appleimage = pygame.Surface((10, 10))
		gameData.appleimage.fill((0, 255, 0))
		gameData.img = pygame.Surface((20, 20))
		gameData.img.fill((255, 0, 0))
		gameData.font = pygame.font.SysFont('Arial', 20)
		if gameData.playData and gameData.loadData:
				replayRoutine( gameData )
		if gameData.humanTrain and gameData.loadData:
			playSnake = MLP(2, 1)
			playSnake.add(Linear(103,1000))
			playSnake.add(Sigmoid(1000))
			playSnake.add(Linear(1000,4))
			playSnake.add(Softmax(4))
			criterion = NLLLoss(103)
			train(np.asarray(gameData.trainData[:-1]), np.asarray(gameData.trainTargetOutput[1:]) ,  playSnake, criterion)
			aiGameRoutine( gameData, playSnake)
		else:
			regularGameRoutine( gameData )



if __name__ == "__main__":
  main()