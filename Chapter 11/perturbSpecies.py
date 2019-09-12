import tellurium as te
import numpy

# Perturbing a species concentration
r = te.loada ('''
      $Xo -> S1;  k1*Xo;
      S1 -> $X1; k2*S1;

      Xo = 1;
      S1 = 0.5;
      k1 = 0.2;
      k2 = 0.4;
''')

# Simulate the first part up to 20 time units
m1 = r.simulate(0, 20, 100, ["time", "S1"])

# Perturb the concentration of S1 by 0.35 units
r.S1 = r.S1 + 0.35

# Continue simulating from last end point
m2 = r.simulate(20, 50, 100, ["time", "S1"])

# Merge and plot the two halves of the simulation
result = numpy.vstack((m1, m2))
te.plotWithLegend(r, result)
