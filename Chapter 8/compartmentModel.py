import tellurium as te

r = te.loada ('''
    compartment V1, V2;
    var S1 in V1, S2 in V2;
    S1 -> S2; A*k*(S1-S2/Keq)/(1 + S1/Km1 + S2/Km2);

    V1 = 1;  V2 = 10;
    S1 = 21;
    A = 1; k = 1;
    Km1 = 0.5; Km2 = 0.5; Keq = 2;
''')

result = r.simulate(0, 200, 100)
r.plot()
print ("Total Mass = ", r.S1*r.V1 + r.S2*r.V2)
