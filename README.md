
# Minesweeper-AI

* Minesweeper is a game consisting of a grid with mines hidden amongst the grid. The goal is to uncover all of the empty tiles and flag tiles containing mines. The game is lost when a player clicks on a mine.
* Built and designed an AI agent, using a Genetic Algorithm (GA), which can solve Minesweeper on various board complexities, comparably to other top AI-based Minesweeper solvers.

# Overview of a GA
1. There exists a population consisting of individual members of a specified format used to represent problem.
2. The population is run, individually, against a fitness functoin which rates the “goodness” of an individual member.
3. Crossover selects two high fitness members and produces two combined offspring.
4. Mutation randomly modifies children.
5. Survivor Selection or replacement brings children into population.


# Results
* With a population size as low as 1000 run over 1000 generations, the success rate for different board complexities is as follows:
    * Beginner (9x9 board) - 100%
    * Intermediate (16x16 board) - 73.30%
    * Expert (16x32 board) - 26.70%
