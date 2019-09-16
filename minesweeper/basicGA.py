import baseGeneticAlgorithm
import random
import time
import copy

LOSE = 0
WIN = 1
CONTINUE = 2

class basicGA(baseGeneticAlgorithm.baseGeneticAlgorithm):
    def __init__(self, boardWidth = 5, boardHeight = 5, bombs = 10, populationSize = 100, generationCount = 100, crossoverRate = .75, mutationRate = .05):
        super(basicGA,self).__init__(boardWidth,boardHeight,bombs,populationSize,generationCount,crossoverRate,mutationRate)

    def fitnessFunction(self, solution):
        score, x_cord, y_cord = 0, 0, 0

        # Iterates through solution and provides corresponding score
        for node in solution:
            if self.board[y_cord][x_cord] == 0 and node == 0:   # Node in chromosome matches the board
                score = score + 1
            if self.board[y_cord][x_cord] == 1 and node == 1:   # Node in chromosome matches the board
                score = score + 2
            elif node == 0 and self.board[y_cord][x_cord] == 1:    # Mistakes empty tile for bomb tile - loss
                score = score - 10
                # return score + self.checkBombLocation(solution, x_cord, y_cord) - 10    # If the string ends early, add correct bomb location guesses to the score
            elif node == 1 and self.board[y_cord][x_cord] == 0:   # Mistakes bomb tile for empty tile - minus 1pt
                score = score - 5

            # Iterates to the next coordinate on the board
            if x_cord < self.boardWidth - 1:
                x_cord = x_cord + 1
            elif y_cord < self.boardHeight - 1:
                x_cord = 0
                y_cord = y_cord + 1

        return score

    def checkBombLocation(self, solution, x_cord, y_cord):
        """
            Continues where the last iteration left off. +2pts for every correct bomb location
        """
        score = 0
        x_cord = x_cord
        y_cord = y_cord

        num = (y_cord * self.boardWidth) + x_cord
        for node in solution[num:]:
            if node == 1:
                if node == self.board[y_cord][x_cord]:
                    score = score + 2
            if x_cord < self.boardWidth - 1:
                x_cord = x_cord + 1
            elif y_cord < self.boardHeight - 1:
                x_cord = 0
                y_cord = y_cord + 1
        return score

    def setMaxFitness(self):
        """
            1pt for correct empty tile guess
            2pts for every correct bomb guess
            -1pt for every incorrect flag
        """
        #self.maxFitness = self.boardHeight * self.boardWidth + self.bombs
        #self.maxFitness = self.bombs * 2
        self.maxFitness = (self.boardHeight * self.boardWidth) + self.bombs

    def parentSelection(self):
        '''
        Need to implement:
            Takes in list of tuples of form (chromosome, fitness)
            returns tuple of form (parentChromosome1, parentChromosome2)
        '''
        
        parList = [] 
        iters = self.populationSize // 10
        if iters < 2:
            iters = 2
        for i in range(iters):
            parList.append(self.popFitness[random.randint(0,self.populationSize - 1)])       
        parent1 = max(parList, key=lambda item:item[1])
        parList = []
        for i in range(iters):
            parList.append(self.popFitness[random.randint(0,self.populationSize - 1)]) 
        parent2 = max(parList, key=lambda item:item[1])
        return (parent1[0],parent2[0])
        
        '''
        copiedList = copy.deepcopy(sortedTuples)
        parent1 = max(copiedList, key=lambda item:item[1])
        copiedList.remove(parent1)
        parent2 = max(copiedList, key=lambda item:item[1])
        '''
        #return (parent1[0],parent2[0])

    def crossoverAlg(self, parents):
        '''
        Need to implement:
            Takes in a tuple of form (parentChromosome1, parentChromosome2)
            Returns a tuple of form (childChromsome1, childChromsome2)
        '''
        pars = copy.deepcopy(parents)
        #pars1 = copy.deepcopy(parents)
        parent1 = pars[0]
        parent2 = pars[1]

        usedPoints = set()
        iters = self.bombs // 2
        if iters < 1:
            iters = 1
        for i in range(iters):
            crossPoint1 = random.randint(0, self.bombs - 1)
            crossPoint2 = random.randint(0, self.bombs - 1)
           

            old_idx_1 = (parent1[1])[crossPoint1]
            old_idx_2 = (parent2[1])[crossPoint2]
            if (parent1[0])[old_idx_2] == 0:
                (parent1[0])[old_idx_1] = 0
                (parent1[1])[crossPoint1] = old_idx_2
                (parent1[0])[old_idx_2] = 1

            if (parent2[0])[old_idx_1] == 0:
                (parent2[0])[old_idx_2] = 0
                (parent2[1])[crossPoint2] = old_idx_1
                (parent2[0])[old_idx_1] = 1

        return (parent1,parent2)

    def mutationAlg(self, children):
        '''
        Need to implement:
            Updates current population according in desired manner
        '''

        threshhold = self.mutationRate * 1000
        for child in children:
            for i in range(len(child[1])):
                if random.randint(0,1000) < threshhold:
                    cur_idx = (child[1])[i]
                    new_idx = random.randint(0,len(child[0]) - 1)
                    if (child[0])[new_idx] != 1:
                        (child[0])[new_idx] = 1
                        (child[0])[cur_idx] = 0
                        (child[1])[i] = new_idx
                        
    def replacement(self, children):
        child1 = children[0]
        child2 = children[1]
        
        child1 = (child1, self.fitnessFunction(child1[0]))
        child2 = (child2, self.fitnessFunction(child2[0]))
        
        min_el = min(self.popFitness, key=lambda item:item[1])
        if min_el[1] < child1[1]:
            min_idx = self.popFitness.index(min_el)
            self.popFitness[min_idx] = child1
        
        min_el = min(self.popFitness, key=lambda item:item[1])
        if min_el[1] < child2[1]:
            min_idx = self.popFitness.index(min_el)
            self.popFitness[min_idx] = child2





if __name__ == '__main__':
    random.seed(time.time())
    import code; code.interact(banner='', local = locals())
