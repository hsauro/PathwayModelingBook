import tellurium as te
import numpy

r = te.loada ('''
    $Xo -> S1; k1 * Xo;
    S1 -> S2; k2*S1;
    S2 -> $X1; k3*S2;

    Xo = 50; S1 = 0; S2 = 0;
    k1 = 0.2; k2 = 0.4; k3 = 2;
''')

m1 = r.gillespie(0, 30)
r.k1 = r.k1/6
m2 = r.gillespie(30, 60)

# Merge the two data sets
result = numpy.vstack((m1, m2))
te.plotWithLegend(r, result)
