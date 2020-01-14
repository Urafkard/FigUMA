#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import random

from time import time

#from itertools import product
import itertools
#import numpy as np


#password maker
# Write your program here

symbolminus = 4 #black
symbolplus = 3  #green
symbolcross = 1 #red
symbolcircle = 2    #blue


heur = 2

#heuristica 1 espaços
mapheur1 = [[symbolminus, symbolminus, symbolcross,None,       symbolcross],
            [None,        None,        None,       symbolcross,None],
            [None,        None,        symbolcross,symbolplus, symbolcross],
            [symbolcircle,symbolcircle,symbolplus, symbolplus, symbolplus],
            [symbolcircle,symbolcircle,None,       symbolplus, None]]


mapheur2 = [[[[-1,-1,-1,3],[-1,-1,-1,3],[6,-1,-1,4]],[[-1,-1,-1,1],[-1,-1,-1,1],[-1,-1,-1,1]],[[-1,-1,-1,-1],[-1,-1,-1,2],[-1,-1,8,3]],[[-1,-1,-1,2],[-1,-1,-1,4],[-1,-1,-1,2]],[[3,-1,-1,-1],[-1,-1,-1,-1],[3,-1,-1,-1]]],
            [[[25,25,25,25],[25,25,25,25],[25,25,25,25]],[[1,-1,-1,-1],[1,-1,-1,-1],[1,-1,-1,-1]],[[-1,-1,1,-1],[-1,-1,1,-1],[-1,-1,1,-1]],[[2,-1,-1,-1],[2,-1,-1,-1],[2,-1,-1,-1]],[[24,24,24,24],[24,24,24,24],[24,24,24,24]]],
            [[[-1,-1,2,-1],[-1,-1,-1,-1],[-1,-1,4,-1]],[[-1,-1,3,-1],[-1,-1,2,-1],[-1,-1,2,-1]],[[-1,-1,-1,-1],[5,-1,5,-1],[9,-1,9,-1]],[[-1,-1,4,-1],[-1,-1,3,-1],[-1,-1,3,-1]],[[-1,-1,5,-1],[-1,-1,-1,-1],[-1,-1,5,-1]]],
            [[[-1,1,-1,-1],[-1,1,-1,-1],[-1,1,-1,-1]],[[-1,-1,-1,-1],[4,4,-1,-1],[7,1,-1,-1]],[[-1,-1,6,-1],[-1,-1,4,-1],[-1,-1,6,-1]],[[-1,-1,-1,-1],[3,8,-1,-1],[4,-1,-1,-1]],[[-1,-1,-1,-1],[-1,6,-1,-1],[-1,-1,-1,-1]]],
            [[[-1,-1,-1,-1],[-1,3,-1,-1],[8,-1,-1,-1]],[[-1,2,-1,-1],[-1,2,-1,7],[-1,2,-1,6]],[[-1,-1,-1,-1],[-1,-1,-1,6],[-1,-1,7,7]],[[-1,-1,-1,-1],[-1,5,-1,5],[-1,-1,-1,5]],[[-1,-1,-1,-1],[-1,7,-1,-1],[5,-1,-1,-1]]]]


pecasExistentes = []
pecasExistentesOld = []

pecasRequeridasMax = (9,-1,9,3)
pecasRequeridasMin = (5,4,5,2)

def product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


allPoints = []

for x in product(range(5),repeat=2):
  allPoints += [x]


def sortF(t,symbol,rank):
  if(mapheur2[t[0]][t[1]][rank][symbol-1] == -1):
    return 255
  else:
    return mapheur2[t[0]][t[1]][rank][symbol-1]

def sortBySymbol(symbol):
  global allPoints
  rank = getPriorityRank(symbol)
  #print("rank: " + str(rank))
  allPoints = sorted(allPoints, key=lambda t: sortF(t,symbol,rank), reverse=False)

score = 0



def getPriorityRank(symbol):
  #print(str(symbol), "peças: ", pecasExistentes[symbol-1] )
  if(pecasExistentes[symbol-1]/pecasRequeridasMax[symbol-1]>=1 and symbol != 2):
    return 2
  elif(pecasExistentes[symbol-1]/pecasRequeridasMin[symbol-1]>=1):
    return 1
  else:
    return 0







#patterns
# MINUS
sminus = [[symbolminus,symbolminus]]
sminusp = 4

bminus = [[symbolminus,symbolminus,symbolminus]]
bminusp = 8

#  PLUS
splus = [[None,symbolplus,None],
       [symbolplus,symbolplus,symbolplus],
       [None,symbolplus,None]]
splusp = 32

