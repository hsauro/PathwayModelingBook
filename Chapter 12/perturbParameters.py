import tellurium as te
import numpy
import pylab

r = te.loada ('''
    $Xo -> S1;  k1*Xo;
    S1 -> $X1; k2*S1;

    Xo = 1;
    S1 = 0.5;
    k1 = 0.2;
    k2 = 0.4;
''')

# Simulate the first part up to 20 time units
m1 = r.simulate(0, 20, 5, ["time", "S1"]).copy()

# Perturb the parameter k1
r.k1 = r.k1 * 1.7

# Simulate from the last point
m2 = r.simulate(20, 50, 40, ["time", "S1"]).copy()

# Restore the parameter back to ordinal value
r.k1 = 0.2

# Carry out final run of the simulation
m3 = r.simulate(50, 80, 40, ["time", "S1"])

# Merge all data sets and plot
result = numpy.vstack((m1, m2, m3))
pylab.ylim([0,1])
te.plotWithLegend(r, result)
