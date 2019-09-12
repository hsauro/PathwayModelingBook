import tellurium as te

r = te.loada ('''
       $Xo -> S1; k1*Xo;
       S1 -> S2; k2*S1;
       S2 -> $X1; k3*S2;

       Xo = 50; S1 = 0; S2 = 0;
       k1 = 0.2; k2 = 0.4; k3 = 2;
''')

result = r.gillespie (0, 30)
r.plot()
