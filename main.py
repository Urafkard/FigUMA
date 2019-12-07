#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here

#patterns
#   MINUSES
#sminus = [[symbolminus,symbolminus]]
#
#bminus = [[symbolminus,symbolminus,symbolminus]]
#
#   PLUS
#splus = [['nan',symbolplus,'nan'],
#        [symbolplus,symbolplus,symbolplus],
#        ['nan',symbolplus,'nan']]
#
#bplus = [['nan','nan',symbolplus,'nan','nan'],
#         ['nan','nan',symbolplus,'nan','nan'],
#         [symbolplus,symbolplus,symbolplus,symbolplus,symbolplus],
#         ['nan','nan',symbolplus,'nan','nan'],
#         ['nan','nan',symbolplus,'nan','nan']]
#
#   CROSS
#scross = [[symbolcross,'nan',symbolcross],
#        ['nan',symbolcross,'nan'],
#        [symbolcross,'nan',symbolcross]]
#
#bcross = [[symbolcross,'nan','nan','nan',symbolcross],
#         ['nan',symbolcross,'nan',symbolcross,'nan'],
#         ['nan','nan',symbolcross,'nan','nan'],
#         ['nan',symbolcross,'nan',symbolcross,'nan'],
#         [symbolcross,'nan','nan','nan',symbolcross]]
#
#   CIRCLE
#scircle = [[symbolcircle,symbolcircle],
#          [symbolcircle,symbolcircle]]
#
#mcircle1 = [[symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle]]
#
#mcircle2 = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan','nan',symbolcircle],
#           [symbolcircle,'nan','nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle,symbolcircle]]
#
#bcircle = [[symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle],
#           [symbolcircle,'nan','nan','nan',symbolcircle],
#           [symbolcircle,'nan','nan','nan',symbolcircle],
#           [symbolcircle,symbolcircle,symbolcircle,symbolcircle,symbolcircle]]
#
#
# Colors: (0:No Color, 1:Black, 2:Blue, 3:Green, 4:Yellow, 5:Red, 6:White, 7:Brown)









brick.sound.beep()

#brick.sound.speak('Bo!')

resetY_Sensor = TouchSensor(Port.S2)

figureSensor = ColorSensor(Port.S1)

claw_Motor = Motor(Port.A)
y_Motor = Motor(Port.B)

x_Motor1 = Motor(Port.C)
x_Motor1.set_run_settings(200, 100)
x_Motor2 = Motor(Port.D)
x_Motor2.set_run_settings(200, 100)

xAxisMotors = DriveBase(x_Motor1,x_Motor2,100,100)


Clawdir = -1



def reset():
    print(y_Motor.angle())
    claw_Motor.run_until_stalled(1000,Stop.BRAKE,30)
    y_Motor.run(300)
    while (resetY_Sensor.pressed()== False):
        wait(10)
    y_Motor.stop()
    print("done reset")

def toggleClaw():
    global Clawdir
    #claw_Motor.run_until_stalled(100000*Clawdir,Stop.BRAKE,30)
    claw_Motor.run_time(5500*Clawdir,2250,Stop.BRAKE)
    Clawdir = -Clawdir

def yAxis(pos):
    y_Motor.run_angle(100,-217.7*pos,Stop.BRAKE,True)
    #.run_time(250,2000,Stop.BRAKE)

def readColor():
    return figureSensor.color()

def xAxis(pos):
    xAxisMotors.drive_time(500*pos, 0, 1000)
    
    #xAxisMotors.run_angle(200,-270*pos,Stop.BRAKE,True)
    #x_Motor1.run_angle(200,-270*pos,Stop.BRAKE,False)
    #x_Motor2.run_angle(200,-270*pos,Stop.BRAKE,True)

reset()
#yAxis()
#toggleClaw()
#yAxis(1)

#xAxis(4)


#toggleClaw()
while(1):
    temp = readColor()
    if(temp != None):
        brick.sound.beeps(temp)
    wait(1000)

#for x in range(20):
#    xAxis(1)
#    xAxis(-1)
