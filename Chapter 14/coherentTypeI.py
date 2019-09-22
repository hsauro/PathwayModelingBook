import tellurium as te
import numpy

# Coherent Type I Genetic Network, noise filter
rr = te.loada ('''
    $G2 -> P2; Vmax2*P1^4/(Km1 + P1^4);
    P2 -> $w;  k1*P2;
    $G3 -> P3; Vmax3*P1^4*P2^4/(Km1 + P1^4*P2^4);
    P3 -> $w;  k1*P3;

    Vmax2 = 1; Vmax3 = 1;
    Km1 = 0.5; k1 = 0.1;
    P1 = 0;    P2 = 0;    P3 = 0;
''')

rr.getSteadyStateValues()
print (rr.getFloatingSpeciesConcentrations())

# Pulse width
# Set to 1 for no effect
# Set to 4 for full effect
width = 1
rr.P1 = 0.3
m1 = rr.simulate(0, 10, 100, ["time", "P1", "P3"])
rr.P1 = 0.7 # input stimulus
m2 = rr.simulate(10, 10 + width, 100, ["time", "P1", "P3"])
rr.P1 = 0.3
m3 = rr.simulate(10 + width, 40, 100, ["time", "P1", "P3"])
m = numpy.vstack((m1, m2))
result = numpy.vstack((m, m3))
te.plotWithLegend(rr, result)
