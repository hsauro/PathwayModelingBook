# Written and supplied by Wilbert Copeland, 2014
# Differential evolution code, used to fit the Henirich model (Figure 8.15)
import random
import sys
from datetime import datetime
import scipy.integrate
import numpy
import matplotlib.pyplot as mplot


"""
Best values:
ObjFunc = Sum of Differences Squared, Generations = 2000
Fitness: 0.33 Vector: [8.0227418, 0.9762534, 98.806163,
                732.4952511, 1.0336005, 108.808089, 5.0047913]

ObjFunc = Percent Error, Generations = 250
Fitness: 0.076 Vector: [8.0497271, 0.9955929, 2.8358877, 37.7531871,
               1.0162701, 130.1762945, 5.0427175]

"""

# Expected fitted values:
# 8, 1, 0, 1, 1, 2.2, 5

class DiffEvo(object):
    def __init__(self, dy, y0, t, expected):
        self.DY = dy
        self.Y0 = y0
        self.T = t
        self.Expected = expected
        self.Islands = []
        return

    def CreateIsland(self, population_size, vector_length, min_val, max_val):
        island = []
        for i in range(population_size):
            island.append(self.CreateRandomMember(vector_length, min_val, max_val))
        self.Islands.append(island)
        return

    def CreateRandomMember(self, vector_length, min_val, max_val):
        v = [round(random.uniform(min_val, max_val), 7) for i in range(vector_length)]
        f = self.GetFitness(v)
        return Member(v,f)

    def CreateTrialMember(self, original, samples, CR=0.6, F=0.8):
        o = original.Vector
        a = samples[0].Vector
        b = samples[1].Vector
        c = samples[2].Vector

        new_vector = []
        for i in range(len(o)):
            if random.random() <= CR:
                v = round(a[i] + F * (b[i] - c[i]), 7)
                if v>0:
                    new_vector.append(v)
                else:
                    new_vector.append(o[i]/2.)
            else:
                new_vector.append(o[i])
        new_fitness = self.GetFitness(new_vector)
        return Member(new_vector, new_fitness)

    def GetFitness(self, vector):
        obs = scipy.integrate.odeint(self.DY, self.Y0, self.T, args=(vector,), mxstep=1000)
        sum_of_squares = 0.
        for i in range(len(obs)):
            for j in range(len(obs[i])):
                if self.Expected[i][j+1] == 0:
                    0.
                else:
                    sum_of_squares += ((obs[i][j] -
                            self.Expected[i][j+1])/ self.Expected[i][j+1]) ** 2
        return sum_of_squares

    def SortIslandsByFitness(self):
        for island in self.Islands:
            island = sorted(island, key=lambda o: o.Fitness)
        return

class Member(object):
    def __init__(self, vector, fitness):
        self.Vector = vector
        self.Fitness = fitness
        return

# Heinrich model using used in main text
def dY(y, t, p):
    dy0 = p[0] - y[0] * 1. - (p[1] * y[0] - 0. * y[1]) * (1. + p[4] * y[1] ** 4)
    dy1 = (p[1] * y[0] - 0. * y[1]) * (1. + p[4] * y[1] ** 4) - y[1] * p[6]
    return [dy0, dy1]

def PlotResults(de):
    best_members = [x[0] for x in de.Islands]
    solution = scipy.integrate.odeint(de.DY, de.Y0, de.T, args=(best_members[0].Vector, ))

    exp_t = [de.Expected[i][0] for i in range(len(de.Expected))]
    exp_y0 = [de.Expected[i][1] for i in range(len(de.Expected))]
    exp_y1 = [de.Expected[i][2] for i in range(len(de.Expected))]

    obs_y0 = solution[:,0]
    obs_y1 = solution[:,1]

    mplot.plot(exp_t, exp_y0, 'bo')
    mplot.plot(exp_t, exp_y1, 'go')
    mplot.plot(de.T, obs_y0)
    mplot.plot(de.T, obs_y1)
    mplot.xlabel('Time')
    mplot.ylabel('Unknown')
    mplot.show()
    return [exp_t, obs_y0, obs_y1]

# Read file
file = open('expdata.txt','r')
data = []
for line in file:
    d = line.replace('\n','').split('  ')
    d = [float(x) for x in d]
    data.append(d)


# Differential evolution
GENERATION_COUNT = 0
MAX_GENERATIONS = 200
FITNESS_THRESHOLD = 1e-6
PARAMETER_COUNT = 7

NI = 1      # Number of islands
MF = 0.45   # Migration frequency
NM = 1      # Number of migrants
SP = 3      # Selection policy = Randomly choose one of the top 3 for migration.
RP = 3      # Replacement policy = Randomly choose one of the top 3 for migration.
MT = range(NI)[1:] + [0]    # Migration topology: Ciricular, unidirectional

#random.seed (4532)

print('Starting DE search.')
clock = datetime.now()

# Initialize Diff Evo routine
DE = DiffEvo(dy=dY, y0=[1., 0.], t=numpy.linspace(0., 10., 50), expected=data)

# Create islands
[DE.CreateIsland(30, 7, 0., 10.) for i in range(NI)]
for island in DE.Islands:
    assert len(island) > 3

while True:
    GENERATION_COUNT += 1

    for island in DE.Islands:
        samples = [random.sample(island, k=3) for i in range(len(island))]
        trial_values = [DE.CreateTrialMember(island[i], samples[i]) for i in range(len(island))]

        for i in range(len(island)):
            if trial_values[i].Fitness < island[i].Fitness:
                island[i] = trial_values[i]

        DE.SortIslandsByFitness()

    top_members = [x[0] for x in DE.Islands]
    for member in top_members:
        print('Fitness: {0}'.format(round(member.Fitness,3)))

    if GENERATION_COUNT >= MAX_GENERATIONS or
              min([x[0].Fitness for x in DE.Islands]) < FITNESS_THRESHOLD:
        top_members = [x[0] for x in DE.Islands]
        for member in top_members:
            print('Fitness: {0} Vector: {1}'.format(round(member.Fitness,3), member.Vector))
        break

print('Done optimizing.')
print('Optimization time: {0}'.format(datetime.now()-clock))

PlotResults(de=DE)

print('Done.')
