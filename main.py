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




#relação de cores com o simbolos
symbolcross = 1 #red
symbolcircle = 2 #blue
symbolplus = 3  #green
symbolminus = 4 #black







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
  allPoints = sorted(allPoints, key=lambda t: sortF(t,symbol,rank), reverse=False)

score = 0



def getPriorityRank(symbol):
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


#função desenha a matrix
def printMatrix(matrix):
    text = "-----\n"
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            text += symbols[int(matrix[x][y])]
        text = text + "\n"
    print(text)



# Colors: (0:No Color, 1:Black, 2:Blue, 3:Green, 4:Yellow, 5:Red, 6:White, 7:Brown)



#função para encontrar padrão numa matrix
def match_pattern(input_array, pattern, wildcard_function=None):

    pattern_shape = (len(pattern),len(pattern[0]))
    input_shape = (len(input_array),len(input_array[0]))

    #verifica se as duas matrizes tem as mesmas dimensões
    if len(pattern_shape) != len(input_shape):
        raise ValueError("Input array and pattern must have the same dimension")

    shape_difference = [i_s - p_s for i_s, p_s in zip(input_shape, pattern_shape)]

    #verifica se o comprimento da matrix e superior ao do padrão
    if any((diff < -1 for diff in shape_difference)):
        raise ValueError("Input array cannot be smaller than pattern in any dimension")

    dimension_iterators = [range(0, s_diff + 1) for s_diff in shape_difference]

    # iteração sobre todas as possiveis possições do padrão na matrix
    for start_indexes in product(*dimension_iterators):

        range_indexes = [(start_i, start_i + p_s) for start_i, p_s in zip(start_indexes, pattern_shape)]

        input_match_candidate = [[0 for x in range(range_indexes[1][0],range_indexes[1][1])] for y in range(range_indexes[0][0],range_indexes[0][1])]
        
        for x in range(len(input_match_candidate)):
            xInput = range_indexes[0][0]+x
            for y in range(len(input_match_candidate[0])):
                yInput = range_indexes[1][0]+y
                input_match_candidate[x][y] = input_array[xInput][yInput]

        #verifica se todos os valores coincidem ou são a wildcard do padrão na matrix
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

#classe do robot
class robot:
    #variaveis principais
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

    #função de inicialização do robo
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

    #metodo para resetar a garra
    def reset_Claw(self):
        self.claw_Motor.run_until_stalled(1000,Stop.BRAKE,38)
        self.claw_Motor.run_time(5500*-1, 1700,Stop.BRAKE)
        self.Clawdir = -1

    #metodo para resetar o eixo do Y
    def reset_YAxis(self):
        self.y_Motor.run(300)
        while (self.resetY_Sensor.pressed()== False):
            wait(10)
        self.y_Motor.stop()

    #metodo para combinar ambos os resets anteriores
    def reset(self):
        self.reset_Claw()
        self.reset_YAxis()
        print("done reset")

    #metodo para abrir e fechar a garra
    def toggleClaw(self):
        self.claw_Motor.run_time(5500*self.Clawdir,1300,Stop.BRAKE)
        self.Clawdir = -self.Clawdir

    #metodo para o movimento no eixo dos Y
    def yAxis(self,pos):
        self.y_Motor.run_angle(100,-217.7*pos,Stop.BRAKE,True)

    #metodo para o movimento no eixo dos X
    def xAxis(self,pos,dir):
        self.xAxisMotors.drive_time(dir*18.75, 0, 1000*pos*4)
    
    #combinação de ambos os metodos anteriores
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
    
    #metodo para o movimento no lobby onde lê as peças
    def moveToLobby(self,pos,resetY = True):
        if(pos%5==0):
            resetY = True
        self.moveTo(pos//5+5,pos%5,resetY)

    #metodo para o movimento dentro do campo de jogo
    def moveToGame(self,xPos,yPos):
        if(xPos>4 or yPos>4):
            quit()
        self.moveTo(xPos,yPos,True)

    #metodo para ler a cor repitindo 10 vezes
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

    #metodo para testar a cor individualmente
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

    #metodo que combina o movimento e a leitura de cores para ler todo o lobby
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

    #metodo que verifica se uma figura foi feita
    def checkFigure(self):
        #itera sobre todos os padrões e verifica se existe algum
        for pattern in figureSequence:
            result = match_pattern(self.matrix,globals()[pattern])
            print(self.matrix)
            if(result != -1):
                globals()["score"] += globals()[pattern + "p"]
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

    #metodo que combina os metodos anteriores para mover uma peça para uma posição especifica
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



    
    

heur = 1

brick.sound.beep()


#seleção da heuristica
block = True
brick.display.text("direita heur 1", (0, 20))
brick.display.text("esquerda heur 2", (0, 40))
while(block):
    if Button.RIGHT in brick.buttons():
        heur = 1
        block = False
    if Button.LEFT in brick.buttons():
        heur = 2
        block = False
    wait(10)


#inicialização do robo
random.seed(int(time()))
clangy = robot()


clangy.readLobby()

#listagem das figuras
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




#execução da heuristica 1
if(heur==1):
    print(clangy.lista_lobby)
    for i in range(len(clangy.lista_lobby)):
        #verifica se esta na altura de o robo fazer reset
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
        #procura de um expaço vazio para colocar a figura
        for mapX in range(len(mapheur1)):
            for mapY in range(len(mapheur1[0])):
                if(mapheur1[mapX][mapY] == clangy.lista_lobby[clangy.posicao_lobby] and clangy.matrix[mapX][mapY] == 0):
                    found = True
                    clangy.movePieceTo(mapX,mapY)
                    break
            if(found):
                break


#execução da heuristica 2 
if(heur == 2):
    for i in range(len(clangy.lista_lobby)):
        
        #verifica se esta na altura de o robo fazer reset
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
        #encontrar a posição para colocar a proxima peça
        sortBySymbol(clangy.lista_lobby[clangy.posicao_lobby])
        for x in allPoints:
            if(clangy.matrix[x[0]][x[1]] == 0):
                clangy.movePieceTo(x[0],x[1])
                printMatrix(clangy.matrix)
                found = True
                break

brick.display.clear()
brick.display.text(score, (0, 20))

while(block):
    if Button.CENTER in brick.buttons():
        block = False
    wait(10)
wait(500)
