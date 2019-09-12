import tellurium as te
import numpy as np

# Steady state band detector
rr = te.loada ('''
    $G1 -> P2; t1*a1*P1/(1 + a1*P1);
    P2 -> $w;  gamma_1*P2;
    $G3 -> P3; t2*b1*P1/(1 + b1*P1 + b2*P2 + b3*P1*P2^8);
    P3 -> $w;  gamma_2*P3;

    P2 = 0;    P3 = 0;
    P1 = 0.01; G3 = 0;
    G1 = 0;
    t1 = 5;    a1 = 0.05;
    t2 = 0.8;  b1 = 1;
    b2 = 0.1;  b3 = 10;
    gamma_1 = 0.1;
    gamma_2 = 0.1;
''')

# Steady state response
n = 200
m = np.empty([n, 2])
for i in range (0, n):
    m[i, 0] = rr.P1
    m[i, 1] = rr.P3
    rr.getSteadyStateValues()
    rr.P1 = rr.P1 + 0.005
te.plotArray(m)
