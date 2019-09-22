import tellurium as te

r = te.loada ('''
     $Xo -> S1;  k1*Xo - k2*S1;
     S1 -> S2;  k3*S1 - k4*S2;
     S2 -> $X1; k4*S2 - k6*X1;

    // Initialize value
    Xo = 10; X1 = 0;
    k1 = 3.4; k2 = 0.2;
    k2 = 2.3; k3 = 0.56;
    k4 = 5.6; k6 = 0.12;

    // Initial starting point
    S1 = 1; S2 = 1;
''')

# Compute steady state
r.getSteadyStateValues()
print (r.S1, r.S2)
