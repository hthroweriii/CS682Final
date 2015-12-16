import sys, re
class GameData(object):
    def __init__(self):
        self.humanTrain = False #Pause between Frames and Output all Frames?
        self.trainPause = False
        self.startSquares = 5 #Starting Snake Length
        self.loadData = False
        self.loadedData = list()
        self.loadWeights = False
        self.playData = False
        self.dataSrc = ""
        self.customFileName = ""
        self.weightsFileName = ""
        self.trainData = []
        self.trainTargetOutput = []
        ''' Training Module Specific'''
        self.lin1M =  103
        self.lin1N = 2000
        self.lin2N = 4
        self.maxTrainPadding = 50
        self.TMSlope = True


    '''
    Interpret Command Line Arguments
    '''  
    def setupCLA( self ):
        #Setup command line arguments
        for x in sys.argv:
            if x.lower() == "-train":
                self.humanTrain = True
            elif x.lower() == "-pause":
                self.trainPause = True
                self.loadWeights = True
            elif x.lower() == "-loaddata":
                "What data should be loaded?: "
                self.dataSrc = raw_input("What data should be loaded?: ")
                self.loadData = True
            elif x.lower() == "-replay":
                self.playData = True
            elif x.lower() == "-slope":
                self.TMSlope = True
            elif x[0:14].lower() == "-maxtrainsize:":
                self.maxTrainPadding = int(x[14:])
            elif x[0:9].lower() == "-datasrc:":
                self.dataSrc = x[9:]
                self.loadData = True;
            elif x[0:13].lower() == "-loadweights:":
                self.weightsFileName = x[13:]
                self.loadWeights = True
            elif x[0:8].lower() == "-saveas:":
                self.customFileName = x[8:] 
            elif x[0:9].lower() == "-squares:":
                self.startSquares= int(x[9:])
            elif x == "snake.py":
                pass
            else:
                print x, " is not a valid config argument."

    def interpretFromFile(self):
        frames = list()
        outArray = []
        data = open(self.dataSrc, 'r')
        self.trainData = []
        self.lin1M = (self.maxTrainPadding * 2) + 3
        if self.TMSlope:
            self.lin1M += 2
        for line in data:
            m = re.match('(\[.+?\]) (\[.+?\]) (\[.+?\]) (.+?) (.+?)', line)
            #print m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            xList = map(int, (m.group(1)).replace(",","").replace("[","").replace("]","").split() )
            yList = map(int, (m.group(2)).replace(",","").replace("[","").replace("]","").split() )
            apos  = map(int, (m.group(3)).replace(",","").replace("[","").replace("]","").split() )
            direction = int(m.group(5)) 
            frames.append(SnakeFrame(xList, yList, apos, direction))
            tempArray = []
            tempArray += apos + [direction]
            if len(xList) > self.maxTrainPadding:
                xList = xList[0:self.maxTrainPadding]
                yList = yList[0:self.maxTrainPadding]
            tempArray += xList
            if len(xList) <= self.maxTrainPadding:
                for x in range(0,self.maxTrainPadding-len(xList)):
                    tempArray += [0]
                tempArray += yList
                for x in range(0,self.maxTrainPadding-len(yList)):
                    tempArray += [0]
            if self.TMSlope:     
                tempArray += [apos[0] - xList[0] ] + [apos[1] - yList[0]]
            if len(tempArray) != self.lin1M:
                print "***************INVALID PARSING ERROR UNKNOWN************"
            else:
                self.trainData.append(tempArray)
            self.trainTargetOutput.append(direction)
        data.close()
        self.loadedData = list(frames)
        
        return (frames, self.trainData, self.trainTargetOutput)

class SnakeFrame:

    def __init__(self, XS, YS, APOS, DIR):
        self.xs = list(XS)
        self.ys = list(YS)
        self.applepos = list(APOS)
        self.sLength = len(XS)
        self.dirs = DIR
    def __str__(self):
        return str(self.xs) + " " + str(self.ys) + " " + str(self.applepos) + " " + str(self.sLength) + " " + str(self.dirs)

