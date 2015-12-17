import os
'''
-------------------------------------------------
SnakeTools.pys Contains Everything Not directly 
Related to Snake.py
-------------------------------------------------
'''
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

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
  if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
    return True
  else:
    return False