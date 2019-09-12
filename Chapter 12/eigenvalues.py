import tellurium as te

rr = te.loada ('''
    $Xo -> S1;  k1*Xo;
    S1 -> $X1; k2*S1;

    // Set up the model initial conditions
    Xo = 1;   X1 = 0;
    k1 = 0.2; k2 = 0.3;
''')

# Evaluation of the steady state
rr.getSteadyStateValues()

# print the eigenvalues of the full Jacobian matrix
print (rr.getFullEigenValues())
