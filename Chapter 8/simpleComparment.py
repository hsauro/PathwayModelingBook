import tellurium as te
import pylab

r = te.loada ('''
    compartment V1 = 1, V2 = 10;
    var S1 in V1;
    var S2 in V2;

    S1 -> S2; A*k1*S1;
    S2 -> S1; A*k2*S2;

    S1 = 10; S2 = 0;
    k1 = 0.4; k2 = 0.4; A = 1;
''')

result = r.simulate(1, 40, 100)
r.plot (xlim=(0, 40))
