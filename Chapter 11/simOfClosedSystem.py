import tellurium as te

# Simulation of a simple closed system
r = te.loada ('''
    A -> B; k1 * A;
    B -> A; k2 * B;

    A = 10; B = 0;
    k1 = 1; k2 = 0.5;
''')

result = r.simulate(0, 3, 100)
r.plot()
