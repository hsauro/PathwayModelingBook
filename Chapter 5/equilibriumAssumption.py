import tellurium as te
import pylab

# Comparing the full model with an approximation
# based on the equilibrium assumption
r = te.loada ('''
    // Model using the equilibrium assumption
    // Note the use of := which represents a simulation rule
    B := T*Keq/(1+Keq);
    A := T - B;
    $s -> T; vo - k3*B;

    // The full model
    $s -> Af; vo;
    Af -> Bf; k1*Af - k2*Bf;
    Bf -> $w; k3*Bf;

    T = 10;

    Af = 3.33333; Bf = 6.66666;
    Keq = 2; vo = 0.5;
    k3 = 0.1; k1 = 1;
    k2 = k1/Keq
''')

result = r.simulate(0, 100, 200, ["time", "Af", "Bf", "A", "B", "T"])
r.plot(ylim=(0,10), xlim=(0,100))
m = r.simulate (0, 20, 100);
r.plot(); 
