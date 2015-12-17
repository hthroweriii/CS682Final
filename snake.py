import pygame, random, sys, re
from datetime import datetime
from pygame.locals import *
from learn_snake_classes import *
import numpy as np
from snakeTools import *
from GameData import *
def wait():
  while True:
    if pygame.event.peek(KEYUP):
      return 



def writeWeights(pSnake, gd):
  out = open(enumFileName(gd.customFileName), 'w')
  out.write("LinMod: ")
  for x in pSnake.modules:
    if isinstance(x,Linear):
      wY = x.W.shape[0]
      wX = x.W[0].shape[0]
      wB = len(x.b)
      out.write( str(wX) + " " )
      out.write( str(wY) + " " )
      out.write( str(wB) + "\n")
      out.write( str(gd.maxTrainPadding) + " ")
      out.write( str(int(gd.TMSlope)) + "\n")
      for i in range(wY):
        for j in range(wX):
          out.write(str(x.W[i][j]) + " " )
      out.write("\n")
      for i in range(wB):
        out.write(str(x.b[i]) + " " )
      out.write("\n")
      out.write("LinMod: ")

  out.close()

def loadWeights(pSnake, gd):
  data = open(gd.weightsFileName, 'r')
  mode = 0
  sizes = []
  params = []
  sizeInd = 0
  tempW = np.asarray([])
  tempB = np.asarray([])

  for line in data:
    mode += 1
    for s in line.split(' '):
      if s == "LinMod:":
        if len(sizes) > 0:
          tempW = np.reshape(tempW, ( sizes[sizeInd+1] , sizes[sizeInd] ) )
          tempLin = Linear( sizes[sizeInd+1], sizes[sizeInd] )
          tempLin.W = np.copy(tempW)
          tempLin.b = np.copy(tempB)
          tempW = np.asarray([])
          tempB = np.asarray([])
          pSnake.add( tempLin )
          if len(sizes) < 4:
            pSnake.add( Sigmoid( sizes[sizeInd + 2]   ) )
          sizeInd += 3
        mode = 0
        continue
      if s == "\n" or s == "":
        continue
      if mode == 0:
        num = int(s)
        sizes.append(num)
      if mode == 1:
        num = int(s)
        params.append(num)
      if mode == 2:
        tempW = np.append(tempW, float(s) )
      if mode == 3:
        tempB= np.append(tempB, float(s) )
  pSnake.add( Softmax(sizes[-1]) )
  gd.lin1M = sizes[0]
  gd.lin1N = sizes[1]
  gd.lin2M = sizes[4]
  gd.maxTrainPadding = params[0]
  gd.TMSlope = params[1]
  print gd.maxTrainPadding
  print gd.TMSlope
  print "Sizes: ",gd.lin1M,gd.lin1N, gd.lin2N,



'''
Replay Data
'''
def replayRoutine( gd ):
  print "Replay Beginning"
  (gd.loadedData, gd.trainData, gd.trainTargetOutput) = gd.interpretFromFile()
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
'''
Play Game Regularly
'''
def regularGameRoutine( gd):
  def die(screen, score):
    #Declare Variables
    print score
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
    (gd.loadedData, gd.trainData, gd.trainTargetOutput) = gd.interpretFromFile()

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

  s = gd.screen
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

'''
 Train AI Game Routine 
'''
def aiGameRoutine( gd , ps):
  def die(screen, score, ps, gd):
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
    gd.loadedData = gd.interpretFromFile()

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
    pygame.time.wait(50)
    if gd.humanTrain and gd.trainPause:
      wait()
    events = pygame.event.get()
    state = []
    state += applepos 
    state += [dirs] 
    if len(xs) > gd.maxTrainPadding:
      tempXS = xs[0:gd.maxTrainPadding]
      tempYS = ys[0:gd.maxTrainPadding]
      state += tempXS
      state += tempYS

    if len(xs) <= gd.maxTrainPadding:
      state += xs
      for x in range(0,gd.maxTrainPadding-len(xs)):
          state += [0]
      state += ys
      for x in range(0,gd.maxTrainPadding-len(ys)):
          state += [0]
    if gd.TMSlope:     
      state += [applepos[0] - xs[0] ] + [applepos[1] - ys[0]]
    prevDirs = dirs
    dirs = ps.predict(np.asarray(state))
    if abs(dirs - prevDirs) == 2:
      dirs = prevDirs

    i = len(xs)-1
    while i >= 2:
      if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
        die(s, score, ps, gd)
      i-= 1
    #Apple Collision
    if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
      score+=1
      xs.append(700)
      ys.append(700)
      applepos=(random.randint(0,590),random.randint(0,590))
    #Walls
    if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580: 
      die(s, score, ps, gd)
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
    gameData.setupCLA()
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
    if gameData.humanTrain and not gameData.trainPause:
      if gameData.loadWeights:
        playSnake = MLP(2, 1)
        loadWeights(playSnake,gameData)
        criterion = NLLLoss(gameData.lin1M)
      else:
        if gameData.loadData:
          gameData.interpretFromFile()
        playSnake = MLP(2, 1)
        playSnake.add(Linear( gameData.lin1M, gameData.lin1N))
        playSnake.add(Sigmoid(gameData.lin1N))
        playSnake.add(Linear(gameData.lin1N,gameData.lin2N))
        playSnake.add(Softmax(gameData.lin2N))
        criterion = NLLLoss(gameData.lin1M)
        train(np.asarray(gameData.trainData[:-2]), np.asarray(gameData.trainTargetOutput[1:]) ,  playSnake, criterion)
        print "Done Training"
        if gameData.customFileName != "":
            writeWeights(playSnake, gameData)
      aiGameRoutine( gameData, playSnake)
    else:
      regularGameRoutine( gameData )



if __name__ == "__main__":
  main()
