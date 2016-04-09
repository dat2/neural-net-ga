import numpy as np
from functools import reduce

def trace(x):
    print(x)
    return x

class NeuralNetwork:
    def __init__(self, n_layers):
        # if n_layers = [3,4,2]
        # n_layers[:-1] = [3,4]
        # n_layers[1:] = [4,2]
        # zip(n_layers[:-1], n_layers[1:]) [ [3,4] [4,2] ]
        # the matrices should be:
        # input: 3x1, layer1: 4x3, layer2: 2x4
        # to include bias, add 1 to second argument

        self.n_layers = n_layers
        self.layers = np.array([np.random.rand(b,a) for a,b in zip(n_layers[:-1], n_layers[1:])])

    def __call__(self, input):
        return reduce(lambda a, l: l.dot(a), self.layers, np.array(input))

    def __str__(self):
        return 'NeuralNetwork { layers=' + str(self.layers) + ' }'

    def encode(self):
        return reduce( lambda a,l: np.concatenate([a, np.ravel(l)]), self.layers, [] )

    # TODO decoded encoded are not equal
    def __eq__(self, other):
        return np.array_equal(self.layers, other.layers)

    @staticmethod
    def decode(n_layers, array):
        net = NeuralNetwork(n_layers)

        array_i = 0

        for layer in net.layers:
            for x in np.nditer(layer, op_flags=['writeonly']):
                x[...] = array[array_i]
                array_i += 1

        return net

