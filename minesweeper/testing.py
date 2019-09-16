import copy
import time
import random
from msgame import MSGame

height = 16
width = 30
mines = 99

LOSE = 0
WIN = 1
CONTINUE = 2

def generateSolution(boardSize, bombCount):
    ret = [0] * boardSize
    for i in range(bombCount):
        bomb_idx = random.randint(0, boardSize - 1)
        while ret[bomb_idx] == 1:
            bomb_idx = random.randint(0, boardSize - 1)
        ret[bomb_idx] = 1
    return ret

def generatePopulationTest(popSize, boardSize, bombCount):
    ret = []
    for i in range(popSize):
        ret.append(generateSolution(boardSize, bombCount))
    return ret


def timingTest(genCount):
    start = time.time()
    clickAndCopyTest(genCount)
    return time.time() - start

def clickAndCopyTest(genCount = 10000):
    base_game = MSGame(height, width, mines)
    
    x = []
    for i in range(genCount):
        x.append(copy.deepcopy(base_game))
        
    count = 0 
    for game in x:
        for i in range(height):
            for j in range(width):
                game.qplay('click', i, j)
        #print(count)
        #count += 1
        
    print('Done\n')
    return x

if __name__ == '__main__':
    random.seed(time.time())
    import code; code.interact(banner='', local = locals())