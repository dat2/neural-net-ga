import cocos
import parameters
import numpy as np

from cocos.actions import *
from entities import Tank, Mine
from genetic_algorithm import GeneticAlgorithm

def generate_tanks(n,w,h):
    tanks = []

    for i in range(n):
        tanks.append(Tank( np.random.randint(0,w), np.random.randint(0,h), np.random.randint(0,360), False ))

    return tanks

def generate_mines(n,w,h):
    mines = []

    for i in range(n):
        mines.append(Mine(np.random.randint(0,w), np.random.randint(0,h)))

    return mines

class Main(cocos.layer.ColorLayer):
    def __init__(self):
        # cornflower blue
        super(Main, self).__init__(100, 149, 237, 127)
        self._setup()
        self.schedule(self.step)

    def _setup(self):
        self.mines = generate_mines(parameters.NUM_MINES, 640, 480)
        for mine in self.mines:
            mine.add_to_layer(self)

        self.tanks = generate_tanks(parameters.POPULATION_SIZE, 640, 480)
        for tank in self.tanks:
            tank.add_to_layer(self)

        self.genetic_algorithm = GeneticAlgorithm(parameters.POPULATION_SIZE, parameters.CROSSOVER_RATE, parameters.MUTATION_RATE, [parameters.N_INPUTS, parameters.N_HIDDEN, parameters.N_OUTPUTS])

    def get_nearest_mine_direction(self, tank):
        t = np.array((tank.x, tank.y))

        min_dist = float('inf')
        dir = np.zeros(2)

        for mine in self.mines:
            m = np.array((mine.x, mine.y))
            if np.linalg.norm(m - t) < min_dist:
                min_dist = np.linalg.norm(m - t)
                dir = (m - t) / np.linalg.norm(m - t)

        return dir

    def run_tank(self, tank, i, dt):
        fx,fy = tank.get_forward_vector()
        nx,ny = self.get_nearest_mine_direction(tank)

        # run the neural network
        network = self.genetic_algorithm.population[i]
        tr_l, tr_r = network( [fx,fy,nx,ny] )

        # apply the actual force
        rot_force = np.clip(tr_l - tr_r, -parameters.MAX_TURN_RATE, parameters.MAX_TURN_RATE)
        tank.rotate(rot_force)

        tank.speed = (tr_l + tr_r) * dt
        tank.do( MoveBy( (fx * tank.speed, fy * tank.speed), dt ) )

    def step(self, dt):
        for i, tank in enumerate(self.tanks):
            self.run_tank(tank, i, dt)

def run():
    cocos.director.director.init()
    cocos.director.director.run (cocos.scene.Scene(Main()))
