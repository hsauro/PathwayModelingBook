import tellurium as te
import pylab

# Chattering in a bistable system
r = te.loada ('''
    $Xo -> x; b1 + Vm*(x/Km)*(1+(x/Km))^(n-1)/((1+(x/Km))^n+k2);
    x -> $w; k3*x;

    k2 = 200; k3 = 4.2;
    Vm = 110; Km = 3.6;
    n = 3.7;  b1 = 10;

    x = 15; # Initialize number of molecules
''')

m = r.gillespie(0, 140, ["Time", "x"])
# Plot and set the x axis limits
r.plot (xlim=(0,140))