bplus = [[None,None,symbolplus,None,None],
        [None,None,symbolplus,None,None],
        [symbolplus,symbolplus,symbolplus,symbolplus,symbolplus],
        [None,None,symbolplus,None,None],
        [None,None,symbolplus,None,None]]
bplusp = 512

#  CROSS
scross = [[symbolcross,None,symbolcross],
       [None,symbolcross,None],
       [symbolcross,None,symbolcross]]
scrossp = 32

bcross = [[symbolcross,None,None,None,symbolcross],
        [None,symbolcross,None,symbolcross,None],
        [None,None,symbolcross,None,None],
        [None,symbolcross,None,symbolcross,None],
        [symbolcross,None,None,None,symbolcross]]
bcrossp = 512

#  CIRCLE
scircle = [[symbolcircle,symbolcircle],
         [symbolcircle,symbolcircle]]
scirclep = 16

mcircle1 = [[symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle]]
mcircle1p = 64

mcircle2 = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,None,symbolcircle],
          [symbolcircle,None,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle,symbolcircle]]
mcircle2p = 4096

bcircle = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle]]
bcirclep = 65536

figureSequence = ("bcircle","bcross","bplus","bminus","mcircle2","scross","splus","sminus","mcircle1","scircle")

symbols = (" ","x","o","+","-")



def printMatrix(matrix):
    text = "-----\n"
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            text += symbols[int(matrix[x][y])]
        text = text + "\n"
    print(text)



# Colors: (0:No Color, 1:Black, 2:Blue, 3:Green, 4:Yellow, 5:Red, 6:White, 7:Brown)




def match_pattern(input_array, pattern, wildcard_function=None):
    #print(input_array)
    #print(pattern)
    pattern_shape = (len(pattern),len(pattern[0]))
    input_shape = (len(input_array),len(input_array[0]))


    if len(pattern_shape) != len(input_shape):
        raise ValueError("Input array and pattern must have the same dimension")

    shape_difference = [i_s - p_s for i_s, p_s in zip(input_shape, pattern_shape)]

    if any((diff < -1 for diff in shape_difference)):
        raise ValueError("Input array cannot be smaller than pattern in any dimension")

    dimension_iterators = [range(0, s_diff + 1) for s_diff in shape_difference]

    # This loop will iterate over every possible "window" given the shape of the pattern
    for start_indexes in product(*dimension_iterators):
        #print(start_indexes,pattern_shape,zip(start_indexes, pattern_shape))
        #for start_i, p_s in zip(start_indexes, pattern_shape):
            #print(start_i, p_s)
        range_indexes = [(start_i, start_i + p_s) for start_i, p_s in zip(start_indexes, pattern_shape)]
        #print(range_indexes)
        input_match_candidate = [[0 for x in range(range_indexes[1][0],range_indexes[1][1])] for y in range(range_indexes[0][0],range_indexes[0][1])]
        #print(input_match_candidate)
        for x in range(len(input_match_candidate)):
            xInput = range_indexes[0][0]+x
            for y in range(len(input_match_candidate[0])):
                yInput = range_indexes[1][0]+y
                input_match_candidate[x][y] = input_array[xInput][yInput]
        #print(input_match_candidate)
        #print(input_match_candidate)
        # This checks that for the current "window" - the candidate - every element is equal 
        #  to the pattern OR the element in the pattern is a wildcard
        correct = True
        for x in range(len(input_match_candidate)):
            for y in range(len(input_match_candidate[x])):
                if(pattern[x][y] != input_match_candidate[x][y] and pattern[x][y] != None):
                    correct = False
        if(correct):
            return (start_indexes,pattern)
    return -1

colors = ("No Color", "Red", "Blue", "Green", "Black", "Yellow")



VOLUME = 100


