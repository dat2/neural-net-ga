from bitstring import Bits

def split_n(n, s):
    return [ s[x:x+n] for x in range(0, len(s), n)]

def encode_floats(floats):
    packed = map(lambda x: Bits(float=x, length=32).bin, floats)
    return ''.join(packed)

def decode_floats(s):
    return list(map(lambda s: Bits(bin=s).float, split_n(32, s)))

def flip_bit(bit):
    return '1' if bit == '0' else '1'

import numpy as np

from neural_net import NeuralNetwork

class GeneticAlgorithm:
    def __init__(self, population_size, crossover_rate, mutation_rate, n_layers):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.n_layers = n_layers

        self.population = self.generate_initial_population()

        # these must be normalized at all times
        self.fitnesses = self.zero_fitnesses()

    def zero_fitnesses(self):
        return np.array( [1.0/self.population_size] * self.population_size)

    def generate_initial_population(self):
        new_population = []

        for i in range(self.population_size):
            new_population.append(NeuralNetwork(self.n_layers))

        return new_population

    def roulette_select(self):
        return np.random.choice(self.population, p=self.fitnesses)

    def mutate(self, chromosome):
        return ''.join([ flip_bit(c) if np.random.random_sample() <= self.mutation_rate else c for c in chromosome ])

    def cross(self, a, b):
        rand = np.random.random_sample()
        if rand >= self.crossover_rate:
            return a,b

        index = np.random.randint(0, len(a))
        return [ a[:index] + b[index:], b[:index] + a[index:] ]

    def make_new_generation(self):
        new_population = []

        while len(new_population) != len(self.population):
            a = self.roulette_select()
            a_encoded = encode_floats(a.encode())

            # find a unique partner
            b = self.roulette_select()
            b_encoded = encode_floats(b.encode())
            while b_encoded != a_encoded:
                b = self.roulette_select()
                b_encoded = encode_floats(b.encode())

            ca,cb = self.cross(a_encoded,b_encoded)
            ma = self.mutate(ca)
            mb = self.mutate(cb)

            decoded_a = NeuralNetwork.decode(self.n_layers, decode_floats(ma))
            decoded_b = NeuralNetwork.decode(self.n_layers, decode_floats(mb))

            new_population.append( decoded_a )
            new_population.append( decoded_b )

        self.population = new_population
        self.fitnesses = self.zero_fitnesses()

