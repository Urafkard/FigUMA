#!/usr/bin/env python3




import ev3dev2
from ev3dev2.motor import LargeMotor,MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent,SpeedRPM, MoveTank
from ev3dev2.senosr import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from ev3dev2.sound import Sound

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


#patterns
#  MINUSES
sminus = [[symbolminus,symbolminus]]

bminus = [[symbolminus,symbolminus,symbolminus]]

#  PLUS
splus = [[None,symbolplus,None],
       [symbolplus,symbolplus,symbolplus],
       [None,symbolplus,None]]

bplus = [[None,None,symbolplus,None,None],
        [None,None,symbolplus,None,None],
        [symbolplus,symbolplus,symbolplus,symbolplus,symbolplus],
        [None,None,symbolplus,None,None],
        [None,None,symbolplus,None,None]]

#  CROSS
scross = [[symbolcross,None,symbolcross],
       [None,symbolcross,None],
       [symbolcross,None,symbolcross]]

bcross = [[symbolcross,None,None,None,symbolcross],
        [None,symbolcross,None,symbolcross,None],
        [None,None,symbolcross,None,None],
        [None,symbolcross,None,symbolcross,None],
        [symbolcross,None,None,None,symbolcross]]

#  CIRCLE
scircle = [[symbolcircle,symbolcircle],
         [symbolcircle,symbolcircle]]

mcircle1 = [[symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle]]

mcircle2 = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,None,symbolcircle],
          [symbolcircle,None,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle,symbolcircle]]

bcircle = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,None,None,None,symbolcircle],
          [symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle]]

figureSequence = ("bcircle","bcross","bplus","bminus","mcircle2","scross","splus","sminus","mcircle1","scircle")


# Colors: (0:No Color, 1:Black, 2:Blue, 3:Green, 4:Yellow, 5:Red, 6:White, 7:Brown)


def product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

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
        self.resetY_Sensor = TouchSensor(INPUT_2)
        self.chromoSensor = ColorSensor(INPUT_1)
        self.claw_Motor = MediumMotor(OUTPUT_A)

        self.y_Motor = LargeMotor(OUTPUT_B)

        self.xAxisMotors = MotorTank(OUTPUT_C,OUTPUT_D)

        self.reset()

    def reset_Claw(self):
        self.claw_Motor.on(SpeedPercent(10))
        self.claw_Motor.wait_until_not_moving(1000)
        self.claw_Motor.stop()
        self.claw_Motor.on_for_seconds(SpeedPercent(-10),2)
        self.Clawdir = -1

    def reset_YAxis(self):
        self.y_Motor.on(SpeedRPM(200))
        self.resetY_Sensor.wait_for_pressed()
        self.y_Motor.stop()

    def reset(self):
        self.reset_Claw()
        self.reset_YAxis()
        print("done reset")

    def toggleClaw(self):
        self.claw_Motor.on_for_seconds(SpeedRPM(200*self.Clawdir),1)
        self.Clawdir = -self.Clawdir

    def yAxis(self,pos):
        self.y_Motor.run_angle(SpeedRPM(200),-217.7*pos)

    def xAxis(self,pos,dir):
        self.xAxisMotors.on_for_degrees(SpeedPercent(10*dir),75*pos)
    
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
                            self.matrix[x+result[0][0]][y+result[0][1]] = 0
                Sound.speak(pattern)
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
        self.claw_Motor.on_for_seconds(SpeedPercent(10),1)
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
   wait(200)
   if color == 1:
       Sound.speak("RED")
   if color == 2:
       Sound.speak("BLUE")
   if color == 3:
       Sound.speak("GREEN")
   if color == 4:
       Sound.speak("BLACK")
   if color == 5:
       Sound.speak("YELLOW")

#clangy.moveToGame(0,0)

# while(block):
#     if Button.CENTER in brick.buttons():
#         block = False
#     wait(10)

for i in range(len(clangy.lista_lobby)):
# #for i in range(2):
    getting = True
    xPos = 0
    yPos = 0
    if(i%5 == 0):
        clangy.moveToGame(0,0)
        Sound.speak("Reset me")
        block = True
        while(block):
            if Button.CENTER in brick.buttons():
                block = False
            wait(10)
        wait(500)

    while(getting):
       xPos = random.randint(0,4)
       yPos = random.randint(0,4)
       if(clangy.matrix[xPos][yPos] == 0):
           getting = False
    clangy.movePieceTo(xPos,yPos)
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
