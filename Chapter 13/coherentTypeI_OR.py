import tellurium as te
import numpy

# Coherent Type I Genetic Network, delay circuit using OR gate
rr = te.loada ('''
    $G2 -> P2;  Vmax2*P1^4/(Km1 + P1^4);
    P2 -> $w;   k1*P2;
    $G3 -> P3;  Vmax3*(P1^4 + P2^4)/(Km1 + P1^4 + P2^4);
    P3 -> $w;   k1*P3;

    Vmax2 = 1;  Vmax3 = 0.1;
    Km1 = 0.5;  k1 = 0.1;
    P1 = 0;     P2 = 0;     P3 = 0;
''')

rr.getSteadyStateValues()
print (rr.getFloatingSpeciesConcentrations())

# Pulse width
# Set to 1 for no effect
# Set to 4 for full effect
width = 10
rr.P1 = 0.3
m1 = rr.simulate(0, 50, 200, ["Time", "P1", "P3"]).copy()
rr.P1 = 0.8 # Input stimulus
m2 = rr.simulate(50, 50 + width, 200, ["Time", "P1", "P3"]).copy()
rr.P1 = 0.3
m3 = rr.simulate(50 + width, 200, 200, ["Time", "P1", "P3"]).copy()
m = numpy.vstack((m1, m2))
result = numpy.vstack((m, m3))
te.plotWithLegend(rr, result)
