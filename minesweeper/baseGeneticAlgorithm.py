import copy
import time
import random
import matplotlib.pyplot as plt
import numpy as np

from msgame import MSGame

class baseGeneticAlgorithm(object):
    def __init__(self, boardWidth = 16, boardHeight = 30, bombs = 99, populationSize = 100, generationCount = 100, crossoverRate = .75, mutationRate = .05):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.bombs = bombs
        self.populationSize = populationSize
        self.generationCount = generationCount
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate

        self.staticGame = MSGame(boardWidth, boardHeight, bombs)
        self.board = self.staticGame.get_mine_map()

        self.maxResults = []
        self.avgResults = []

        self.population = self.generatePopulation(populationSize, boardHeight * boardWidth, bombs)
        self.setMaxFitness()

    def generateChromosome(self, boardSize, bombCount):
        ret = [0] * boardSize
        bomb_idxs = []
        for i in range(bombCount):
            bomb_idx = random.randint(0, boardSize - 1)
            while ret[bomb_idx] == 1:
                bomb_idx = random.randint(0, boardSize - 1)
            ret[bomb_idx] = 1
            bomb_idxs.append(bomb_idx)
        return (ret, bomb_idxs)

    def generatePopulation(self, popSize, boardSize, bombCount):
        ret = []
        for i in range(popSize):
            ret.append(self.generateChromosome(boardSize, bombCount))
        return ret

    def fitnessFunction(self, solution):
        '''
        Need to implement:
            Takes in a particular solution string and a board to evaluate.
            determines fitness of solution and returns fitness values
        '''
        game = copy.deepcopy(self.staticGame)
        return 0

    def getFitnessVals(self):
        ret = []
        for chromosome in self.population:
            ret.append(self.fitnessFunction(chromosome[0]))
        return ret

    def setMaxFitness(self):
        '''
        Needs to be implemented:
            Needs to set maximum fitness value according to whatever fitness algorithm is being used
        '''
        self.maxFitness = float('inf')

    def mutationAlg(self, children):
        '''
        Need to implement:
            Updates current population according in desired manner
        '''
        pass

    def getMaxChromosome(self, tupleList):
        maxVal = None
        for item in tupleList:
            if maxVal is None or maxVal < item[1]:
                maxChromosome = item[0]
                maxVal = item[1]
        return maxChromosome[0]

    def parentSelection(self, sortedTuples):
        '''
        Need to implement:
            Takes in list of tuples of form (chromosome, fitness)
            returns tuple of form (parentChromosome1, parentChromosome2)
        '''
        return ((sortedTuples[0])[0], (sortedTuples[1])[0])

    def crossoverAlg(self, parents):
        '''
        Need to implement:
            Takes in a tuple of form (parentChromosome1, parentChromosome2)
            Returns a tuple of form (childChromsome1, childChromsome2)
        '''
        return parents

    def replacement(self, children):
        pass

    def recombination(self, tupleList):
        #Sort according to fitness
        sortedTuples = sorted(tupleList, key=lambda item: item[1], reverse=True)

        childCount = int(self.crossoverRate * self.populationSize)
        if childCount % 2 == 1:
            childCount -= 1
        children = []
        for i in range(childCount // 4):
            parents = self.parentSelection(sortedTuples)
            newChildren = self.crossoverAlg(parents)
            children.append(copy.deepcopy(newChildren[0]))
            children.append(copy.deepcopy(newChildren[1]))

        # RIGHT NOW, SURVIVOR SELECTION ALWAYS CHOOSES MOST FIT
        # MAY WANT TO IMPLEMENT SEPERATE ALGORITHMS IN FUTURE
        x,y = (zip(*sortedTuples))

        return list(x)[:self.populationSize - childCount] + children

    def getAvgFitnessValue(self, fitnessSum):
        return fitnessSum / self.populationSize

    def graphResults(self, maxResults, avgResults):
        plt.plot(maxResults, xrange(self.generationCount))
        plt.ylabel("Fitness Score")
        plt.xlabel("Generations")
        plt.show()

    def runEpoch(self):
        finalChromosome = None
        fitnesses = self.getFitnessVals()
        self.popFitness = list(zip(self.population, fitnesses))
        for generation_idx in range(self.generationCount):
            for i in range(25):
                parents = self.parentSelection()
                children = self.crossoverAlg(parents)
                self.mutationAlg(children)
                self.replacement(children)
            max_fit = max(list(zip(*self.popFitness))[1])
            self.maxResults.append(max_fit)
            self.avgResults.append(self.getAvgFitnessValue(sum(list(zip(*self.popFitness))[1])))

            print(max_fit)
            if self.maxFitness == max_fit:
                break

        self.graphResults(self.maxResults, self.avgResults)
        finalChromosome = self.getMaxChromosome(self.popFitness)
        return finalChromosome

if __name__ == '__main__':
    random.seed(time.time())
    import code; code.interact(banner='', local = locals())
