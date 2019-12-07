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
#import numpy as np


#password maker
# Write your program here

#patterns
#   MINUSES
#sminus = numpy.array([[symbolminus,symbolminus]])
#
#bminus = numpy.array([[symbolminus,symbolminus,symbolminus]])
#
#   PLUS
#splus = numpy.array([['nan',symbolplus,'nan'],
#        [symbolplus,symbolplus,symbolplus],
#        ['nan',symbolplus,'nan']])
#
#bplus = numpy.array([['nan','nan',symbolplus,'nan','nan'],
#         ['nan','nan',symbolplus,'nan','nan'],
#         [symbolplus,symbolplus,symbolplus,symbolplus,symbolplus],
#         ['nan','nan',symbolplus,'nan','nan'],
#         ['nan','nan',symbolplus,'nan','nan']])
#
#   CROSS
#scross = numpy.array([[symbolcross,'nan',symbolcross],
#        ['nan',symbolcross,'nan'],
#        [symbolcross,'nan',symbolcross]])
#
#bcross = numpy.array([[symbolcross,'nan','nan','nan',symbolcross],
#         ['nan',symbolcross,'nan',symbolcross,'nan'],
#         ['nan','nan',symbolcross,'nan','nan'],
#         ['nan',symbolcross,'nan',symbolcross,'nan'],
#         [symbolcross,'nan','nan','nan',symbolcross]])
#
#   CIRCLE
#scircle = numpy.array([[symbolcircle,symbolcircle],
#          [symbolcircle,symbolcircle]])
#
#mcircle1 = numpy.array([[symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle]])
#
#mcircle2 = numpy.array([[symbolcircle,symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan','nan',symbolcircle],
#           [symbolcircle,'nan','nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle,symbolcircle]])
#
#bcircle = numpy.array([[symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan','nan','nan',symbolcircle],
#           [symbolcircle,'nan','nan','nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle]])
#
#
# Colors: (0:No Color, 1:Black, 2:Blue, 3:Green, 4:Yellow, 5:Red, 6:White, 7:Brown)


#def match_pattern(input_array, pattern, wildcard_function=np.isnan):
#
#    pattern_shape = pattern.shape
#    input_shape = input_array.shape
#
#    is_wildcard = wildcard_function(pattern) # This gets a boolean N-dim array
#
#    if len(pattern_shape) != len(input_shape):
#        raise ValueError("Input array and pattern must have the same dimension")
#
#    shape_difference = [i_s - p_s for i_s, p_s in zip(input_shape, pattern_shape)]
#
#    if any((diff < -1 for diff in shape_difference)):
#        raise ValueError("Input array cannot be smaller than pattern in any dimension")
#
#    dimension_iterators = [range(0, s_diff + 1) for s_diff in shape_difference]
#
#    # This loop will iterate over every possible "window" given the shape of the pattern
#    for start_indexes in product(*dimension_iterators):
#        range_indexes = [slice(start_i, start_i + p_s) for start_i, p_s in zip(start_indexes, pattern_shape)]
#        input_match_candidate = input_array[range_indexes]
#
#        # This checks that for the current "window" - the candidate - every element is equal 
#        #  to the pattern OR the element in the pattern is a wildcard
#        if np.all(
#            np.logical_or(
#                is_wildcard, (input_match_candidate == pattern)
#            )
#        ):
#            return start_indexes
#
#    return -1

#colors = ("No Color", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown")

class robot:
    #status Variables
    position = [0,0]
    Clawdir = -1

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
        self.claw_Motor.run_until_stalled(1000,Stop.BRAKE,30)
        self.claw_Motor.run_time(5500*-1, 1700,Stop.BRAKE)

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
        self.claw_Motor.run_time(5500*self.Clawdir,1200,Stop.BRAKE)
        self.Clawdir = -self.Clawdir

    def yAxis(self,pos):
        self.y_Motor.run_angle(100,-217.7*pos,Stop.BRAKE,True)

    def readColor(self):
        return self.chromoSensor.rgb()

    def xAxis(self,pos,dir):
        self.xAxisMotors.drive_time(dir*18.75, 0, 1000*pos*4)
    
    def moveTo(self,xPos,yPos):
        dir = 1
        self.reset_YAxis()
        if(xPos - self.position[0]<0):
            dir = -1
        self.xAxis(abs(xPos - self.position[0]),dir)   
        self.yAxis(yPos +0.25)
        self.position[0]= xPos
        self.position[1]= yPos
    
    def moveToLobby(self,pos):
        self.moveTo(pos//5+5,pos%5)

    def moveToGame(self,xPos,yPos):
        if(xPos>4 or yPos>4):
            quit()
        self.moveTo(xPos,yPos)            


    
    


brick.sound.beep()





random.seed(int(time()))
clangy = robot()
clangy.moveToLobby(0)
clangy.toggleClaw()
clangy.moveToGame(1,3)
clangy.toggleClaw()
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
