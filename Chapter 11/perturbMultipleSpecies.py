import tellurium as te
import numpy

# Multiple species perturbations
r = te.loada ('''
    $Xo -> S1;  k1*Xo;
    S1 -> $X1; k2*S1;

    Xo = 1;
    S1 = 0.0;
    k1 = 0.2;
    k2 = 0.4;
''')

# Simulate the first part up to 20 time units
m1 = r.simulate(0, 20, 100, ["time", "S1"])

# Perturb the concentration of S1 by 0.35 units
r.S1 = r.S1 + 0.35

# Continue simulating from last end point
m2 = r.simulate(20, 40, 50, ["time", "S1"])

# Merge the data sets
m3 = numpy.vstack((m1, m2))

# Do a negative perturbation in S1
r.S1 = r.S1 - 0.35

# Continue simulating from last end point
m4 = r.simulate(40, 60, 50, ["time", "S1"])

# Merge and plot the final two halves of the simulation
result = numpy.vstack((m3, m4))
te.plotWithLegend(r, result)
