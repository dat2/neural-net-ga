import numpy as np
np.random.seed(300)

INPUTS = 4
HIDDEN = 6
OUTPUTS = 2

from genetic_algorithm import GeneticAlgorithm

g = GeneticAlgorithm(20, 0.7, 0.01, [INPUTS, HIDDEN, OUTPUTS])

g.make_new_generation()

import game
