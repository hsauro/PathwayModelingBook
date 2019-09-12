import tellurium as te

rr = te.loada ('''
    $Xo -> A;  vo;
    A -> B;   k1*A;
    B -> $X1; k3*B;

    // Set up the model initial conditions
    Xo = 1; X1 = 0;
    vo = 0.5; k1 = 0.2; k3 = 0.3;
''')

# Evaluate the steady state
# Evaluate returns a number indicating how far we are
# from the steady state solution. A number less that 1E-6
# is a good indicator that it has found the steady state.
rr.steadyState()
print (rr.A, rr.B)
