import tellurium as te

r = te.loada ('''
    $Xo -> x; 0.1 + k1*x^4/(k2+x^4);
    x -> $w; k3*x;

    // Initialization here
    k1 = 0.9; k2 = 0.3;
    k3 = 0.7;
''')

# Compute steady state
print (r.getSteadyStateValues())
