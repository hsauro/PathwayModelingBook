import tellurium as te

# Simulation of an open system
r = te.loada ('''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;

    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
''')

result = r.simulate(0, 6, 100)
r.plot()
