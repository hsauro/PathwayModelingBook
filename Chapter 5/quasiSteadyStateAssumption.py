import tellurium as te
import pylab

# Comparing the full model with an approximation
# based on the quasi-steady-state assumption
r = te.loada ('''
    Ass := (vo + k2*B)/k1;
    $s -> B; vo - k3*B
    $s -> Af; vo;

    Af -> Bf; k1*Af - k2*Bf;
    Bf -> $w; k3*Bf;

    B = 6.66666;
    Af = 3.33333; Bf = 6.66666;
    vo = 1.5;
    k3 = 0.1;
    // Use k1 = 1000 to obtain a better approximation
    k1 = 0.1;
    Keq = 2;
    k2 = k1/Keq;
''')

result = r.simulate(0, 100, 200, ["time", "Af", "Bf", "Ass", "B"])
r.plot(ylim=(0,30), xlim=(0,100))    
