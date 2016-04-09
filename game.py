import cocos
from cocos.actions import *

import numpy.random as np

from entities import Tank, Mine

def generate_tanks(n,w,h):
    tanks = []

    for i in range(n):
        tanks.append(Tank( np.randint(0,w), np.randint(0,h), np.randint(0,360), False ))

    return tanks

def generate_mines(n,w,h):
    mines = []

    for i in range(n):
        mines.append(Mine(np.randint(0,w), np.randint(0,h)))

    return mines

TIME = 1/60


class Main(cocos.layer.ColorLayer):
    def __init__(self):
        # cornflower blue
        super(Main, self).__init__(100, 149, 237, 127)
        self._setup()
        self.schedule(self.step)

    def _setup(self):
        self.mines = generate_mines(15, 640, 480)
        for mine in self.mines:
            mine.add_to_layer(self)

        self.tanks = generate_tanks(20, 640, 480)
        for tank in self.tanks:
            tank.add_to_layer(self)

    def step(self, dt):

cocos.director.director.init()
cocos.director.director.run (cocos.scene.Scene(Main()))
