
from random import seed
from random import randint


symbolcross = 1 #red
symbolcircle = 2    #blue
symbolplus = 3  #green
symbolminus = 4 #black


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

def getPriorityRank(symbol):
  #print(str(symbol), "peças: ", pecasExistentes[symbol-1] )
  if(pecasExistentes[symbol-1]/pecasRequeridasMax[symbol-1]>=1 and symbol != 2):
    return 2
  elif(pecasExistentes[symbol-1]/pecasRequeridasMin[symbol-1]>=1):
    return 1
  else:
    return 0






#função produto
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





#função para encontrar padrões
def match_pattern(input_array, pattern, wildcard_function=None):
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
        range_indexes = [(start_i, start_i + p_s) for start_i, p_s in zip(start_indexes, pattern_shape)]
        input_match_candidate = [[0 for x in range(range_indexes[1][0],range_indexes[1][1])] for y in range(range_indexes[0][0],range_indexes[0][1])]
        for x in range(len(input_match_candidate)):
            xInput = range_indexes[0][0]+x
            for y in range(len(input_match_candidate[0])):
                yInput = range_indexes[1][0]+y
                input_match_candidate[x][y] = input_array[xInput][yInput]
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

class game:
    lista_lobby = []
    posicao_lobby = 0
    matrix =   [[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]

    def __init__(self):
        printMatrix(self.matrix)
        #self.lista_lobby = [2, 1, 4, 1, 4, 4, 1, 4, 4, 3, 2, 1, 4, 1, 4, 2, 3, 3, 1, 3, 4, 1, 1, 2, 3, 4, 4, 1, 1, 3, 2]
        for _ in range(125):
            self.lista_lobby += [randint(1,4)]
        print(tuple(map(lambda x: symbols[x],self.lista_lobby)))
        print(self.lista_lobby)
        countOfChars = {i:self.lista_lobby.count(i) for i in self.lista_lobby}
        print(countOfChars)
        global pecasExistentes
        global pecasExistentesOld
        pecasExistentes += [countOfChars[1]]
        pecasExistentes += [countOfChars[2]]
        pecasExistentes += [countOfChars[3]]
        pecasExistentes += [countOfChars[4]]
        pecasExistentesOld = pecasExistentes.copy()


    def checkFigure(self):
        for pattern in figureSequence:
            result = match_pattern(self.matrix,globals()[pattern])
            if(result != -1):
                globals()["score"] += globals()[pattern + "p"]
                #print(pattern)
                for x in range(len(result[1])):
                    for y in range(len(result[1][x])):
                        if(result[1][x][y]==self.matrix[x+result[0][0]][y+result[0][1]]):
                            pecasExistentes[result[1][x][y]-1] -= 1
                            self.matrix[x+result[0][0]][y+result[0][1]] = 0
    
    def insertPiece(self, xPos,yPos):
        self.matrix[xPos][yPos] = self.lista_lobby[self.posicao_lobby]
        self.posicao_lobby += 1
        self.checkFigure()


#seed(1)

temp = game()
#if(heur == 1):
temp.posicao_lobby = 0
temp.matrix =   [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]
score = 0
for i in range(len(temp.lista_lobby)):
    found = False
    for mapX in range(len(mapheur1)):
      for mapY in range(len(mapheur1[0])):
        if(mapheur1[mapX][mapY] == temp.lista_lobby[temp.posicao_lobby] and temp.matrix[mapX][mapY] == 0):
          found = True
          #print(pecasExistentes)
          temp.insertPiece(mapX,mapY)
          break
      if(found):
        break
print(score)


pecasExistentes = pecasExistentesOld
print(pecasExistentes)
#if(heur == 2):
print(temp.lista_lobby)
temp.posicao_lobby = 0
temp.matrix =   [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]
score = 0
for i in range(len(temp.lista_lobby)):
  found = False
  sortBySymbol(temp.lista_lobby[temp.posicao_lobby])
  
  for x in allPoints:
    if(temp.matrix[x[0]][x[1]] == 0):
      temp.insertPiece(x[0],x[1])
      #printMatrix(temp.matrix)
      found = True
      break
    
    
print(temp.lista_lobby[temp.posicao_lobby:])
      
print(score)
printMatrix(temp.matrix)