class robot:
    #status Variables
    position = [0,0]
    Clawdir = -1
    lista_lobby = []
    posicao_lobby = 0
    matrix =   [[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]

    #sensors
    resetY_Sensor = None
    chromoSensor = None


    #motors
    claw_Motor = None
    y_Motor = None
    x_Motor1 = None
    x_motor2 = None
    xAxisMotors = None

    def __init__(self):
        self.resetY_Sensor = TouchSensor(Port.S2)
        self.chromoSensor = ColorSensor(Port.S1)
        self.claw_Motor = Motor(Port.A)

        self.y_Motor = Motor(Port.B)

        self.x_Motor1 = Motor(Port.C)
        self.x_Motor1.set_run_settings(200, 100)
        self.x_Motor2 = Motor(Port.D)
        self.x_Motor2.set_run_settings(200, 100)

        self.xAxisMotors = DriveBase(self.x_Motor1,self.x_Motor2,50,100)


        self.reset()

    def reset_Claw(self):
        self.claw_Motor.run_until_stalled(1000,Stop.BRAKE,38)
        self.claw_Motor.run_time(5500*-1, 1700,Stop.BRAKE)
        self.Clawdir = -1

    def reset_YAxis(self):
        self.y_Motor.run(300)
        while (self.resetY_Sensor.pressed()== False):
            wait(10)
        self.y_Motor.stop()

    def reset(self):
        self.reset_Claw()
        self.reset_YAxis()
        print("done reset")

    def toggleClaw(self):
        self.claw_Motor.run_time(5500*self.Clawdir,1300,Stop.BRAKE)
        self.Clawdir = -self.Clawdir

    def yAxis(self,pos):
        self.y_Motor.run_angle(100,-217.7*pos,Stop.BRAKE,True)

    def xAxis(self,pos,dir):
        self.xAxisMotors.drive_time(dir*18.75, 0, 1000*pos*4)
    
    def moveTo(self,xPos,yPos,resetY=True):
        dir = 1
        if(resetY):
            self.reset_YAxis()
        if(xPos - self.position[0]<0):
            dir = -1
        self.xAxis(abs(xPos - self.position[0]),dir)
        if(not(resetY)): 
            self.yAxis(yPos - self.position[1])
        else:
            self.yAxis(yPos +0.25)
        self.position[0]= xPos
        self.position[1]= yPos
    
    def moveToLobby(self,pos,resetY = True):
        if(pos%5==0):
            resetY = True
        self.moveTo(pos//5+5,pos%5,resetY)

    def moveToGame(self,xPos,yPos):
        if(xPos>4 or yPos>4):
            quit()
        self.moveTo(xPos,yPos,True)

    def readColor(self):
        while(True):
            tempList = []
            for x in range(10):
                wait(200)
                tempList += [self.testecor(self.chromoSensor.rgb())]
            tempList = list(dict.fromkeys(tempList))
            print(tempList)
            if(len(tempList)==1):
                if(tempList[0]!=0):
                    return tempList[0]

    def readLobby(self):
        pos = 0
        self.moveToLobby(pos,True)
        while(len(self.lista_lobby)==0 or self.lista_lobby[-1]!=5): #le as peças ate ler amarelo
            self.lista_lobby.append(self.readColor())
            print(self.lista_lobby[:-1])
            pos+=1
            if(self.lista_lobby[-1]!=5):
                self.moveToLobby(pos,False)
        self.lista_lobby = self.lista_lobby[:-1]
        self.reset_YAxis()
        countOfChars = {i:self.lista_lobby.count(i) for i in self.lista_lobby}
        print(countOfChars)
        global pecasExistentes
        global pecasExistentesOld
        pecasExistentes += [countOfChars[1]]
        pecasExistentes += [countOfChars[2]]
        pecasExistentes += [countOfChars[3]]
        pecasExistentes += [countOfChars[4]]
        pecasExistentesOld = pecasExistentes.copy()
        print(self.lista_lobby)

    def testecor(self,a):
        #print(a)
        if(a[0]>a[1]+a[2] and a[0]+a[1]+a[2]>25):
            return 1 #vermelho
        elif(a[2]> a[0]+a[1] and a[0]+a[1]+a[2]>25):
            return 2 #azul
        elif(a[0]+a[1]+a[2]<70):
            temp = self.chromoSensor.color()
            if(temp==3):
                return 3 #verde
            elif(temp==1):
                return 4 #preto
            else:
                return 0 #sem cor
        elif(a[0]+a[1]+a[2]<180):
            return 5 #amarelo
    
    def checkFigure(self):
        for pattern in figureSequence:
            result = match_pattern(self.matrix,globals()[pattern])
            #print(result)
            print(self.matrix)
            if(result != -1):
                for x in range(len(result[1])):
                    for y in range(len(result[1][x])):
                        if(result[1][x][y]==self.matrix[x+result[0][0]][y+result[0][1]]):
                            pecasExistentes[result[1][x][y]-1] -= 1
                            self.matrix[x+result[0][0]][y+result[0][1]] = 0
                brick.sound.file(SoundFile.DETECTED,VOLUME)
                brick.display.text(pattern)
                block = True
                while(block):
                    if Button.CENTER in brick.buttons():
                        block = False
                    wait(10)
    
    def movePieceTo(self, xPos, yPos):
        self.moveToLobby(self.posicao_lobby)
        self.matrix[xPos][yPos] = self.lista_lobby[self.posicao_lobby]
        self.posicao_lobby += 1
        self.toggleClaw()
        self.moveToGame(xPos,yPos)
        self.claw_Motor.run_time(1000,1000,Stop.BRAKE)
        self.reset_YAxis()
        self.reset_Claw()
        self.checkFigure()



    
    


brick.sound.beep()




random.seed(int(time()))
clangy = robot()

#print(match_pattern(clangy.matrix, globals()["sminus"]))
#clangy.checkFigure()
#clangy.reset_Claw()
clangy.readLobby()

for color in clangy.lista_lobby:
   wait(10)
   if color == 1:
       brick.sound.file(SoundFile.RED,VOLUME)
   if color == 2:
       brick.sound.file(SoundFile.BLUE,VOLUME) 
   if color == 3:
       brick.sound.file(SoundFile.GREEN,VOLUME) 
   if color == 4:
       brick.sound.file(SoundFile.BLACK,VOLUME)
   if color == 5:
       brick.sound.file(SoundFile.YELLOW,VOLUME)

#clangy.moveToGame(0,0)

# while(block):
#     if Button.CENTER in brick.buttons():
#         block = False
#     wait(10)
if(heur==1):
    print("hello?")
    print(clangy.lista_lobby)
    for i in range(len(clangy.lista_lobby)):
        if(i%5 == 0):
            clangy.moveToGame(0,0)
            brick.sound.file(SoundFile.HELLO)
            block = True
            while(block):
                if Button.CENTER in brick.buttons():
                    block = False
                wait(10)
            wait(500)
        found = False
        for mapX in range(len(mapheur1)):
            for mapY in range(len(mapheur1[0])):
                if(mapheur1[mapX][mapY] == clangy.lista_lobby[clangy.posicao_lobby] and clangy.matrix[mapX][mapY] == 0):
                    found = True
                    #print(pecasExistentes)
                    clangy.movePieceTo(mapX,mapY)
                    break
            if(found):
                break



if(heur == 2):
    for i in range(len(clangy.lista_lobby)):
        found = False
        if(i%5 == 0):
            clangy.moveToGame(0,0)
            brick.sound.file(SoundFile.HELLO)
            block = True
            while(block):
                if Button.CENTER in brick.buttons():
                    block = False
                wait(10)
            wait(500)
        sortBySymbol(clangy.lista_lobby[clangy.posicao_lobby])
        for x in allPoints:
            if(clangy.matrix[x[0]][x[1]] == 0):
                clangy.movePieceTo(x[0],x[1])
                printMatrix(clangy.matrix)
                found = True
                break




#for i in range(len(clangy.lista_lobby)):
# #for i in range(2):
#    getting = True
#    xPos = 0
#    yPos = 0
#    if(i%5 == 0):
#        clangy.moveToGame(0,0)
#        brick.sound.file(SoundFile.HELLO)
#        block = True
#        while(block):
#            if Button.CENTER in brick.buttons():
#                block = False
#            wait(10)
#        wait(500)

#    while(getting):
#       xPos = random.randint(0,4)
#       yPos = random.randint(0,4)
#       if(clangy.matrix[xPos][yPos] == 0):
#           getting = False
#    clangy.movePieceTo(xPos,yPos)
    #clangy.movePieceTo(clangy.posicao_lobby//5,clangy.posicao_lobby%5)


#clangy.moveToLobby(0)
#clangy.toggleClaw()
#clangy.moveToGame(1,3)
#clangy.toggleClaw()
#for x in range(10):
#    positionGame = [random.randint(0,4),random.randint(0,4)]
#    print(positionGame)
#    clangy.moveToGame(positionGame[0],positionGame[1])
#    positionLobby = random.randint(0,10)
#    print(positionLobby)
#    clangy.moveToLobby(positionLobby)




    #.run_time(250,2000,Stop.BRAKE)




    
    #xAxisMotors.run_angle(200,-270*pos,Stop.BRAKE,True)
    #x_Motor1.run_angle(200,-270*pos,Stop.BRAKE,False)
    #x_Motor2.run_angle(200,-270*pos,Stop.BRAKE,True)

#reset()
#yAxis()
#toggleClaw()
#yAxis(0.5)
#toggleClaw()
#xAxis(4)
#xAxis(5,-1)
#toggleClaw()
#
#toggleClaw()
#while(1):
#    temp = readColor()
#    if(temp != None):
#        brick.display.clear()
#        brick.display.text(temp, (0, 20))
#    wait(1000)


    
#for x in range(20):
#    xAxis(1)
#    xAxis(-1)
