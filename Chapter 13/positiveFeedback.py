import tellurium as te
import numpy

rr = te.loada ('''
    J1: $Xo -> x; 0.1 + k1*x^4/(k2+x^4);
    x -> $w; k3*x;

    k1 = 0.9;
    k2 = 0.3;
    k3 = 0.7;
    x = 0.05;
''')

m = rr.simulate(0, 15, 100)
for i in range(1, 10):
    rr.x = i*0.2
    mm = rr.simulate(0, 15, 100, ["x"])
    m = numpy.hstack((m, mm))
te.plotArray(m)
