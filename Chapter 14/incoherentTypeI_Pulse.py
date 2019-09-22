import tellurium as te
import numpy

# Incoherent Type I Genetic Network, Pulse generator
rr = te.loada ('''
    $G1 -> P2; t1*a1*P1/(1 + a1*P1);
    P2 -> $w;  gamma_1*P2;
    $G3 -> P3; t2*b1*P1/(1 + b1*P1 + b2*P2 + b3*P1*P2^8);
    P3 -> $w;  gamma_2*P3;

    P2 = 0;
    P3 = 0;
    P1 = 0.01;
    G3 = 0;
    G1 = 0;
    t1 = 5;
    a1 = 0.1;
    t2 = 1;
    b1 = 1;
    b2 = 0.1;
    b3 = 10;
    gamma_1 = 0.1;
    gamma_2 = 0.1;
''')

# Time course response for a step pulse
rr.P1 = 0.0;
m1 = rr.simulate(0, 10, 100, ["Time", "P1", "P3"])
rr.P1 = 0.4 # Input stimulus
m2 = rr.simulate(10, 50, 200, ["Time", "P1", "P3"])
m = numpy.vstack((m1, m2))
te.plotWithLegend(rr, m)
